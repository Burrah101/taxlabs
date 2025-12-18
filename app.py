from flask import Flask, request, send_file, jsonify, Response
import os
import uuid

from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)

UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


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

    uid = str(uuid.uuid4())
    csv_path = os.path.join(UPLOAD_DIR, f"{uid}.csv")
    html_path = os.path.join(REPORT_DIR, f"{uid}.html")

    file.save(csv_path)

    try:
        generate_report(csv_path, html_path)
    except Exception as e:
        return jsonify({"error": "HTML generation failed", "details": str(e)}), 500

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    return Response(
        html,
        headers={
            "Content-Type": "text/html",
            "X-Report-ID": uid
        }
    )


@app.route("/download-pdf", methods=["GET"])
def download_pdf():
    report_id = request.args.get("id")
    if not report_id:
        return jsonify({"error": "Missing report id"}), 400

    html_path = os.path.join(REPORT_DIR, f"{report_id}.html")
    pdf_path = os.path.join(REPORT_DIR, f"{report_id}.pdf")

    if not os.path.exists(html_path):
        return jsonify({"error": "Report not found"}), 404

    try:
        generate_pdf(html_path, pdf_path)
    except Exception as e:
        return jsonify({"error": "PDF generation failed", "details": str(e)}), 500

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="TaxLabs_Report.pdf",
        mimetype="application/pdf"
    )
