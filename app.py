import os
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename

from report_html import generate_report
from report_pdf import generate_pdf

# Optional email
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def send_email_with_pdf(to_email, pdf_path):
    """Send email WITHOUT breaking the app if it fails"""
    try:
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        email_from = os.getenv("EMAIL_FROM", email_user)

        if not email_user or not email_pass:
            print("⚠️ Email skipped: missing EMAIL_USER or EMAIL_PASS")
            return

        msg = EmailMessage()
        msg["Subject"] = "Your TaxLabs Crypto Report"
        msg["From"] = email_from
        msg["To"] = to_email
        msg.set_content(
            "Your TaxLabs crypto tax report is attached.\n\n— TaxLabs"
        )

        with open(pdf_path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename=os.path.basename(pdf_path),
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email_user, email_pass)
            server.send_message(msg)

        print("📧 Email sent to", to_email)

    except Exception as e:
        # CRITICAL: NEVER crash the app
        print("❌ Email failed:", str(e))


@app.route("/")
def health():
    return "TaxLabs backend is running"


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    email = request.form.get("email")

    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    csv_path = os.path.join(UPLOAD_DIR, filename)
    file.save(csv_path)

    try:
        # Generate HTML + PDF
        html_path = generate_report(csv_path)
        pdf_path = generate_pdf(html_path)

        # Email is OPTIONAL and SAFE
        if email:
            send_email_with_pdf(email, pdf_path)

        # ALWAYS return the PDF
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name="TaxLabs_Report.pdf",
        )

    except Exception as e:
        print("❌ Processing failed:", str(e))
        return jsonify({"error": "Processing failed", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
