from app.processing import chunk_pages, extract_pdf_text
from pdf_helpers import pdf_with_text


def test_extract_pdf_text_and_chunk_pages(tmp_path):
    pdf = tmp_path / "sample.pdf"
    pdf.write_bytes(pdf_with_text("First page.", "Second page here."))

    pages = extract_pdf_text(str(pdf))
    chunks = chunk_pages(pages, max_chars=12)

    assert pages == [(1, "First page."), (2, "Second page here.")]
    assert [(chunk.page_number, chunk.position, chunk.text) for chunk in chunks] == [
        (1, 0, "First page."),
        (2, 1, "Second page"),
        (2, 2, "here."),
    ]
