The contents of the file /pdf_master/pdf_master/app.py are as follows:

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    after_this_request
)

from pdf2docx import Converter
import pdfplumber
from pdf2image import convert_from_path
import zipfile

import os
import time

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("pdf")
        output_format = request.form.get("format")

        if not file or file.filename == "":
            return render_template("index.html")

        # Original filename (without .pdf)
        original_name = os.path.splitext(file.filename)[0]

        # Safe backend filename
        timestamp = int(time.time())
        pdf_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}.pdf")
        file.save(pdf_path)

        # ==================================================
        # PDF → WORD
        # ==================================================
        if output_format == "word":
            output_path = os.path.join(
                OUTPUT_FOLDER, f"{original_name}.docx"
            )

            cv = Converter(pdf_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()

            @after_this_request
            def cleanup(response):
                try:
                    os.remove(pdf_path)
                    os.remove(output_path)
                except Exception as e:
                    print("Cleanup error:", e)
                return response

            return send_file(
                output_path,
                as_attachment=True,
                download_name=f"{original_name}.docx"
            )

        # ==================================================
        # PDF → TEXT
        # ==================================================
        elif output_format == "text":
            output_path = os.path.join(
                OUTPUT_FOLDER, f"{original_name}.txt"
            )

            full_text = ""

            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    full_text += (page.extract_text() or "") + "\n"

            if not full_text.strip():
                return "No text found in PDF (possibly scanned)"

            with open(output_path, "w") as f:
                f.write(full_text)

            @after_this_request
            def cleanup(response):
                try:
                    os.remove(pdf_path)
                    os.remove(output_path)
                except Exception as e:
                    print("Cleanup error:", e)
                return response

            return send_file(
                output_path,
                as_attachment=True,
                download_name=f"{original_name}.txt"
            )

        # ==================================================
        # PDF → IMAGES (ZIP)
        # ==================================================
        elif output_format == "images":
            images = convert_from_path(pdf_path)

            zip_path = os.path.join(
                OUTPUT_FOLDER, f"{original_name}_images.zip"
            )

            with zipfile.ZipFile(zip_path, "w") as zipf:
                for i, image in enumerate(images):
                    img_name = f"page_{i+1}.png"
                    img_path = os.path.join(OUTPUT_FOLDER, img_name)

                    image.save(img_path, "PNG")
                    zipf.write(img_path, img_name)
                    os.remove(img_path)

            @after_this_request
            def cleanup(response):
                try:
                    os.remove(pdf_path)
                    os.remove(zip_path)
                except Exception as e:
                    print("Cleanup error:", e)
                return response

            return send_file(
                zip_path,
                as_attachment=True,
                download_name=f"{original_name}_images.zip"
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)