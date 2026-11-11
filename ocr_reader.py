import easyocr
import cv2
import numpy as np

from io import BytesIO


# Initialize OCR model only once
reader = easyocr.Reader(
    ["en"],
    gpu=False
)


def read_image(file_bytes):

    image_array = np.frombuffer(
        file_bytes,
        np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        raise ValueError(
            "Unable to read image"
        )

    results = reader.readtext(
        image,
        detail=0,
        paragraph=True
    )

    extracted_text = "\n".join(
        results
    )

    if not extracted_text.strip():

        return []

    return [{
        "text": extracted_text,
        "page": None
    }]