# pages/resume_builder.py
import streamlit as st
import base64
import textwrap
from utils.pdf_generator import generate_resume_pdf
from utils.theme_injector import apply_global_styles

st.set_page_config(layout="wide", page_title="Premium Resume Builder", page_icon="📝")
apply_global_styles()

# Base64 image converter to avoid server storage issues
def get_base64_image(image_file):
    if image_file is not None:
        return f"data:image/png;base64,{base64.b64encode(image_file.getvalue()).decode()}"
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#94a3b8" width="60" height="60">
        <circle cx="12" cy="8" r="4"/><path d="M12 14c-6.1 0-8 4-8 4v2h16v-2s-1.9-4-8-4z"/>
    </svg>"""
    return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode()).decode()}"

st.title("📝 Premium Resume Builder")
st.caption("Design, configure, and download clean corporate resume sheets instantly.")

left_col, right_col = st.columns([1.1, 1], gap="large")

with left_col:
    st.subheader("Structure & Data")
    
    tab_design, tab_personal, tab_experience, tab_skills = st.tabs([
        "🎨 Style Theme", 
        "👤 Identity Details", 
        "💼 Experience & Academics", 
        "🛠 Skills & Projects"
    ])
    
    with tab_design:
        col_theme, col_temp = st.columns([1, 2])
        with col_theme:
            theme_color = st.color_picker("Accent Theme Color", "#4a779d")
        with col_temp:
            template = st.selectbox(
                "Choose Structure Style", 
                ["Luxury Sidebar Timeline", "Executive Monospace", "Modern Minimalist", "Tech Split Banner"]
            )
        profile_upload = st.file_uploader("Upload Headshot (JPG/PNG)", type=["png", "jpg", "jpeg"])

    with tab_personal:
        name = st.text_input("Full Name", value="Parth Somaiya")
        role = st.text_input("Target Job Title", value="Web Developer")
        email = st.text_input("Email Address", value="parthsomaiya2004@gmail.com")
        phone = st.text_input("Phone Number", value="9104244421")
        summary = st.text_area("About Me", value="Completed B.C.A. from Atmiya University and seeking an opportunity to start my career and enhance my skills.", height=120)

    with tab_experience:
        experience = st.text_area(
            "Experience (Format: Title - Company | Description)", 
            value="Web designer - Codizious Technologies | Designed and developed responsive web applications.\nLaravel Intern - Omega Infoway | Maintained backend functionality using PHP and Laravel.",
            height=150
        )
        education = st.text_area(
            "Education (Format: Degree - University | Description)", 
            value="Bachelor of Computer Applications - Atmiya University | 2022 - 2025. Emphasizes modern development frameworks.\nWeb Developer Training - Codizious Technologies | 04/2025 - 09/2025. Focused on HTML, CSS, PHP.",
            height=120
        )

    with tab_skills:
        skills = st.text_input("Core Skills (Comma Separated)", value="Web Design, PHP, WordPress, Laravel, SEO")
        projects = st.text_area(
            "Personal Projects (One per line)",
            value="Restaurant Management System Website in PHP.\nMadras Café Website in WordPress with elementor.\nNextGen Mobiles Store in WordPress.\nFitness Gym Website in Laravel.",
            height=120
        )

    st.write("---")
    if st.button("🚀 Prepare PDF for Download", use_container_width=True):
        try:
            pdf_data = generate_resume_pdf(
                name=name, role=role, email=email, phone=phone, summary=summary,
                skills=skills, experience=experience, education=education,
                projects=projects, theme_color=theme_color, template=template, profile_file=profile_upload
            )
            
            st.success("PDF compiled successfully!")
            st.download_button(
                label="⬇ Download Professional PDF",
                data=pdf_data,
                file_name=f"{name.replace(' ', '_')}_Resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Failed to generate PDF: {e}")

# Live preview matches the premium light theme output
with right_col:
    st.subheader("Live View Workspace")
    img_b64 = get_base64_image(profile_upload)
    
    # 1. Parse Skills to HTML Tags
    skill_tags = [f'<span class="skill-tag">{s.strip()}</span>' for s in skills.split(',') if s.strip()]
    skill_html = "".join(skill_tags) if skill_tags else "<p>No skills listed</p>"
    
    # 2. Render Timeline Blocks
    def render_timeline(text_block):
        if not text_block: return ""
        items = text_block.split('\n')
        html_out = ""
        for item in items:
            it = item.strip()
            if not it: continue
            parts = it.split('|')
            title = parts[0].strip()
            desc = parts[1].strip() if len(parts) > 1 else ""
            html_out += f"""
            <div class="timeline-container">
                <div class="timeline-dot" style="background:{theme_color};"></div>
                <strong style="font-size: 0.95rem; color:#1e293b;">{title}</strong>
                <p style="margin: 2px 0; font-size:0.85rem; color:#475569; line-height:1.4;">{desc}</p>
            </div>
            """
        return html_out

    # 3. Render Basic List Blocks (For non-timeline designs)
    def render_basic_list(text_block):
        if not text_block: return ""
        items = text_block.split('\n')
        html_out = ""
        for item in items:
            it = item.strip()
            if not it: continue
            parts = it.split('|')
            title = parts[0].strip()
            desc = parts[1].strip() if len(parts) > 1 else ""
            html_out += f"""
            <div style="margin-bottom: 12px; border-left: 2px solid #e2e8f0; padding-left:10px;">
                <strong style="font-size: 0.95rem; color:#1e293b;">{title}</strong>
                <p style="margin: 2px 0; font-size:0.85rem; color:#475569; line-height:1.4;">{desc}</p>
            </div>
            """
        return html_out

    # 4. Render Project lists
    proj_lines = [p.strip() for p in projects.split('\n') if p.strip()]
    proj_html = "".join([f"<p style='margin: 4px 0; font-size:0.9rem;'><b>{i}.</b> {proj}</p>" for i, proj in enumerate(proj_lines, 1)])

    # Construct HTML preview layouts programmatically to eliminate f-string conflicts
    preview_html = ""

    if template == "Luxury Sidebar Timeline":
        preview_html = f"""
        <div class="preview-card" style="position: relative; overflow: hidden; padding: 0 !important; max-width: 100%;">
            <!-- Top-left geometric accent line -->
            <div style="position: absolute; top:0; left:0; width: 0; height: 0; border-top: 100px solid {theme_color}; border-right: 150px solid transparent; z-index:1;"></div>
            
            <table style="width:100%; border-collapse: collapse; z-index: 2; position: relative;">
                <tr style="vertical-align: top;">
                    <td style="width: 35%; padding: 120px 15px 25px 25px; border-right: 1px solid #cbd5e1; background: #fafafa;">
                        <h2 style="margin:0; font-size:1.6rem; color:#1e293b; text-align:center;">{name}</h2>
                        <p style="margin:4px 0 20px 0; color:{theme_color}; font-weight:500; font-size:0.95rem; text-align:center;">{role}</p>
                        
                        <h4 style="border-bottom: 1px solid #cbd5e1; padding-bottom:4px; font-size:0.9rem; margin-top:15px;">Contact</h4>
                        <p style="font-size: 0.8rem; margin:4px 0;"><b>Phone:</b><br>{phone}</p>
                        <p style="font-size: 0.8rem; margin:4px 0;"><b>Email:</b><br>{email}</p>
                        
                        <h4 style="border-bottom: 1px solid #cbd5e1; padding-bottom:4px; font-size:0.9rem; margin-top:20px;">About Me</h4>
                        <p style="font-size: 0.8rem; line-height:1.4; color:#475569;">{summary}</p>
                        
                        <h4 style="border-bottom: 1px solid #cbd5e1; padding-bottom:4px; font-size:0.9rem; margin-top:20px;">Skills</h4>
                        <div style="margin-top:5px;">{skill_html}</div>
                    </td>
                    <td style="width: 65%; padding: 40px 25px 25px 25px;">
                        <h3 style="color:#1e293b; margin:0 0 4px 0; font-size:1.1rem; border-bottom:2px solid {theme_color}; padding-bottom:4px;">🎓 Education</h3>
                        <div style="margin-top:10px;">{render_timeline(education)}</div>
                        
                        <h3 style="color:#1e293b; margin:20px 0 4px 0; font-size:1.1rem; border-bottom:2px solid {theme_color}; padding-bottom:4px;">💼 Experience</h3>
                        <div style="margin-top:10px;">{render_timeline(experience)}</div>
                        
                        <h3 style="color:#1e293b; margin:20px 0 4px 0; font-size:1.1rem; border-bottom:2px solid {theme_color}; padding-bottom:4px;">📋 Personal Projects</h3>
                        <div style="margin-top:10px; color:#475569;">{proj_html}</div>
                    </td>
                </tr>
            </table>
        </div>
        """
        
    elif template == "Executive Monospace":
        preview_html = f"""
        <div class="preview-card" style="padding: 30px !important; text-align: center; max-width: 100%;">
            <h1 style="margin:0; font-size:2.2rem; color:#1e293b; font-family:'Times New Roman', serif;">{name}</h1>
            <p style="color:{theme_color}; font-size:1rem; margin:4px 0; text-transform:uppercase; letter-spacing:1px;">{role}</p>
            <p style="font-size:0.85rem; color:#475569; margin-bottom:15px;">Email: {email} &nbsp;|&nbsp; Phone: {phone}</p>
            <hr style="border: 0; border-top: 1.5px solid {theme_color}; margin-bottom: 20px;">
            
            <div style="text-align: left;">
                <h4 style="color:#1e293b; font-size:1.05rem; margin-bottom:4px;">EXECUTIVE SUMMARY</h4>
                <p style="font-size:0.9rem; line-height:1.5; color:#475569; margin-bottom:15px;">{summary}</p>
                
                <h4 style="color:#1e293b; font-size:1.05rem; margin-bottom:4px; margin-top:20px;">CHRONOLOGICAL EXPERIENCE</h4>
                <div style="margin-bottom:15px;">{render_basic_list(experience)}</div>
                
                <h4 style="color:#1e293b; font-size:1.05rem; margin-bottom:4px; margin-top:20px;">EDUCATION</h4>
                <div style="margin-bottom:15px;">{render_basic_list(education)}</div>
                
                <h4 style="color:#1e293b; font-size:1.05rem; margin-bottom:4px; margin-top:20px;">PROJECT WORK</h4>
                <div>{proj_html}</div>
            </div>
        </div>
        """
        
    elif template == "Modern Minimalist":
        preview_html = f"""
        <div class="preview-card" style="padding: 30px !important; max-width: 100%;">
            <table style="width:100%; border-collapse: collapse;">
                <tr style="vertical-align: top;">
                    <td style="width: 35%; padding-right: 20px;">
                        <h2 style="margin:0; font-size:1.8rem; color:#1e293b;">{name}</h2>
                        <p style="color:{theme_color}; font-weight:500; font-size:0.95rem; margin-bottom:20px;">{role}</p>
                        
                        <h4 style="border-top:2px solid {theme_color}; padding-top:4px; font-size:0.95rem;">Contact Details</h4>
                        <p style="font-size: 0.85rem; margin:4px 0;">📧 {email}</p>
                        <p style="font-size: 0.85rem; margin:4px 0;">📱 {phone}</p>
                        
                        <h4 style="border-top:2px solid {theme_color}; padding-top:4px; font-size:0.95rem; margin-top:20px;">Skills</h4>
                        <div>{skill_html}</div>
                    </td>
                    <td style="width: 65%; padding-left: 20px; border-left:1px solid #cbd5e1;">
                        <h4 style="border-bottom:1.2px solid {theme_color}; padding-bottom:4px; font-size:1rem; margin:0 0 10px 0;">SUMMARY</h4>
                        <p style="font-size:0.9rem; line-height:1.5; color:#475569; margin-bottom:20px;">{summary}</p>
                        
                        <h4 style="border-bottom:1.2px solid {theme_color}; padding-bottom:4px; font-size:1rem; margin-top:20px;">WORK EXPERIENCE</h4>
                        <div>{render_basic_list(experience)}</div>
                        
                        <h4 style="border-bottom:1.2px solid {theme_color}; padding-bottom:4px; font-size:1rem; margin-top:20px;">ACADEMIC PROFILE</h4>
                        <div>{render_basic_list(education)}</div>
                    </td>
                </tr>
            </table>
        </div>
        """
        
    else:  # Tech Split Banner
        preview_html = f"""
        <div class="preview-card" style="padding: 0 !important; max-width: 100%;">
            <div style="background:#fafafa; padding:25px 30px; border-bottom: 2px solid {theme_color};">
                <table style="width:100%;">
                    <tr>
                        <td>
                            <h2 style="margin:0; font-size:2.0rem; color:#1e293b;">{name}</h2>
                            <p style="color:{theme_color}; font-weight:500; font-size:1rem; margin:4px 0 0 0;">{role}</p>
                        </td>
                        <td style="text-align: right; font-size: 0.85rem; color:#475569;">
                            Email: {email}<br>Phone: {phone}
                        </td>
                    </tr>
                </table>
            </div>
            
            <table style="width:100%; border-collapse: collapse; padding: 25px;">
                <tr style="vertical-align: top;">
                    <td style="width: 45%; padding: 25px 15px 25px 30px;">
                        <h4 style="color:#1e293b; margin-top:0;">Summary</h4>
                        <p style="font-size:0.9rem; line-height:1.4; color:#475569; margin-bottom:20px;">{summary}</p>
                        
                        <h4 style="color:#1e293b;">Key Competency</h4>
                        <div style="margin-bottom:20px;">{skill_html}</div>
                        
                        <h4 style="color:#1e293b;">Key Deployments</h4>
                        <div>{proj_html}</div>
                    </td>
                    <td style="width: 55%; padding: 25px 30px 25px 15px;">
                        <h4 style="color:#1e293b; margin-top:0;">Experience</h4>
                        <div>{render_basic_list(experience)}</div>
                        
                        <h4 style="color:#1e293b; margin-top:20px;">Education History</h4>
                        <div>{render_basic_list(education)}</div>
                    </td>
                </tr>
            </table>
        </div>
        """

    # Apply textwrap.dedent to ensure Markdown parser treats the block as HTML (not raw indented code)
    st.markdown(textwrap.dedent(preview_html), unsafe_allow_html=True)