require "net/http"
require "json"

# FastAPI AI 서버(/summarize, /ask) 호출 클라이언트.
class AiClient
  # status: Rails가 프론트엔드에 돌려줄 HTTP 상태
  class Error < StandardError
    attr_reader :status

    def initialize(message, status: :bad_gateway)
      super(message)
      @status = status
    end
  end

  # AI 서버의 4xx는 사용자 입력 문제이므로 그대로 전달한다.
  PASS_THROUGH = [ 404, 413, 415, 422 ].freeze

  def initialize(base_url: ENV.fetch("AI_SERVER_URL", "http://localhost:8000"),
                 timeout: ENV.fetch("AI_SERVER_TIMEOUT", 600).to_i)
    @base_uri = URI(base_url)
    @timeout = timeout
  end

  # @param file [ActionDispatch::Http::UploadedFile]
  # @return [Hash] document_id, summary, text, char_count, chunk_count, model
  def summarize(file)
    request = Net::HTTP::Post.new(endpoint("/summarize"))
    request.set_form(
      [ [ "file", file.tempfile, { filename: file.original_filename, content_type: file.content_type } ] ],
      "multipart/form-data"
    )
    perform(request)
  end

  # @return [Hash] answer, sources, model
  def ask(document_id, question)
    request = Net::HTTP::Post.new(endpoint("/ask"), "Content-Type" => "application/json")
    request.body = { document_id: document_id, question: question }.to_json
    perform(request)
  end

  private

  def endpoint(path)
    URI.join(@base_uri.to_s.chomp("/") + "/", path.delete_prefix("/"))
  end

  def perform(request)
    response = Net::HTTP.start(@base_uri.host, @base_uri.port, use_ssl: @base_uri.scheme == "https",
                               open_timeout: 5, read_timeout: @timeout) do |http|
      http.request(request)
    end
    body = parse(response.body)
    return body if response.is_a?(Net::HTTPSuccess)

    status = PASS_THROUGH.include?(response.code.to_i) ? response.code.to_i : :bad_gateway
    raise Error.new(body["detail"].presence || "AI 서버 오류 (#{response.code})", status: status)
  rescue Net::OpenTimeout, Errno::ECONNREFUSED, SocketError => e
    raise Error.new("AI 서버에 연결할 수 없습니다. (#{e.class})", status: :bad_gateway)
  rescue Net::ReadTimeout
    raise Error.new("AI 서버 응답 시간이 초과되었습니다.", status: :gateway_timeout)
  end

  def parse(raw)
    JSON.parse(raw.presence || "{}")
  rescue JSON::ParserError
    {}
  end
end
