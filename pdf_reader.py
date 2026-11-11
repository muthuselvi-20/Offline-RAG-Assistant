from io import BytesIO
from pypdf import PdfReader


def read_pdf(file_bytes):

    pdf = PdfReader(BytesIO(file_bytes))

    documents = []

    for page_number, page in enumerate(
        pdf.pages,
        start=1
    ):

        text = page.extract_text() or ""

        if text.strip():

            documents.append({

                "text": text,

                "page": page_number

            })

    return documents