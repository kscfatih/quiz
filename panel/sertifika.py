from django.http import FileResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .models import Sertifika
from io import BytesIO
from reportlab.lib.units import inch
def sertifika_pdf(request, sertifika_id):
    sertifika = Sertifika.objects.get(pk=sertifika_id)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(letter))
    img_path = 'static/background.jpg'
    img = ImageReader(img_path)
    p.drawImage(img, 0, 0, width=landscape(letter)[0], height=landscape(letter)[1])
    page_width, page_height = landscape(letter)

    font_name = "Helvetica-Bold"
    font_size = 19
    bottom_text_font_size = 35

    top_text = "THIS CERTIFICATE IS PROUDLY PRESENTED FOR HONORABLE ACHIEVEMENT TO"
    top_text_width = p.stringWidth(top_text, font_name, font_size)
    x_top_position = (page_width - top_text_width) / 2
    y_top_position = page_height / 2 + font_size

    bottom_text = sertifika.isim
    bottom_text_width = p.stringWidth(bottom_text, font_name, bottom_text_font_size)
    x_bottom_position = (page_width - bottom_text_width) / 2
    y_bottom_position = page_height / 2 - bottom_text_font_size

    p.setFont(font_name, font_size)
    p.drawString(x_top_position, y_top_position, top_text)
    p.setFont(font_name, bottom_text_font_size)  
    p.drawString(x_bottom_position, y_bottom_position, bottom_text)
    p.setFont(font_name, font_size)

    date_text = f"Date of Issue: {sertifika.issue_date}"
    date_text_width = p.stringWidth(date_text, font_name, font_size)
    x_date_position = (page_width - date_text_width) / 2
    p.drawString(x_date_position, y_bottom_position - 1.5*inch, date_text)

    p.save()

    buffer.seek(0)

    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="sertifika_{sertifika_id}.pdf"'

    return response