from PIL import Image
import pytesseract

class OCRService:
    @staticmethod
    def extract_text_from_image(file_path: str) -> str:
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            return f"OCR Extraction Error: {str(e)}"