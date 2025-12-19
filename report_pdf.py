from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_pdf(df, buffer):
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40

    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y, "TaxLabs — Crypto Tax Summary")
    y -= 40

    c.setFont("Helvetica", 10)
    for index, row in df.iterrows():
        line = f"{row['date']} | {row['type']} | {row['asset']} | {row['amount']} | ${row['usd_value']}"
        c.drawString(72, y, line)
        y -= 20
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()
