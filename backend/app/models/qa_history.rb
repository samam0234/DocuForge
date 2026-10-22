class QaHistory < ApplicationRecord
  belongs_to :document

  validates :question, :answer, presence: true
end
