"""업로드 파일 텍스트 추출 및 청크 분할."""
import io
import re
from pathlib import Path

from pypdf import PdfReader

from app.services.office_parser import OfficeParseError, extract_docx, extract_pptx

SUPPORTED_EXTENSIONS = {".txt", ".md", ".markdown", ".pdf", ".docx", ".pptx"}
SUPPORTED_LABEL = "TXT, MD, PDF, DOCX, PPTX"
# 구형 Office 형식은 별도 변환이 필요해 지원하지 않는다
LEGACY_EXTENSIONS = {".doc": ".docx", ".ppt": ".pptx"}


class UnsupportedFormatError(ValueError):
    """지원하지 않는 파일 형식."""


class EmptyDocumentError(ValueError):
    """추출 가능한 텍스트가 없음."""


def extract_text(filename: str, data: bytes) -> str:
    ext = Path(filename).suffix.lower()
    if ext in LEGACY_EXTENSIONS:
        raise UnsupportedFormatError(
            f"구형 {ext} 형식은 지원하지 않습니다. {LEGACY_EXTENSIONS[ext]}로 저장한 뒤 업로드해 주세요."
        )
    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFormatError(
            f"지원하지 않는 형식입니다: {ext or '(확장자 없음)'} ({SUPPORTED_LABEL}만 가능)"
        )

    try:
        text = _EXTRACTORS.get(ext, _decode_text)(data)
    except OfficeParseError as exc:
        raise EmptyDocumentError(str(exc)) from exc
    text = _normalize(text)
    if not text:
        raise EmptyDocumentError("문서에서 텍스트를 추출할 수 없습니다. (스캔·이미지 전용 문서는 지원하지 않습니다)")
    return text


def split_chunks(text: str, size: int, overlap: int) -> list[str]:
    """문단 경계를 우선하여 size 문자 이하 청크로 나누고, 앞 청크 끝 overlap 문자를 겹친다."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        for piece in _hard_split(para, size):
            if current and len(current) + len(piece) + 2 > size:
                chunks.append(current)
                tail = current[-overlap:] if overlap else ""
                current = f"{tail}\n\n{piece}" if tail else piece
            else:
                current = f"{current}\n\n{piece}" if current else piece
    if current:
        chunks.append(current)
    return chunks


def _hard_split(para: str, size: int) -> list[str]:
    if len(para) <= size:
        return [para]
    sentences = re.split(r"(?<=[.!?。])\s+", para)
    pieces, buf = [], ""
    for sent in filter(None, sentences):
        while len(sent) > size:
            pieces.append(sent[:size])
            sent = sent[size:]
        if buf and len(buf) + len(sent) + 1 > size:
            pieces.append(buf)
            buf = sent
        else:
            buf = f"{buf} {sent}" if buf else sent
    if buf:
        pieces.append(buf)
    return pieces


def _extract_pdf(data: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(data))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:  # pypdf는 손상 파일에 다양한 예외를 던진다
        raise EmptyDocumentError(f"PDF를 읽을 수 없습니다: {exc}") from exc


def _decode_text(data: bytes) -> str:
    for encoding in ("utf-8-sig", "cp949", "utf-16"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def _normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


_EXTRACTORS = {".pdf": _extract_pdf, ".docx": extract_docx, ".pptx": extract_pptx}
