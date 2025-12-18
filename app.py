from flask import Flask, request, send_file, jsonify
import os
import uuid

# IMPORTANT: keep these imports once deps are installed
from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)

UPLOAD_DIR = "uploads"
OUT_DIR = "out"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

@app.get("/")
def health():
    return "TaxLabs backend is running", 200

@app.post("/upload")
def upload():
    # 1) Validate upload
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded. Field name must be 'file'."}), 400

    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "Empty filename."}), 400

    # Only allow CSV
    if not f.filename.lower().endswith(".csv"):
        return jsonify({"error": "Only .csv files are supported."}), 400

    # 2) Save file with a safe unique name (avoid weird filenames)
    job_id = str(uuid.uuid4())[:8]
    csv_path = os.path.join(UPLOAD_DIR, f"{job_id}.csv")
    f.save(csv_path)

    # 3) Generate HTML + PDF safely
    try:
        # generate_report writes report.html by your current function design
        # We'll run it in a per-job filename to avoid collisions.
        html_path = os.path.join(OUT_DIR, f"{job_id}.html")
        pdf_path = os.path.join(OUT_DIR, f"TaxLabs_Report_{job_id}.pdf")

        # If your generate_report only accepts csv_path and writes "report.html",
        # we’ll support both styles:
        try:
            # Preferred (if you update generate_report to accept output path)
            generate_report(csv_path, html_path)  # type: ignore
        except TypeError:
            # Current behavior: generate_report(csv_path) -> writes "report.html"
            generate_report(csv_path)
            # Move/rename it to our job html
            if os.path.exists("report.html"):
                os.replace("report.html", html_path)
            else:
                return jsonify({"error": "Report HTML was not generated."}), 500

        # PDF generator: support both styles too
        try:
            generate_pdf(html_path, pdf_path)  # type: ignore
        except TypeError:
            # If your generate_pdf takes only html_path and outputs report.pdf
            generate_pdf(html_path)
            if os.path.exists("report.pdf"):
                os.replace("report.pdf", pdf_path)
            else:
                return jsonify({"error": "Report PDF was not generated."}), 500

        # 4) Return the PDF (this is the main success)
        return send_file(pdf_path, as_attachment=True, download_name=os.path.basename(pdf_path))

    except Exception as e:
        return jsonify({"error": "Processing failed", "details": str(e)}), 500
