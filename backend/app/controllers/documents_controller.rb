class DocumentsController < ApplicationController
  # GET /api/documents — 최근 문서 목록
  def index
    documents = Document.recent.limit(20).select(:id, :filename, :byte_size, :summary, :created_at)
    render json: documents.map { |d| list_json(d) }
  end

  # GET /api/documents/:id — 문서 + 요약
  def show
    render json: detail_json(Document.find(params[:id]))
  end

  # POST /api/documents — 업로드 → FastAPI 요약 → 저장
  def create
    file = params.require(:file)
    return render_error("파일 형식이 올바르지 않습니다.", :bad_request) unless file.respond_to?(:original_filename)
    return render_error(Document.unsupported_message(file.original_filename), :unsupported_media_type) unless Document.allowed_extension?(file.original_filename)
    return render_error("파일이 너무 큽니다. (최대 #{Document::MAX_BYTES / 1.megabyte}MB)", :content_too_large) if file.size > Document::MAX_BYTES

    result = ai_client.summarize(file)
    document = Document.create!(
      filename: file.original_filename,
      content_type: file.content_type,
      byte_size: file.size,
      original_text: result["text"],
      summary: result["summary"],
      ai_document_id: result["document_id"]
    )
    render json: detail_json(document), status: :created
  end

  private

  def list_json(document)
    document.as_json(only: %i[id filename byte_size created_at])
            .merge("summary_preview" => document.summary.to_s.truncate(120))
  end

  def detail_json(document)
    document.as_json(only: %i[id filename content_type byte_size summary created_at])
            .merge("char_count" => document.char_count)
  end
end
