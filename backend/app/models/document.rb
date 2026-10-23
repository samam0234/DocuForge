class Document < ApplicationRecord
  # FastAPI(document_parser.py)와 Vue(DocumentUpload.vue)의 허용 형식과 같아야 한다.
  ALLOWED_EXTENSIONS = %w[.txt .md .markdown .pdf .docx .pptx].freeze
  SUPPORTED_LABEL = "TXT, MD, PDF, DOCX, PPTX".freeze
  # 구형 Office 형식은 지원하지 않으며 변환 안내를 준다.
  LEGACY_EXTENSIONS = { ".doc" => ".docx", ".ppt" => ".pptx" }.freeze
  MAX_BYTES = ENV.fetch("MAX_UPLOAD_MB", 10).to_i.megabytes

  has_many :qa_histories, -> { order(:created_at) }, dependent: :delete_all

  validates :filename, :ai_document_id, presence: true
  validates :ai_document_id, uniqueness: true

  scope :recent, -> { order(created_at: :desc) }

  def self.allowed_extension?(filename)
    ALLOWED_EXTENSIONS.include?(File.extname(filename.to_s).downcase)
  end

  def self.unsupported_message(filename)
    ext = File.extname(filename.to_s).downcase
    if LEGACY_EXTENSIONS.key?(ext)
      "구형 #{ext} 형식은 지원하지 않습니다. #{LEGACY_EXTENSIONS[ext]}로 저장한 뒤 업로드해 주세요."
    else
      "#{SUPPORTED_LABEL} 파일만 업로드할 수 있습니다."
    end
  end

  def char_count
    original_text.to_s.length
  end
end
