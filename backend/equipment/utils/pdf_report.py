from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

def generate_pdf(history):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Equipment Analysis Report")

    c.setFont("Helvetica", 12)
    y = 760
    c.drawString(50, y, f"File: {history.filename}")
    y -= 30
    c.drawString(50, y, f"Total Equipment: {history.total_equipment}")
    y -= 20
    c.drawString(50, y, f"Avg Flowrate: {history.avg_flowrate}")
    y -= 20
    c.drawString(50, y, f"Avg Pressure: {history.avg_pressure}")
    y -= 20
    c.drawString(50, y, f"Avg Temperature: {history.avg_temperature}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
