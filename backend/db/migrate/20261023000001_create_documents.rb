class CreateDocuments < ActiveRecord::Migration[8.1]
  def change
    create_table :documents do |t|
      t.string :filename, null: false
      t.string :content_type
      t.integer :byte_size
      t.text :original_text
      t.text :summary
      # FastAPI 청크 인덱스 ID
      t.string :ai_document_id, null: false

      t.timestamps
    end
    add_index :documents, :ai_document_id, unique: true
    add_index :documents, :created_at
  end
end
