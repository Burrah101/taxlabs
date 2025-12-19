from flask import Flask, request, send_file, jsonify
import pandas as pd
from io import BytesIO
import traceback
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>TaxLabs</h1>
    <p>Upload your CSV to generate your crypto report.</p>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".csv" required />
        <button type="submit">Upload CSV → Download PDF</button>
    </form>
    """

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        df = pd.read_csv(file)
        pdf_buffer = BytesIO()
        generate_pdf(df, pdf_buffer)
        pdf_buffer.seek(0)

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

def generate_pdf(df, buffer):
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []

    story.append(Paragraph("TaxLabs — Crypto Tax Checkup", style=style("h1")))
    story.append(Spacer(1, 12))

    # Summary stats
    total = len(df)
    net_usd = int(df['usd_value'].sum()) if 'usd_value' in df.columns else 0
    story.append(Paragraph(f"Total Transactions: {total}", style=style("normal")))
    story.append(Paragraph(f"Net USD Value: ${net_usd}", style=style("normal")))
    story.append(Spacer(1, 12))

    # Table of first 5 rows
    if not df.empty:
        columns = df.columns.tolist()
        data = [columns] + df.head(10).values.tolist()
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
            ('ALIGN',(0,0),(-1,-1),'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND',(0,1),(-1,-1),colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        story.append(table)

    doc.build(story)

def style(name):
    from reportlab.lib.styles import getSampleStyleSheet
    styles = getSampleStyleSheet()
    return styles["Heading1"] if name == "h1" else styles["Normal"]

if __name__ == "__main__":
    app.run(debug=True)
