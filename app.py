from flask import Flask, request, send_file, jsonify
import pandas as pd
from io import BytesIO
import traceback
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)

# Load environment variables
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASS = os.environ.get('EMAIL_PASS')
EMAIL_FROM = os.environ.get('EMAIL_FROM')


def generate_pdf(df, buffer):
    c = canvas.Canvas(buffer, pagesize=letter)
    textobject = c.beginText(50, 750)
    textobject.setFont("Helvetica", 12)

    textobject.textLine("TaxLabs — Crypto Tax Checkup")
    textobject.textLine(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d')}")
    textobject.textLine("")

    textobject.textLine(f"Total transactions reviewed: {len(df)}")
    textobject.textLine("")

    type_counts = df['type'].value_counts()
    for t, count in type_counts.items():
        textobject.textLine(f"{t}: {count}")

    c.drawText(textobject)
    c.showPage()
    c.save()


def send_email_with_pdf(to_email, pdf_bytes):
    msg = EmailMessage()
    msg['Subject'] = 'Your TaxLabs Crypto Report'
    msg['From'] = EMAIL_FROM
    msg['To'] = to_email
    msg.set_content("Attached is your crypto tax summary PDF report.")

    msg.add_attachment(
        pdf_bytes.getvalue(),
        maintype='application',
        subtype='pdf',
        filename='TaxLabs_Report.pdf'
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)


@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        df = pd.read_csv(file)

        # Generate PDF into memory
        pdf_buffer = BytesIO()
        generate_pdf(df, pdf_buffer)
        pdf_buffer.seek(0)

        # Optional email delivery
        to_email = request.form.get('email')
        if to_email and EMAIL_USER and EMAIL_PASS and EMAIL_FROM:
            try:
                send_email_with_pdf(to_email, pdf_buffer)
                print(f"Email sent to {to_email}")
            except Exception as e:
                print(f"Email error: {e}")

        # Return PDF to browser
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='TaxLabs_Report.pdf'
        )

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500


@app.route('/')
def index():
    return 'Backend is live. Use the UI to upload.'


if __name__ == '__main__':
    app.run()
