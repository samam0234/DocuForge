class ApplicationController < ActionController::API
  rescue_from ActiveRecord::RecordNotFound do
    render_error("문서를 찾을 수 없습니다.", :not_found)
  end

  rescue_from ActionController::ParameterMissing do |e|
    render_error("필수 값이 없습니다: #{e.param}", :bad_request)
  end

  rescue_from ActiveRecord::RecordInvalid do |e|
    render_error(e.record.errors.full_messages.join(", "), :unprocessable_content)
  end

  rescue_from AiClient::Error do |e|
    render_error(e.message, e.status)
  end

  private

  def render_error(message, status)
    render json: { error: message }, status: status
  end

  def ai_client
    @ai_client ||= AiClient.new
  end
end
