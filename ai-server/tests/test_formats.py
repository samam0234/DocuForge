"""문서 형식별 텍스트 추출 테스트 (Office 문서는 테스트 안에서 생성)."""
import io
import zipfile

import pytest
from docx import Document
from fastapi.testclient import TestClient
from pptx import Presentation
from pptx.util import Inches

from app.config import get_settings
from app.main import app
from app.services import ollama_client
from app.services.document_parser import (
    EmptyDocumentError,
    UnsupportedFormatError,
    extract_text,
)


def make_docx() -> bytes:
    doc = Document()
    doc.add_heading("프로젝트 개요", level=1)
    doc.add_paragraph("DocuForge는 문서 요약 플랫폼이다.")
    table = doc.add_table(rows=2, cols=2)
    table.cell(0, 0).text = "항목"
    table.cell(0, 1).text = "값"
    table.cell(1, 0).text = "모델"
    table.cell(1, 1).text = "gemma4:12b"
    doc.add_paragraph("표 뒤의 문단")
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def make_pptx() -> bytes:
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "분기 보고"
    slide.placeholders[1].text = "매출이 20% 증가했다"
    slide.notes_slide.notes_text_frame.text = "발표 시 강조할 것"
    blank = prs.slides.add_slide(prs.slide_layouts[6])  # 텍스트 없는 슬라이드는 건너뛴다
    group = blank.shapes.add_group_shape()
    box = group.shapes.add_textbox(Inches(1), Inches(1), Inches(3), Inches(1))
    box.text_frame.text = "그룹 안의 텍스트"
    buf = io.BytesIO()
    prs.save(buf)
    return buf.getvalue()


def test_markdown_and_txt_are_decoded():
    assert extract_text("a.md", "# 제목\n\n본문".encode("utf-8")) == "# 제목\n\n본문"
    assert extract_text("a.markdown", b"hello") == "hello"
    assert extract_text("a.txt", "한글".encode("cp949")) == "한글"


def test_docx_keeps_order_headings_and_tables():
    text = extract_text("report.DOCX", make_docx())
    assert text.index("프로젝트 개요") < text.index("DocuForge는") < text.index("모델 | gemma4:12b") < text.index("표 뒤의 문단")
    assert "## 프로젝트 개요" in text
    assert "항목 | 값" in text


def test_pptx_extracts_slides_notes_and_groups():
    text = extract_text("deck.pptx", make_pptx())
    assert "[슬라이드 1]" in text and "분기 보고" in text and "매출이 20% 증가했다" in text
    assert "[발표자 노트]\n발표 시 강조할 것" in text
    assert "[슬라이드 2]" in text and "그룹 안의 텍스트" in text


@pytest.mark.parametrize("name", ["old.doc", "old.ppt"])
def test_legacy_office_formats_get_conversion_hint(name):
    with pytest.raises(UnsupportedFormatError) as exc:
        extract_text(name, b"x")
    assert "저장한 뒤" in str(exc.value)


@pytest.mark.parametrize("name", ["bad.docx", "bad.pptx"])
def test_corrupted_office_files_are_rejected(name):
    with pytest.raises(EmptyDocumentError) as exc:
        extract_text(name, b"not a zip (or password protected)")
    assert "손상" in str(exc.value)


def test_zip_bomb_is_rejected(monkeypatch):
    from app.services import office_parser

    monkeypatch.setattr(office_parser, "MAX_UNCOMPRESSED_BYTES", 10)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("big.xml", "a" * 1000)
    with pytest.raises(EmptyDocumentError) as exc:
        extract_text("bomb.docx", buf.getvalue())
    assert "크기" in str(exc.value)


def test_empty_docx_is_rejected():
    buf = io.BytesIO()
    Document().save(buf)
    with pytest.raises(EmptyDocumentError):
        extract_text("empty.docx", buf.getvalue())


@pytest.fixture
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(get_settings(), "ai_data_dir", tmp_path)
    monkeypatch.setattr(get_settings(), "ollama_embed_model", "")

    async def fake_chat(system, user, **kwargs):
        return "가짜 응답"

    monkeypatch.setattr(ollama_client, "chat", fake_chat)
    return TestClient(app)


@pytest.mark.parametrize(
    "name,data",
    [("a.md", "# 제목\n본문".encode()), ("a.docx", make_docx()), ("a.pptx", make_pptx())],
    ids=["md", "docx", "pptx"],  # 바이트가 테스트 이름에 들어가지 않도록 ID를 지정한다
)
def test_summarize_endpoint_accepts_new_formats(client, name, data):
    res = client.post("/summarize", files={"file": (name, data)})
    assert res.status_code == 200
    assert res.json()["char_count"] > 0


def test_unsupported_message_lists_all_formats(client):
    res = client.post("/summarize", files={"file": ("a.png", b"x")})
    assert res.status_code == 415
    assert "TXT, MD, PDF, DOCX, PPTX" in res.json()["detail"]
    res = client.post("/summarize", files={"file": ("a.doc", b"x")})
    assert res.status_code == 415 and ".docx" in res.json()["detail"]
    res = client.post("/summarize", files={"file": ("a.docx", b"junk")})
    assert res.status_code == 422
