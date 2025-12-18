from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from bs4 import BeautifulSoup

def generate_pdf(html_path, output_pdf_path="TaxLabs_Report.pdf"):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_pdf_path)
    story = []

    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "lxml")  # 🔥 parser now exists

    for tag in soup.find_all(["h1", "h3", "p", "td"]):
        text = tag.get_text(strip=True)
        if text:
            story.append(Paragraph(text, styles["Normal"]))
            story.append(Spacer(1, 12))

    doc.build(story)
    return output_pdf_path
