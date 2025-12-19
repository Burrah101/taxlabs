from reportlab.pdfgen import canvas

def generate_pdf(df, buffer):
    c = canvas.Canvas(buffer)
    c.setFont("Helvetica", 12)
    c.drawString(100, 800, "TaxLabs — Crypto Tax Summary")
    
    y = 780
    for index, row in df.iterrows():
        line = f"{row['date']} — {row['type']} — {row['asset']} — {row['amount']} — {row['usd_value']}"
        c.drawString(100, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = 800

    c.save()
