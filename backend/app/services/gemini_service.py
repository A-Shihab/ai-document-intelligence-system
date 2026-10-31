import json
import os
import traceback
from google import genai
from google.genai import types
from app.config import settings

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_id = "gemini-3.5-flash-lite"

    async def extract_document_data(self, content_input: str, file_path: str = None, is_image: bool = False) -> dict:
        prompt = """
        You are an expert financial document intelligence AI. Extract structured data from this invoice document or image.
        You must strictly return a valid JSON object matching this schema:
        {
            "invoice_number": "string or null",
            "invoice_date": "YYYY-MM-DD or null",
            "supplier_name": "string or null",
            "customer_name": "string or null",
            "subtotal": 0.0,
            "tax": 0.0,
            "additional_fees": {
                "shipping": 0.0,
                "handling": 0.0
            },
            "total": 0.0,
            "currency": "USD/EUR/BDT etc or null",
            "line_items": [
                {
                    "description": "string",
                    "quantity": 0,
                    "unit_price": 0.0,
                    "total_price": 0.0
                }
            ],
            "uncertain_fields": []
        }
        Extract any extra charges like shipping, delivery, freight, or handling fees into the additional_fees object as key-value pairs. If none exist, leave it as an empty object {}.
        Do NOT invent or hallucinate values. If a field is missing, set it to null.
        """

        try:
            if is_image and file_path and os.path.exists(file_path):
                mime_type = "image/png"
                if file_path.lower().endswith((".jpg", ".jpeg")):
                    mime_type = "image/jpeg"

                with open(file_path, "rb") as f:
                    image_bytes = f.read()

                print(f"DEBUG - Calling Gemini with image path: {file_path}, size: {len(image_bytes)} bytes")

                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                        prompt
                    ],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.1,
                    ),
                )
            else:
                print(f"DEBUG - Calling Gemini with text content length: {len(content_input)}")
                full_prompt = f"{prompt}\n\nDocument Content:\n{content_input}"
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.1,
                    ),
                )

            if response and response.text:
                print(f"DEBUG - Gemini Raw Response: {response.text}")
                return json.loads(response.text)
            
            print("DEBUG - Gemini returned empty response text.")
            return {"error": "Empty response from Gemini"}
        except Exception as e:
            print(f"!!! GEMINI EXTRACTION CRASHED !!!")
            traceback.print_exc()
            return {"error": f"Gemini extraction failed: {str(e)}"}