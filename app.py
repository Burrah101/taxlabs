from flask import Flask, request, send_file, jsonify
import traceback
import io
import pandas as pd

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        email = request.form.get('email')

        if not file:
            return jsonify({"error": "No file provided"}), 400

        # 🔥 FIX is here: read uploaded CSV from file stream, not from path
        df = pd.read_csv(file.stream)

        # 🔄 Your existing processing logic
        from report_pdf import generate_pdf
        pdf_buffer = generate_pdf(df, email)

        # 🧪 Email logic (optional, safe fallback if fails)
        try:
            from send_email import send_email_with_pdf
            if email:
                send_email_with_pdf(email, pdf_buffer)
        except Exception as email_error:
            print("Email error:", email_error)

        pdf_buffer.seek(0)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='TaxLabs_Report.pdf'
        )

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": "Processing failed", "details": str(e)}), 500

