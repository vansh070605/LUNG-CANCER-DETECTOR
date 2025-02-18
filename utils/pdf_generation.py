from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf():
    c = canvas.Canvas("static/report.pdf", pagesize=letter)
    c.drawString(100, 750, "Lung Cancer Detection Report")
    c.drawString(100, 730, "Patient's Risk: High Risk")
    # Add other details here
    c.save()
