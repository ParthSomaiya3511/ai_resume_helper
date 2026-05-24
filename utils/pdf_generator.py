from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus.tables import Table, TableStyle


def generate_resume_pdf(
    name,
    email,
    phone,
    skills,
    experience,
    education
):

    doc = SimpleDocTemplate(
        "resume.pdf",
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=20
    )

    styles = getSampleStyleSheet()

    elements = []

    # HEADER

    title = Paragraph(
        f"""
        <font size=24>
        <b>{name}</b>
        </font>
        """,
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 10))

    # CONTACT

    contact = Paragraph(
        f"""
        <font size=11>
        📧 {email} &nbsp;&nbsp;&nbsp;
        📱 {phone}
        </font>
        """,
        styles['BodyText']
    )

    elements.append(contact)

    elements.append(Spacer(1, 20))

    # SKILLS SECTION

    skills_title = Paragraph(
        "<b><font size=16 color='blue'>Skills</font></b>",
        styles['Heading2']
    )

    elements.append(skills_title)

    skills_text = Paragraph(
        skills,
        styles['BodyText']
    )

    elements.append(skills_text)

    elements.append(Spacer(1, 15))

    # EXPERIENCE

    exp_title = Paragraph(
        "<b><font size=16 color='blue'>Experience</font></b>",
        styles['Heading2']
    )

    elements.append(exp_title)

    exp_text = Paragraph(
        experience,
        styles['BodyText']
    )

    elements.append(exp_text)

    elements.append(Spacer(1, 15))

    # EDUCATION

    edu_title = Paragraph(
        "<b><font size=16 color='blue'>Education</font></b>",
        styles['Heading2']
    )

    elements.append(edu_title)

    edu_text = Paragraph(
        education,
        styles['BodyText']
    )

    elements.append(edu_text)

    elements.append(Spacer(1, 20))

    # FOOTER LINE

    table = Table(
        [["AI Resume Helper"]],
        colWidths=[500]
    )

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#2563eb")),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
    ]))

    elements.append(table)

    # BUILD PDF

    doc.build(elements)