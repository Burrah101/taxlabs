from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_pdf(df, buffer):
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50  # Start near top
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "TaxLabs — Crypto Tax Checkup")
    y -= 25

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Total transactions reviewed: {len(df)}")
    y -= 30

    for i, row in df.iterrows():
        line = f"{row['type']}: {row['asset']} — {row['amount']} @ ${row['usd_value']}"
        c.drawString(50, y, line)
        y -= 15

        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
