from pathlib import Path
from reportlab.pdfgen import canvas

PDF_PATH = Path(__file__).parent / 'hello.pdf'
PDF_FD = PDF_PATH.open('w+b')

canvas = canvas.Canvas(PDF_FD)

canvas.drawString(100, 100, 'Hello World')
canvas.showPage()
canvas.save()
