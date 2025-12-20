from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime

def generate_pdf(user_data, filename="tax_report.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, height - 72, "Tax Report")

    # Subtitle
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 100, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # User Data
    c.drawString(72, height - 130, "User Details:")
    y = height - 150
    for key, value in user_data.items():
        c.drawString(80, y, f"{key}: {value}")
        y -= 20

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(72, 40, "This report is auto-generated. Contact support for corrections.")

    c.save()
    return filename
