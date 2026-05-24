from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

def generate_resume_pdf(
    name,
    role,
    email,
    phone,
    summary,
    skills,
    experience,
    education,
    certifications,
    theme
):

    doc = SimpleDocTemplate(
        "resume.pdf",
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        f"""
        <font size=24 color='{theme}'>
        <b>{name}</b>
        </font>
        """,
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1,15))

    contact = Paragraph(
        f"{role}<br/>{email}<br/>{phone}",
        styles['BodyText']
    )

    elements.append(contact)

    elements.append(Spacer(1,20))

    sections = [
        ("Summary",summary),
        ("Skills",skills),
        ("Experience",experience),
        ("Education",education),
        ("Certifications",certifications)
    ]

    for title_text,content in sections:

        heading = Paragraph(
            f"""
            <font size=16 color='{theme}'>
            <b>{title_text}</b>
            </font>
            """,
            styles['Heading2']
        )

        elements.append(heading)

        elements.append(
            Paragraph(
                content,
                styles['BodyText']
            )
        )

        elements.append(Spacer(1,15))

    doc.build(elements)