from fastapi import FastAPI, UploadFile, File
import shutil
from ocr_engine import extract_text, extract_invoice_data

app = FastAPI()


@app.get("/")
def home():
    return {"message": "OCR API is running"}


@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    try:
        file_path = f"temp_{file.filename}"

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text
        text = extract_text(file_path)

        # Extract structured data
        structured = extract_invoice_data(text)

        return {
            "status": "success",
            "raw_text": text,
            "structured_data": structured
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
