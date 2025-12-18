from flask import Flask, request, jsonify, send_file, render_template_string
import os
import uuid

from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)

UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

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

    job_id = str(uuid.uuid4())

    csv_path = os.path.join(UPLOAD_DIR, f"{job_id}.csv")
    html_path = os.path.join(REPORT_DIR, f"{job_id}.html")
    pdf_path = os.path.join(REPORT_DIR, f"{job_id}.pdf")

    file.save(csv_path)

    # Generate HTML report
    generate_report(csv_path, html_path)

    # Store paths for PDF step
    with open(f"{REPORT_DIR}/{job_id}.meta", "w") as f:
        f.write(html_path)

    # Return preview page
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    preview_page = f"""
    <html>
      <head>
        <title>TaxLabs Preview</title>
        <style>
          body {{
            margin: 0;
            background: #020617;
            color: #e5e7eb;
            font-family: system-ui;
          }}
          .top {{
            position: sticky;
            top: 0;
            background: #020617;
            padding: 16px;
            border-bottom: 1px solid #1f2937;
            text-align: center;
          }}
          button {{
            padding: 12px 24px;
            font-size: 16px;
            background: #0ea5e9;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
          }}
          iframe {{
            width: 100%;
            height: calc(100vh - 72px);
            border: none;
            background: white;
          }}
        </style>
      </head>
      <body>
        <div class="top">
          <form action="/download-pdf" method="POST">
            <input type="hidden" name="job_id" value="{job_id}">
            <button type="submit">Download PDF</button>
          </form>
        </div>
        <iframe srcdoc="{html_content.replace('"', '&quot;')}"></iframe>
      </body>
    </html>
    """

    return render_template_string(preview_page)


@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    job_id = request.form.get("job_id")
    if not job_id:
        return "Missing job id", 400

    html_path = os.path.join(REPORT_DIR, f"{job_id}.html")
    pdf_path = os.path.join(REPORT_DIR, f"{job_id}.pdf")

    if not os.path.exists(html_path):
        return "Report not found", 404

    generate_pdf(html_path, pdf_path)

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="TaxLabs_Report.pdf"
    )
