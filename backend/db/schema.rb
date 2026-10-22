# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[8.1].define(version: 2026_10_23_000002) do
  # These are extensions that must be enabled in order to support this database
  enable_extension "pg_catalog.plpgsql"

  create_table "documents", force: :cascade do |t|
    t.string "filename", null: false
    t.string "content_type"
    t.integer "byte_size"
    t.text "original_text"
    t.text "summary"
    t.string "ai_document_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["ai_document_id"], name: "index_documents_on_ai_document_id", unique: true
    t.index ["created_at"], name: "index_documents_on_created_at"
  end

  create_table "qa_histories", force: :cascade do |t|
    t.bigint "document_id", null: false
    t.text "question", null: false
    t.text "answer", null: false
    t.jsonb "sources", default: [], null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["document_id"], name: "index_qa_histories_on_document_id"
  end

  add_foreign_key "qa_histories", "documents", on_delete: :cascade
end
