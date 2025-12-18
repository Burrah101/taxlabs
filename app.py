from flask import Flask, request, jsonify, send_file
import os

from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)

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

    os.makedirs("uploads", exist_ok=True)
    path = os.path.join("uploads", file.filename)
    file.save(path)

    # Generate reports
    generate_report(path)
    generate_pdf(path)

    # Return PDF directly (THIS IS THE KEY)
    return send_file(
        "TaxLabs_Report.pdf",
        as_attachment=True,
        download_name="TaxLabs_Report.pdf"
    )
