require "test_helper"

# FastAPI 호출 없이 Rails 오케스트레이션 흐름을 검증한다.
class DocumentsFlowTest < ActionDispatch::IntegrationTest
  class FakeAiClient
    def summarize(_file)
      { "document_id" => SecureRandom.hex(16), "summary" => "요약 결과", "text" => "원문 텍스트" }
    end

    def ask(document_id, question)
      raise AiClient::Error.new("인덱스 없음", status: 404) if document_id == "missing"

      { "answer" => "#{question}에 대한 답변", "sources" => [ { "chunk_index" => 0, "text" => "원문", "score" => 1.0 } ] }
    end
  end

  setup do
    fake = FakeAiClient.new
    AiClient.define_singleton_method(:new) { |*| fake }
  end

  teardown do
    AiClient.singleton_class.remove_method(:new)
  end

  test "업로드 후 요약을 저장하고 질문 히스토리를 남긴다" do
    post "/api/documents", params: { file: fixture_file_upload("sample.txt", "text/plain") }
    assert_response :created
    doc = response.parsed_body
    assert_equal "요약 결과", doc["summary"]
    assert_equal "sample.txt", doc["filename"]

    get "/api/documents"
    assert_equal [ doc["id"] ], response.parsed_body.map { |d| d["id"] }

    post "/api/documents/#{doc['id']}/questions", params: { question: "무엇?" }, as: :json
    assert_response :created
    assert_equal "무엇?에 대한 답변", response.parsed_body["answer"]

    get "/api/documents/#{doc['id']}/questions"
    assert_equal 1, response.parsed_body.size
    assert_equal 0, response.parsed_body.first["sources"].first["chunk_index"]
  end

  test "지원하지 않는 형식은 415이고 지원 형식을 안내한다" do
    post "/api/documents", params: { file: fixture_file_upload("sample.png", "image/png") }
    assert_response :unsupported_media_type
    assert_includes response.parsed_body["error"], "TXT, MD, PDF, DOCX, PPTX"
  end

  test "MD, DOCX, PPTX, PDF 업로드를 받아들인다" do
    %w[note.md note.markdown report.DOCX deck.pptx doc.pdf].each do |name|
      file = Rack::Test::UploadedFile.new(StringIO.new("x"), "application/octet-stream", original_filename: name)
      post "/api/documents", params: { file: file }
      assert_response :created, "#{name} 업로드 실패"
    end
  end

  test "구형 doc, ppt는 변환 안내와 함께 415" do
    { "old.doc" => ".docx", "old.PPT" => ".pptx" }.each do |name, target|
      file = Rack::Test::UploadedFile.new(StringIO.new("x"), "application/msword", original_filename: name)
      post "/api/documents", params: { file: file }
      assert_response :unsupported_media_type
      assert_includes response.parsed_body["error"], "#{target}로 저장"
    end
  end

  test "파일 없이 요청하면 400" do
    post "/api/documents"
    assert_response :bad_request
  end

  test "없는 문서는 404" do
    get "/api/documents/999999"
    assert_response :not_found
  end

  test "AI 서버 오류 상태를 그대로 전달한다" do
    doc = Document.create!(filename: "x.txt", ai_document_id: "missing")
    post "/api/documents/#{doc.id}/questions", params: { question: "질문" }, as: :json
    assert_response :not_found
    assert_equal "인덱스 없음", response.parsed_body["error"]
  end
end
