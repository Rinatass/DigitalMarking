import qrcode
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from django.conf import settings


def generate_pdf_with_codes(codes):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x = 20 * mm
    y = height - 40 * mm

    for code in codes:
        full_url = f"{settings.BASE_URL}/track/{code}/"

        qr_img = qrcode.make(full_url)
        qr_io = BytesIO()
        qr_img.save(qr_io, format='PNG')
        qr_io.seek(0)
        qr_reader = ImageReader(qr_io)

        c.drawImage(qr_reader, x, y, width=30*mm, height=30*mm)
        c.drawString(x + 35*mm, y + 10*mm, f"{full_url}")

        y -= 40 * mm
        if y < 40 * mm:
            c.showPage()
            y = height - 40 * mm

    c.save()
    buffer.seek(0)
    return buffer