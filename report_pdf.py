# report_pdf.py

from reportlab.pdfgen import canvas
import os

def generate_pdf(file_path="static/report.pdf"):
    """
    Generates a simple PDF with a thank-you message for the user.
    Saves it to the given file path.
    """
    # Create PDF canvas
    c = canvas.Canvas(file_path)

    # Draw text on PDF
    c.drawString(100, 750, "✅ This is your Tax Report PDF!")
    c.drawString(100, 730, "🧾 Thank you for using TaxLabs.")
    c.drawString(100, 710, "Generated securely with Python + Stripe 💻")

    # Save PDF
    c.save()
    print(f"📄 PDF generated at: {file_path}")
