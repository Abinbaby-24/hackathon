import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from app.schemas.product_schema import ProductData


# Load .env from the project root
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_product(ocr_result: dict) -> ProductData:
    """
    Extract structured product information from OCR result.
    """

    # Get OCR text from Member 2's OCR output
    ocr_text = ocr_result["text"]

    # Load extraction prompt
    prompt_path = Path(__file__).parent / "prompts" / "extraction_prompt.txt"
    prompt = prompt_path.read_text(encoding="utf-8")

    # Send OCR text to Gemini
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"{prompt}\n\nOCR TEXT:\n{ocr_text}",
        config={
            "response_mime_type": "application/json",
            "response_schema": ProductData,
        },
    )

    # Validate Gemini's response against ProductData schema
    return ProductData.model_validate_json(response.text)