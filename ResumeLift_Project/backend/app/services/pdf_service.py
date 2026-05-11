from __future__ import annotations

import fitz


def extract_text_from_pdf(file_bytes: bytes) -> str:
    if not file_bytes:
        return ""

    document = fitz.open(stream=file_bytes, filetype="pdf")
    pages = []
    for page in document:
        pages.append(page.get_text("text"))
    text = "\n".join(pages)
    return " ".join(text.split())
