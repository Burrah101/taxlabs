from flask import Flask, request, send_file, jsonify
import os

from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)

@app.route("/")
def health():
    return "TaxLabs backend is running"

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    os.makedirs("uploads", exist_ok=True)

    csv_path = os.path.join("uploads", file.filename)
    file.save(csv_path)

    try:
        html_path = generate_report(csv_path, "report.html")
        pdf_path = generate_pdf(html_path, "TaxLabs_Report.pdf")

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="TaxLabs_Report.pdf"
        )

    except Exception as e:
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500
