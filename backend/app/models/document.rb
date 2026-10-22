class Document < ApplicationRecord
  ALLOWED_EXTENSIONS = %w[.txt .pdf].freeze
  MAX_BYTES = ENV.fetch("MAX_UPLOAD_MB", 10).to_i.megabytes

  has_many :qa_histories, -> { order(:created_at) }, dependent: :delete_all

  validates :filename, :ai_document_id, presence: true
  validates :ai_document_id, uniqueness: true

  scope :recent, -> { order(created_at: :desc) }

  def self.allowed_extension?(filename)
    ALLOWED_EXTENSIONS.include?(File.extname(filename.to_s).downcase)
  end

  def char_count
    original_text.to_s.length
  end
end
