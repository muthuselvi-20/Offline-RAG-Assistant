from io import BytesIO
from docx import Document


def read_docx(file_bytes):

    document = Document(
        BytesIO(file_bytes)
    )

    extracted_text = []

    # Read paragraphs
    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:

            extracted_text.append(text)

    # Read tables
    for table in document.tables:

        for row in table.rows:

            row_data = []

            for cell in row.cells:

                value = cell.text.strip()

                if value:

                    row_data.append(value)

            if row_data:

                extracted_text.append(
                    " | ".join(row_data)
                )

    final_text = "\n".join(
        extracted_text
    )

    if not final_text.strip():

        return []

    return [{
        "text": final_text,
        "page": None
    }]