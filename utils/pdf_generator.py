# utils/pdf_generator.py
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Custom Flowable to draw the timeline connectors
class TimelineNode(Flowable):
    def __init__(self, color, height_offset=35):
        Flowable.__init__(self)
        self.color = color
        self.height_offset = height_offset
        self.width = 12
        self.height = 12

    def draw(self):
        self.canv.saveState()
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(1.5)
        self.canv.line(6, -self.height_offset, 6, 20)
        self.canv.setFillColor(self.color)
        self.canv.circle(6, 4, 3.5, fill=1, stroke=1)
        self.canv.restoreState()

# Draw the luxury top-left triangle
def draw_first_page_bg(canvas, doc):
    canvas.saveState()
    accent_color = colors.HexColor("#8c7a6b") # Matching Warm Taupe Accents
    canvas.setFillColor(accent_color)
    
    path = canvas.beginPath()
    path.moveTo(0, 792)
    path.lineTo(190, 792)
    path.lineTo(0, 680)
    path.close()
    
    canvas.drawPath(path, fill=True, stroke=False)
    canvas.restoreState()

def generate_resume_pdf(
    name, role, email, phone, summary, skills, experience, education, projects, theme_color, template, profile_file=None
):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    story = []
    styles = getSampleStyleSheet()
    
    # Warm Luxury Palette
    primary_color = colors.HexColor("#8c7a6b") # Luxury Warm Taupe
    neutral_dark = colors.HexColor("#2c2523")  # Warm Charcoal / Espresso
    text_muted = colors.HexColor("#6e625f")    # Soft warm clay
    line_gray = colors.HexColor("#e6dfd9")     # Sand Clay borders

    # Typography Styling Setup
    style_name = ParagraphStyle(
        'ResName', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=neutral_dark, spaceAfter=4
    )
    
    style_role = ParagraphStyle(
        'ResRole', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=15,
        textColor=primary_color, spaceAfter=6
    )

    style_sidebar_name = ParagraphStyle(
        'SidebarName', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=20, leading=24,
        textColor=primary_color, alignment=1, spaceAfter=3
    )

    style_sidebar_role = ParagraphStyle(
        'SidebarRole', parent=styles['Normal'],
        fontName='Helvetica', fontSize=11, leading=14,
        textColor=text_muted, alignment=1, spaceAfter=15
    )

    style_sidebar_heading = ParagraphStyle(
        'SidebarHeading', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=neutral_dark, spaceAfter=6
    )

    style_section_heading = ParagraphStyle(
        'SectionHeading', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=15,
        textColor=neutral_dark, spaceAfter=6, keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13.5,
        textColor=text_muted
    )

    style_bullet = ParagraphStyle(
        'BulletStyle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=text_muted, leftIndent=10, firstLineIndent=-8, spaceAfter=2
    )

    def parse_items(text):
        return [item.strip() for item in text.split('\n') if item.strip()]

    def get_parsed_flowables(text):
        flowables = []
        if not text:
            return flowables
        for line in text.split('\n'):
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith('-') or line_str.startswith('•') or line_str.startswith('*'):
                flowables.append(Paragraph(f"&bull; {line_str.lstrip('-•* ').strip()}", style_bullet))
            else:
                flowables.append(Paragraph(line_str, style_body))
        return flowables


    # ==================== RENDER LAYOUTS ====================

    if template == "Luxury Sidebar Timeline":
        left_side = [Spacer(1, 100)]
        left_side.append(Paragraph(name if name else "Candidate Name", style_sidebar_name))
        left_side.append(Paragraph(role if role else "Your Role", style_sidebar_role))

        left_side.append(Paragraph("Contact", style_sidebar_heading))
        left_side.append(HRFlowable(width="100%", thickness=1, color=line_gray, spaceAfter=8))
        left_side.append(Paragraph(f"<b>Phone:</b> {phone}", style_body))
        left_side.append(Paragraph(f"<b>Email:</b> {email}", style_body))
        left_side.append(Spacer(1, 15))

        if summary:
            left_side.append(Paragraph("About Me", style_sidebar_heading))
            left_side.append(HRFlowable(width="100%", thickness=1, color=line_gray, spaceAfter=8))
            left_side.append(Paragraph(summary, style_body))
            left_side.append(Spacer(1, 15))

        if skills:
            left_side.append(Paragraph("Skills", style_sidebar_heading))
            left_side.append(HRFlowable(width="100%", thickness=1, color=line_gray, spaceAfter=8))
            for s in skills.split(','):
                if s.strip():
                    left_side.append(Paragraph(f"&bull; {s.strip()}", style_body))

        right_side = [Spacer(1, 15)]

        if education:
            right_side.append(Paragraph("Education", style_section_heading))
            right_side.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=10))
            for entry in parse_items(education):
                parts = entry.split('|')
                title_text = parts[0].strip()
                desc_text = parts[1].strip() if len(parts) > 1 else ""
                entry_content = [
                    Paragraph(f"<b>{title_text}</b>", style_section_heading),
                    Paragraph(desc_text, style_body),
                    Spacer(1, 6)
                ]
                item_table = Table([[TimelineNode(primary_color), entry_content]], colWidths=[15, 335])
                item_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0)]))
                right_side.append(item_table)
            right_side.append(Spacer(1, 10))

        if experience:
            right_side.append(Paragraph("Experience", style_section_heading))
            right_side.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=10))
            for entry in parse_items(experience):
                parts = entry.split('|')
                title_text = parts[0].strip()
                desc_text = parts[1].strip() if len(parts) > 1 else ""
                entry_content = [
                    Paragraph(f"<b>{title_text}</b>", style_section_heading),
                    Paragraph(desc_text, style_body),
                    Spacer(1, 6)
                ]
                item_table = Table([[TimelineNode(primary_color), entry_content]], colWidths=[15, 335])
                item_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0)]))
                right_side.append(item_table)
            right_side.append(Spacer(1, 10))

        if projects:
            right_side.append(Paragraph("Personal Projects", style_section_heading))
            right_side.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=10))
            for i, proj in enumerate(parse_items(projects), 1):
                right_side.append(Paragraph(f"<b>{i}. {proj}</b>", style_body))
                right_side.append(Spacer(1, 5))

        master_table = Table([[left_side, right_side]], colWidths=[180, 360])
        master_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('RIGHTPADDING', (0,0), (0,0), 12),
            ('LEFTPADDING', (1,0), (1,0), 12),
            ('LINEAFTER', (0,0), (0,0), 0.5, line_gray),
        ]))
        story.append(master_table)
        doc.build(story, onFirstPage=draw_first_page_bg)

    elif template == "Executive Monospace":
        style_centered_name = ParagraphStyle('CenterName', parent=style_name, alignment=1)
        style_centered_role = ParagraphStyle('CenterRole', parent=style_role, alignment=1)
        style_centered_contact = ParagraphStyle('CenterContact', parent=style_body, alignment=1, textColor=text_muted)

        story.append(Paragraph(name if name else "Candidate Name", style_centered_name))
        story.append(Paragraph(role if role else "Target Job Role", style_centered_role))
        story.append(Paragraph(f"Email: {email}   |   Phone: {phone}", style_centered_contact))
        story.append(Spacer(1, 15))
        story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=15))

        if summary:
            story.append(Paragraph("PROFESSIONAL SUMMARY", style_section_heading))
            story.append(HRFlowable(width="100%", thickness=0.5, color=line_gray, spaceAfter=6))
            story.append(Paragraph(summary, style_body))
            story.append(Spacer(1, 15))

        if experience:
            story.append(Paragraph("CHRONOLOGICAL WORK EXPERIENCE", style_section_heading))
            story.append(HRFlowable(width="100%", thickness=0.5, color=line_gray, spaceAfter=6))
            for entry in parse_items(experience):
                story.extend(get_parsed_flowables(entry))
                story.append(Spacer(1, 8))
            story.append(Spacer(1, 10))

        if education:
            story.append(Paragraph("EDUCATION HISTORY", style_section_heading))
            story.append(HRFlowable(width="100%", thickness=0.5, color=line_gray, spaceAfter=6))
            for entry in parse_items(education):
                story.extend(get_parsed_flowables(entry))
                story.append(Spacer(1, 8))
            story.append(Spacer(1, 10))

        if projects:
            story.append(Paragraph("KEY PROJECT DEPLOYMENTS", style_section_heading))
            story.append(HRFlowable(width="100%", thickness=0.5, color=line_gray, spaceAfter=6))
            for i, proj in enumerate(parse_items(projects), 1):
                story.append(Paragraph(f"<b>{i}. {proj}</b>", style_body))
                story.append(Spacer(1, 4))

        doc.build(story)

    elif template == "Modern Minimalist":
        left_side = []
        right_side = []

        left_side.append(Paragraph(name if name else "Candidate Name", style_name))
        left_side.append(Paragraph(role if role else "Your Role", style_role))
        left_side.append(Spacer(1, 15))

        left_side.append(Paragraph("Contact Details", style_section_heading))
        left_side.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceAfter=6))
        left_side.append(Paragraph(f"Email: {email}", style_body))
        left_side.append(Paragraph(f"Phone: {phone}", style_body))
        left_side.append(Spacer(1, 15))

        if skills:
            left_side.append(Paragraph("Technical Stack", style_section_heading))
            left_side.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceAfter=6))
            for s in skills.split(','):
                left_side.append(Paragraph(f"&bull; {s.strip()}", style_body))

        if summary:
            right_side.append(Paragraph("EXECUTIVE STATEMENT", style_section_heading))
            right_side.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceAfter=6))
            right_side.append(Paragraph(summary, style_body))
            right_side.append(Spacer(1, 15))

        if experience:
            right_side.append(Paragraph("PROFESSIONAL HISTORY", style_section_heading))
            right_side.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceAfter=6))
            for exp in parse_items(experience):
                right_side.extend(get_parsed_flowables(exp))
                right_side.append(Spacer(1, 8))
            right_side.append(Spacer(1, 15))

        if education:
            right_side.append(Paragraph("ACADEMIC CREDENTIALS", style_section_heading))
            right_side.append(HRFlowable(width="100%", thickness=1.2, color=primary_color, spaceAfter=6))
            for edu in parse_items(education):
                right_side.extend(get_parsed_flowables(edu))
                right_side.append(Spacer(1, 8))

        master_table = Table([[left_side, right_side]], colWidths=[180, 360])
        master_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('RIGHTPADDING', (0,0), (0,0), 12),
            ('LEFTPADDING', (1,0), (1,0), 12),
        ]))
        story.append(master_table)
        doc.build(story)

    else:  # Tech Split Banner
        banner_data = [
            [Paragraph(name if name else "Candidate Name", style_name), ""],
            [Paragraph(role if role else "Your Role", style_role), Paragraph(f"Phone: {phone}<br/>Email: {email}", style_body)]
        ]
        banner_table = Table(banner_data, colWidths=[360, 180])
        banner_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LINEBELOW', (0,1), (-1,1), 1.5, primary_color),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(banner_table)
        story.append(Spacer(1, 15))

        left_side = []
        right_side = []

        if summary:
            left_side.append(Paragraph("Summary Statement", style_section_heading))
            left_side.append(Paragraph(summary, style_body))
            left_side.append(Spacer(1, 15))

        if skills:
            left_side.append(Paragraph("Core Proficiencies", style_section_heading))
            skills_list = [s.strip() for s in skills.split(',') if s.strip()]
            left_side.append(Paragraph(", ".join(skills_list), style_body))
            left_side.append(Spacer(1, 15))

        if projects:
            left_side.append(Paragraph("Selected Projects", style_section_heading))
            for i, proj in enumerate(parse_items(projects), 1):
                left_side.append(Paragraph(f"<b>{i}. {proj}</b>", style_body))

        if experience:
            right_side.append(Paragraph("Professional Experience", style_section_heading))
            for exp in parse_items(experience):
                right_side.extend(get_parsed_flowables(exp))
                right_side.append(Spacer(1, 10))
            right_side.append(Spacer(1, 15))

        if education:
            right_side.append(Paragraph("Education History", style_section_heading))
            for edu in parse_items(education):
                right_side.extend(get_parsed_flowables(edu))
                right_side.append(Spacer(1, 10))

        master_table = Table([[left_side, right_side]], colWidths=[250, 290])
        master_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('RIGHTPADDING', (0,0), (0,0), 15),
            ('LEFTPADDING', (1,0), (1,0), 15),
        ]))
        story.append(master_table)
        doc.build(story)

    buffer.seek(0)
    return buffer.getvalue()