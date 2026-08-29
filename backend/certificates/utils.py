from io import BytesIO

from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas


def generate_certificate_pdf(certificate):

    if not certificate.certificate_id:
        certificate.save()

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=(595, 842),
    )

    # ==================================================
    # PDF METADATA
    # ==================================================

    pdf.setTitle(
        f"Python Academy - Certificate of Completion - "
        f"{certificate.course.title}"
    )

    pdf.setAuthor("Python Academy")

    pdf.setSubject(
        f"Certificate of Completion - {certificate.course.title}"
    )

    pdf.setCreator("Python Academy")

    # ==================================================
    # CERTIFICATE CONTENT
    # ==================================================

    pdf.setFont("Helvetica-Bold", 24)

    pdf.drawCentredString(
        300,
        760,
        "PYTHON ACADEMY",
    )

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawCentredString(
        300,
        710,
        "Certificate of Completion",
    )

    pdf.setFont("Helvetica", 14)

    pdf.drawCentredString(
        300,
        650,
        "This certifies that",
    )

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawCentredString(
        300,
        620,
        certificate.user.get_full_name()
        or certificate.user.username,
    )

    pdf.setFont("Helvetica", 14)

    pdf.drawCentredString(
        300,
        580,
        "has successfully completed",
    )

    pdf.setFont("Helvetica-Bold", 18)

    pdf.drawCentredString(
        300,
        550,
        certificate.course.title,
    )

    # ==================================================
    # CERTIFICATE DETAILS
    # ==================================================

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        120,
        f"Certificate ID : {certificate.certificate_id}",
    )

    pdf.drawString(
        50,
        100,
        f"Issue Date : "
        f"{certificate.issued_at.strftime('%d-%m-%Y')}",
    )

    # ==================================================
    # SAVE PDF
    # ==================================================

    pdf.showPage()
    pdf.save()

    pdf_data = buffer.getvalue()

    buffer.close()

    certificate.pdf.save(
        f"{certificate.certificate_id}.pdf",
        ContentFile(pdf_data),
        save=True,
    )

    return certificate