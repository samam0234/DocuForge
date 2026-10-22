class QuestionsController < ApplicationController
  before_action :set_document

  # GET /api/documents/:document_id/questions — 질문 히스토리
  def index
    render json: @document.qa_histories.map { |qa| qa_json(qa) }
  end

  # POST /api/documents/:document_id/questions — 질문 → FastAPI /ask → 저장
  def create
    question = params.require(:question).to_s.strip
    return render_error("질문을 입력해 주세요.", :bad_request) if question.empty?

    result = ai_client.ask(@document.ai_document_id, question)
    qa = @document.qa_histories.create!(question: question, answer: result["answer"], sources: result["sources"] || [])
    render json: qa_json(qa), status: :created
  end

  private

  def set_document
    @document = Document.find(params[:document_id])
  end

  def qa_json(qa)
    qa.as_json(only: %i[id document_id question answer sources created_at])
  end
end
