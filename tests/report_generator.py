from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf_report(audit):
    os.makedirs("reports", exist_ok=True)

    filename = f"reports/audit_{audit['model_name']}.pdf"

    c = canvas.Canvas(filename, pagesize=letter)

    c.drawString(100, 750, f"AI AUDIT REPORT")
    c.drawString(100, 720, f"Model: {audit['model_name']}")
    c.drawString(100, 700, f"Language Score: {audit['language_score']}")
    c.drawString(100, 680, f"Instruction Score: {audit['instruction_score']}")
    c.drawString(100, 660, f"Boundary Score: {audit['boundary_score']}")
    c.drawString(100, 640, f"Overall Score: {audit['overall_score']}")
    c.drawString(100, 620, f"Status: {audit['status']}")

    c.save()

    return filename