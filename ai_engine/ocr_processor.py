"""Extract text from uploaded PDFs or images."""
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp"}


def _ocr_image(image) -> str:
    import pytesseract

    return pytesseract.image_to_string(image)


def extract_text(path: str) -> str:
    p = Path(path)
    ext = p.suffix.lower()

    if ext in IMAGE_EXTS:
        from PIL import Image

        return _ocr_image(Image.open(p)).strip()

    if ext == ".pdf":
        # Try the embedded text layer first (digital PDFs)
        from PyPDF2 import PdfReader

        text = "\n".join((page.extract_text() or "") for page in PdfReader(str(p)).pages).strip()
        if len(text) > 50:
            return text
        # Fall back to OCR for scanned PDFs
        from pdf2image import convert_from_path

        return "\n".join(_ocr_image(img) for img in convert_from_path(str(p))).strip()

    raise ValueError(f"Unsupported file type: {ext}")
