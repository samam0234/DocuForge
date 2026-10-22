class CreateQaHistories < ActiveRecord::Migration[8.1]
  def change
    create_table :qa_histories do |t|
      t.references :document, null: false, foreign_key: { on_delete: :cascade }
      t.text :question, null: false
      t.text :answer, null: false
      # 근거 청크 목록 [{ chunk_index, text, score }]
      t.jsonb :sources, null: false, default: []

      t.timestamps
    end
  end
end
