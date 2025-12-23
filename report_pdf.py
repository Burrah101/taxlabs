from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generate_pdf():
    """
    Generates a simple PDF with a thank-you message for the user.
    Saves it to static/report_TIMESTAMP.pdf and returns the file path.
    """
    # Make sure static/ folder exists
    os.makedirs("static", exist_ok=True)

    # Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"static/report_{timestamp}.pdf"

    # Create PDF canvas
    c = canvas.Canvas(file_path)
    c.drawString(100, 750, "✅ This is your Tax Report PDF!")
    c.drawString(100, 730, "🧾 Thank you for using TaxLabs.io × Boost.Global")
    c.drawString(100, 710, "Generated securely with Python + Stripe 💻")
    c.save()

    print(f"📄 PDF generated at: {file_path}")
    return file_path
