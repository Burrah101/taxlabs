from flask import Flask, request, send_file, jsonify
import os

from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)

UPLOAD_DIR = "uploads"
OUTPUT_PDF = "report.pdf"


@app.route("/", methods=["GET"])
def health():
    return "TaxLabs backend is running", 200


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only CSV files are allowed"}), 400

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    csv_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(csv_path)

    try:
        # Generate reports
        generate_report(csv_path)
        generate_pdf(csv_path)

        # Send PDF directly to browser
        return send_file(
            OUTPUT_PDF,
            as_attachment=True,
            download_name="TaxLabs_Report.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
