from flask import Flask, request, jsonify, send_file
import os

from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)

UPLOAD_DIR = "uploads"
OUTPUT_HTML = "report.html"
OUTPUT_PDF = "TaxLabs_Report.pdf"


@app.route("/", methods=["GET"])
def health():
    return "TaxLabs backend is running", 200


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return jsonify({
            "message": "POST a CSV file to this endpoint."
        }), 200

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    csv_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(csv_path)

    try:
        generate_report(csv_path, OUTPUT_HTML)
        generate_pdf(OUTPUT_HTML, OUTPUT_PDF)

        return send_file(
            OUTPUT_PDF,
            as_attachment=True,
            download_name=OUTPUT_PDF
        )

    except Exception as e:
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500
