import re
import pytesseract
from PIL import Image


def extract_text(image_path: str):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text


def extract_invoice_data(text: str):
    data = {}

    # Split lines
    lines = text.split("\n")

    # Store name (first non-empty line)
    for line in lines:
        if line.strip():
            data["store_name"] = line.strip()
            break

    # GSTIN
    gst = re.search(r'GSTIN[:\s]*([A-Z0-9]+)', text)
    if gst:
        data["gstin"] = gst.group(1)

    # Phone numbers
    phones = re.findall(r'\b\d{10}\b', text)
    if phones:
        data["phone"] = phones

    # Date
    date = re.search(r'\d{2}/\d{2}/\d{4}', text)
    if date:
        data["date"] = date.group()

    # Time
    time = re.search(r'\d{2}:\d{2}', text)
    if time:
        data["time"] = time.group()

    # Invoice number
    inv = re.search(r'(CASHMEMO NO|Invoice No)[:\s]*([0-9]+)', text, re.IGNORECASE)
    if inv:
        data["invoice_number"] = inv.group(2)

    # Amounts
    amounts = re.findall(r'\d{1,3}(?:,\d{3})*\.\d{2}', text)
    if amounts:
        data["amounts"] = amounts

    return data
