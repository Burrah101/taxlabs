from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER
from bs4 import BeautifulSoup


def generate_pdf(html_path, pdf_path):
    doc = SimpleDocTemplate(pdf_path, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    for tag in soup.find_all(["h1", "h3", "p", "td"]):
        text = tag.get_text(strip=True)
        if text:
            story.append(Paragraph(text, styles["Normal"]))

    doc.build(story)
