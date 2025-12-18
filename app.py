from flask import Flask, request, send_file, jsonify, render_template
from io import BytesIO
from report_pdf import generate_pdf  # Your PDF generator
from werkzeug.utils import secure_filename
import os
import smtplib
from email.message import EmailMessage
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # ✅ Step 1: Get uploaded file
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # ✅ Step 2: Read file contents
        filename = secure_filename(file.filename)
        csv_data = file.read().decode('utf-8')

        # ✅ Step 3: Generate PDF in memory
        pdf_buffer = BytesIO()
        generate_pdf(csv_data, pdf_buffer)
        pdf_buffer.seek(0)

        # ✅ Step 4: Optional email sending
        email_to = request.form.get("email", "").strip()
        if email_to:
            msg = EmailMessage()
            msg['Subject'] = "Your Tax Report"
            msg['From'] = os.environ.get("EMAIL_FROM")
            msg['To'] = email_to
            msg.set_content("Here is your tax report PDF.")
            msg.add_attachment(pdf_buffer.getvalue(), maintype='application', subtype='pdf', filename="TaxLabs_Report.pdf")

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS"))
                smtp.send_message(msg)

            # Reset buffer position after sending email
            pdf_buffer.seek(0)

        # ✅ Step 5: Return PDF to browser
        return send_file(pdf_buffer, mimetype='application/pdf', as_attachment=True, download_name='TaxLabs_Report.pdf')

    except Exception as e:
        # 🔥 Catch and log full traceback
        print("===== EXCEPTION TRACEBACK START =====")
        print(traceback.format_exc())
        print("===== EXCEPTION TRACEBACK END =====")
        return jsonify({"error": "Processing failed", "details": str(e)}), 500
