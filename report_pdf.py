from reportlab.pdfgen import canvas

def generate_pdf(df, buffer):
    c = canvas.Canvas(buffer)
    c.drawString(100, 800, "Tax Report Summary")

    y = 750
    for index, row in df.iterrows():
        line = f"{row['date']} | {row['type']} | {row['asset']} | ${row['usd_value']}"
        c.drawString(100, y, line)
        y -= 20

    c.save()  # ✅ Must close the canvas
