from flask import Flask, request, send_file, jsonify, Response
import os, uuid, smtplib
from email.message import EmailMessage

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


def send_email(to_email, pdf_path):
    msg = EmailMessage()
    msg["Subject"] = "Your TaxLabs Crypto Tax Report"
    msg["From"] = os.environ["EMAIL_USER"]
    msg["To"] = to_email

    msg.set_content("Attached is your TaxLabs crypto tax summary PDF.")

    with open(pdf_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="TaxLabs_Report.pdf"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(
            os.environ["EMAIL_USER"],
            os.environ["EMAIL_PASS"]
        )
        server.send_message(msg)


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    email = request.form.get("email")

    uid = str(uuid.uuid4())
    csv_path = os.path.join(UPLOAD_DIR, f"{uid}.csv")
    html_path = os.path.join(REPORT_DIR, f"{uid}.html")
    pdf_path = os.path.join(REPORT_DIR, f"{uid}.pdf")

    file.save(csv_path)

    try:
        generate_report(csv_path, html_path)
        generate_pdf(html_path, pdf_path)

        if email:
            send_email(email, pdf_path)

    except Exception as e:
        return jsonify({"error": "Processing failed", "details": str(e)}), 500

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="TaxLabs_Report.pdf",
        mimetype="application/pdf"
    )
