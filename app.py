import os
import smtplib
from flask import Flask, request, send_file
from email.message import EmailMessage
from report_html import generate_report
from report_pdf import generate_pdf

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400

    file = request.files["file"]
    email = request.form.get("email")

    if file.filename == "":
        return {"error": "Empty filename"}, 400

    os.makedirs("uploads", exist_ok=True)
    csv_path = os.path.join("uploads", file.filename)
    file.save(csv_path)

    # Generate reports
    html_path = generate_report(csv_path)
    pdf_path = generate_pdf(html_path)

    # 🔹 EMAIL (SAFE, NON-BLOCKING)
    if email:
        try:
            msg = EmailMessage()
            msg["Subject"] = "Your TaxLabs Crypto Report"
            msg["From"] = os.environ["EMAIL_FROM"]
            msg["To"] = email
            msg.set_content(
                "Attached is your TaxLabs crypto tax summary.\n\n"
                "This is for informational clarity only."
            )

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

        except Exception as e:
            # Email failure must NEVER break PDF
            print("Email skipped:", e)

    # 🔹 PDF ALWAYS RETURNS
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name="TaxLabs_Report.pdf"
    )
