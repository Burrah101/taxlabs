from flask import Flask, request, jsonify, send_file
import os
from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def health():
    return "TaxLabs backend is running"


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    csv_path = os.path.join(UPLOAD_DIR, file.filename)
    html_path = os.path.join(OUTPUT_DIR, "report.html")
    pdf_path = os.path.join(OUTPUT_DIR, "TaxLabs_Report.pdf")

    file.save(csv_path)

    try:
        generate_report(csv_path, html_path)
        generate_pdf(html_path, pdf_path)

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="TaxLabs_Report.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500
