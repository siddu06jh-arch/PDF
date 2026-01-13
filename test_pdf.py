import pdfplumber

with pdfplumber.open("yourfile.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""

print("TEXT FOUND:" if text.strip() else "NO TEXT FOUND")

