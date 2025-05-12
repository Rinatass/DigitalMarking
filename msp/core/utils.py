from io import BytesIO
from reportlab.pdfgen import canvas

def generate_pdf_with_codes(codes):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    y = 800
    for code in codes:
        p.drawString(100, y, f"Code: {code}")
        y -= 30
        if y < 100:
            p.showPage()
            y = 800
    p.save()
    buffer.seek(0)
    return buffer
