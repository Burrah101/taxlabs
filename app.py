from flask import Flask, request, jsonify, send_file
import os

from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Health check (Railway + browser)
@app.route("/", methods=["GET"])
def health():
    return "TaxLabs backend is running", 200


# Upload endpoint
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    # ✅ Re-enabled report generation
    generate_report(path)
    generate_pdf(path)

    # ✅ Return the generated PDF
    return send_file(
        "report.pdf",
        as_attachment=True,
        download_name="TaxLabs_Report.pdf",
        mimetype="application/pdf"
    )
