from flask import Flask, request, jsonify, send_file
import os

from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)

UPLOAD_DIR = "uploads"
PDF_NAME = "TaxLabs_Report.pdf"


# -----------------------------
# Health check
# -----------------------------
@app.route("/", methods=["GET"])
def health():
    return "TaxLabs backend is running", 200


# -----------------------------
# Upload endpoint
# -----------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    # ✅ Graceful GET handling (no crash, no confusion)
    if request.method == "GET":
        return jsonify({
            "message": "This endpoint accepts POST requests with a CSV file."
        }), 200

    # ✅ POST logic
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    csv_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(csv_path)

    try:
        # Generate reports
        generate_report(csv_path)
        generate_pdf(csv_path)

        # Return PDF directly (browser auto-downloads)
        return send_file(
            PDF_NAME,
            as_attachment=True,
            download_name=PDF_NAME
        )

    except Exception as e:
        # 🔒 Safe error response instead of 500 crash
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500
