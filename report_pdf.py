from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from bs4 import BeautifulSoup

def generate_pdf(html_path, output_pdf_path="TaxLabs_Report.pdf"):
    styles = getSampleStyleSheet()
    story = []

    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")

    for tag in soup.find_all(["h1", "p"]):
        text = tag.get_text(strip=True)
        if text:
            story.append(Paragraph(text, styles["Normal"]))

    doc = SimpleDocTemplate(output_pdf_path)
    doc.build(story)

    return output_pdf_path
