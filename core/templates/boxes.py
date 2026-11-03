"""
Technical Boxes CV Template.
Clean, modern engineering aesthetic:
- Rounded container boxes with soft borders and airy padding
- Rectangular photo with soft rounded corners on the top right
- Rounded section headers with crystal-clear typography (Plus Jakarta Sans / Inter)
- Plain text language proficiency (no sliders)
- Highly legible spacing and professional contrast
"""
from .base_template import BaseTemplate


class BoxesTemplate(BaseTemplate):
    """Modern rounded technical boxes grid template with high readability."""

    def build(self, output_path: str = "nowe_cv.html") -> str:
        photo_uri = self._photo_base64()
        if photo_uri:
            photo_html = f'<div class="bx-photo-wrap"><img src="{photo_uri}" alt="{self.esc(self.info.name)}" class="bx-photo"></div>'
        else:
            photo_html = (
                '<div class="bx-photo-wrap">'
                '<div class="bx-photo-empty">'
                '<svg class="bx-user-svg" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="1.6">'
                '<circle cx="12" cy="8" r="4"/>'
                '<path d="M4 20c0-4 4-6 8-6s8 2 8 6"/>'
                '</svg>'
                '</div>'
                '</div>'
            )

        info = self.info
        contact_parts = []
        if info.phone:
            contact_parts.append(f'<span class="bx-c-item">{self.ICO_PHONE} <a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a></span>')
        if info.email:
            contact_parts.append(f'<span class="bx-c-item">{self.ICO_MAIL} <a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a></span>')
        if info.location:
            contact_parts.append(f'<span class="bx-c-item">{self.ICO_PIN} <span>{self.esc(info.location)}</span></span>')
        if info.linkedin:
            lbl = info.linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_parts.append(f'<span class="bx-c-item">{self.ICO_LINKEDIN} <a href="{self.esc(info.linkedin)}" target="_blank">{self.esc(lbl)}</a></span>')
        if info.github:
            lbl = info.github.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_parts.append(f'<span class="bx-c-item">{self.ICO_GITHUB} <a href="{self.esc(info.github)}" target="_blank">{self.esc(lbl)}</a></span>')
        if info.driver_license:
            contact_parts.append(f'<span class="bx-c-item">{self.ICO_CAR} <span>Prawo jazdy: {self.esc(info.driver_license)}</span></span>')

        contact_bar = "".join(contact_parts)

        # Experience entries
        exp_rows = []
        for exp in self.data.experience:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in exp.description)
            comp_loc = self.esc(exp.company)
            if exp.location:
                comp_loc += f", {self.esc(exp.location)}"
            exp_rows.append(f"""
            <div class="bx-job-item">
                <div class="bx-job-meta">
                    <span class="bx-job-date">{self.esc(exp.period)}</span>
                    <span class="bx-job-comp">{comp_loc}</span>
                </div>
                <div class="bx-job-role">{self.esc(exp.role)}</div>
                <ul class="bx-dash-list">{bullets}</ul>
            </div>""")
        experience_html = "\n".join(exp_rows)

        # Startups
        st_rows = []
        for st in self.data.startups:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in st.description)
            st_rows.append(f"""
            <div class="bx-job-item">
                {f'<div class="bx-job-date">{self.esc(st.period)}</div>' if st.period else ''}
                <div class="bx-job-role">{self.esc(st.name)}</div>
                <ul class="bx-dash-list">{bullets}</ul>
            </div>""")
        startups_html = "\n".join(st_rows)

        # Education
        edu_rows = []
        for ed in self.data.education:
            inst = self.esc(ed.institution)
            loc = f", {self.esc(ed.location)}" if ed.location else ""
            edu_rows.append(f"""
            <div class="bx-edu-item">
                <div class="bx-edu-date">{self.esc(ed.period)}</div>
                <div class="bx-edu-school">{inst}{loc}</div>
                <div class="bx-edu-degree">{self.esc(ed.degree)}</div>
            </div>""")
        education_html = "\n".join(edu_rows)

        # Languages (Simple & clean text layout without sliders)
        lang_rows = []
        for lg in self.data.languages:
            lvl_text = lg.level or ""
            lang_rows.append(f"""
            <div class="bx-lang-item">
                <div class="bx-lang-name">{self.esc(lg.language)}</div>
                {f'<div class="bx-lang-level">{self.esc(lvl_text)}</div>' if lvl_text else ''}
            </div>""")
        languages_html = "\n".join(lang_rows)

        # Projects
        proj_rows = []
        for pr in self.data.projects:
            if pr.url:
                clean_url = pr.url.replace("https://", "").replace("http://", "").rstrip("/")
                icon = self.ICO_GITHUB if "github.com" in clean_url else self.ICO_LINK
                link = f'<a class="bx-link" href="{self.esc(pr.url)}" target="_blank" rel="noopener">{icon} {self.esc(clean_url)}</a>'
            else:
                link = ""
            tech = f'<div class="bx-tech-info">{self.esc(", ".join(pr.tech_stack))}</div>' if pr.tech_stack else ""
            desc = f'<div class="bx-proj-desc">{self.esc(pr.description)}</div>' if pr.description else ""
            proj_rows.append(f"""
            <div class="bx-job-item">
                <div class="bx-proj-header">
                    <span class="bx-job-role">{self.esc(pr.name)}</span>
                    {link}
                </div>
                {tech}
                {desc}
            </div>""")
        projects_html = "\n".join(proj_rows)

        # Skills (Technical & Soft)
        skills_blocks = []
        if self.data.skills_categorized:
            for cat_name, sks in self.data.skills_categorized.items():
                items = "".join(f'<span class="bx-skill-pill">{self.esc(s)}</span>' for s in sks)
                skills_blocks.append(f"""
                <div class="bx-skill-group">
                    <div class="bx-skill-cat">{self.esc(cat_name)}</div>
                    <div class="bx-skill-pills">{items}</div>
                </div>""")
        elif self.data.skills_technical:
            items = "".join(f'<span class="bx-skill-pill">{self.esc(s)}</span>' for s in self.data.skills_technical)
            skills_blocks.append(f'<div class="bx-skill-pills">{items}</div>')

        if self.data.skills_soft:
            soft_items = "".join(f'<span class="bx-skill-pill soft">{self.esc(s)}</span>' for s in self.data.skills_soft)
            skills_blocks.append(f"""
            <div class="bx-skill-group">
                <div class="bx-skill-cat">Umiejętności interpersonalne</div>
                <div class="bx-skill-pills">{soft_items}</div>
            </div>""")

        skills_html = "\n".join(skills_blocks)

        css = f"""
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        {self._css_variables()}
        {self._css_reset()}
        {self._css_common_components()}

        body {{
            background: #f1f5f9;
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #1e293b;
            line-height: 1.55;
            -webkit-font-smoothing: antialiased;
        }}

        .cv-container {{
            max-width: 890px;
            margin: 24px auto;
            background: #ffffff;
            padding: 38px 42px;
            box-shadow: 0 4px 24px rgba(15, 23, 42, 0.08);
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-sizing: border-box;
        }}

        /* Header with Rectangular Photo Top Right */
        .bx-header-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 22px;
        }}

        .bx-header-left {{
            vertical-align: middle;
            padding-right: 20px;
        }}

        .bx-header-right {{
            width: 130px;
            vertical-align: middle;
            text-align: right;
        }}

        .bx-name {{
            font-size: 30px;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.6px;
            line-height: 1.15;
            margin: 0;
        }}

        .bx-sub {{
            font-size: 14.5px;
            font-weight: 600;
            color: #475569;
            margin-top: 4px;
            margin-bottom: 12px;
            letter-spacing: -0.2px;
        }}

        .bx-contact-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px 12px;
            align-items: center;
        }}

        .bx-c-item {{
            display: inline-flex;
            align-items: center;
            font-size: 11.5px;
            font-weight: 500;
            color: #334155;
            background: #f8fafc;
            padding: 4px 9px;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
        }}

        .bx-c-item a {{
            color: #1e293b;
            text-decoration: none;
        }}

        .bx-c-item a:hover {{
            color: #0f172a;
            text-decoration: underline;
        }}

        .bx-c-item svg {{
            width: 13px;
            height: 13px;
            margin-right: 5px;
            stroke: #475569;
        }}

        .bx-photo-wrap {{
            display: inline-block;
        }}

        .bx-photo {{
            width: 118px;
            height: 138px;
            object-fit: cover;
            border-radius: 12px;
            border: 1.5px solid #cbd5e1;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
            display: block;
        }}

        .bx-photo-empty {{
            width: 118px;
            height: 138px;
            border-radius: 12px;
            border: 1.5px solid #cbd5e1;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f8fafc;
        }}

        .bx-user-svg {{
            width: 46px;
            height: 46px;
            stroke: #94a3b8;
        }}

        /* 2-Column Table Body */
        .bx-grid-table {{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            table-layout: fixed;
        }}

        .bx-col-left {{
            width: 58%;
            vertical-align: top;
            padding-right: 12px;
            box-sizing: border-box;
        }}

        .bx-col-right {{
            width: 42%;
            vertical-align: top;
            padding-left: 12px;
            box-sizing: border-box;
        }}

        /* Boxed Section Headers with soft curves */
        .bx-box-header {{
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 12px;
            font-weight: 700;
            color: #0f172a;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
        }}

        /* Rounded Content Containers */
        .bx-box-content {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 16px;
            page-break-inside: avoid;
        }}

        .bx-job-item {{
            margin-bottom: 14px;
            page-break-inside: avoid;
        }}

        .bx-job-item:last-child {{
            margin-bottom: 0;
        }}

        .bx-job-meta {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 8px;
            margin-bottom: 2px;
        }}

        .bx-job-date {{
            font-size: 11px;
            font-weight: 700;
            color: #64748b;
            letter-spacing: 0.2px;
        }}

        .bx-job-comp {{
            font-size: 12px;
            font-weight: 600;
            color: #334155;
            text-align: right;
        }}

        .bx-job-role {{
            font-size: 13.5px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 4px;
            line-height: 1.3;
        }}

        .bx-dash-list {{
            list-style: none;
            padding-left: 0;
            margin: 4px 0 0 0;
            font-size: 11.5px;
            color: #334155;
            line-height: 1.5;
        }}

        .bx-dash-list li {{
            position: relative;
            padding-left: 14px;
            margin-bottom: 3px;
        }}

        .bx-dash-list li::before {{
            content: "•";
            position: absolute;
            left: 2px;
            top: 0;
            color: #64748b;
            font-weight: bold;
        }}

        .bx-edu-item {{
            margin-bottom: 12px;
        }}

        .bx-edu-item:last-child {{
            margin-bottom: 0;
        }}

        .bx-edu-date {{
            font-size: 11px;
            font-weight: 700;
            color: #64748b;
            margin-bottom: 1px;
        }}

        .bx-edu-school {{
            font-size: 12px;
            font-weight: 600;
            color: #1e293b;
        }}

        .bx-edu-degree {{
            font-size: 11.5px;
            color: #475569;
            margin-top: 2px;
            line-height: 1.4;
        }}

        /* Languages: Clean modern list (No sliders) */
        .bx-lang-item {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            padding: 6px 0;
            border-bottom: 1px solid #f1f5f9;
        }}

        .bx-lang-item:last-child {{
            border-bottom: none;
            padding-bottom: 0;
        }}

        .bx-lang-name {{
            font-size: 12.5px;
            font-weight: 700;
            color: #0f172a;
        }}

        .bx-lang-level {{
            font-size: 11.5px;
            font-weight: 500;
            color: #64748b;
        }}

        /* Skills Pills */
        .bx-skill-group {{
            display: flex;
            align-items: baseline;
            gap: 10px;
            margin-bottom: 5px;
        }}

        .bx-skill-group:last-child {{
            margin-bottom: 0;
        }}

        .bx-skill-cat {{
            font-size: 11px;
            font-weight: 700;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            min-width: 120px;
            flex-shrink: 0;
            margin-bottom: 0;
        }}

        .bx-skill-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px 6px;
        }}

        .bx-skill-pill {{
            font-size: 10.5px;
            font-weight: 500;
            color: #1e293b;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: 2px 7px;
            line-height: 1.35;
        }}
            padding: 2.5px 8px;
        }}

        .bx-skill-pill.soft {{
            background: #fafafa;
            color: #475569;
        }}

        /* Projects */
        .bx-proj-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 8px;
            margin-bottom: 2px;
        }}

        .bx-link {{
            font-size: 11px;
            color: #2563eb;
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 3px;
        }}

        .bx-link:hover {{
            text-decoration: underline;
        }}

        .bx-tech-info {{
            font-size: 11px;
            font-weight: 500;
            color: #64748b;
            margin-bottom: 3px;
        }}

        .bx-proj-desc {{
            font-size: 11.5px;
            color: #334155;
            line-height: 1.45;
        }}

        .bx-rodo {{
            margin-top: 24px;
            padding-top: 10px;
            border-top: 1px solid #e2e8f0;
            font-size: 9.5px;
            color: #94a3b8;
            font-style: italic;
            text-align: justify;
            line-height: 1.4;
        }}

        {self._css_print_button()}
        {self._css_print_base()}

        @media print {{
            body {{
                background: #ffffff !important;
            }}
            .cv-container {{
                box-shadow: none !important;
                border: none !important;
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
            }}
            .bx-box-content {{
                border-color: #cbd5e1 !important;
            }}
            .bx-box-header {{
                background-color: #f1f5f9 !important;
                border-color: #cbd5e1 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}
            .bx-c-item {{
                background-color: #f8fafc !important;
                border-color: #e2e8f0 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}
            .bx-skill-pill {{
                background-color: #f1f5f9 !important;
                border-color: #e2e8f0 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}
        }}
        """

        loc_str = f", {self.info.location}" if self.info.location else ""
        sub_title = f"{self.info.title}{loc_str}" if self.info.title else (self.info.location or "")

        full_html = f"""{self._html_head(css)}
<body>
    {self._print_button()}
    <div class="cv-container">
        <!-- TOP HEADER -->
        <table class="bx-header-table">
            <tr>
                <td class="bx-header-left">
                    <h1 class="bx-name">{self.esc(self.info.name or "Kacper Pudełko")}</h1>
                    {f'<div class="bx-sub">{self.esc(sub_title)}</div>' if sub_title else ''}
                    <div class="bx-contact-bar">{contact_bar}</div>
                </td>
                <td class="bx-header-right">
                    {photo_html}
                </td>
            </tr>
        </table>

        <!-- 2-COLUMN GRID -->
        <table class="bx-grid-table">
            <tr>
                <!-- LEFT COLUMN -->
                <td class="bx-col-left">
                    {f'''
                    <div class="bx-box-header">Doświadczenie zawodowe</div>
                    <div class="bx-box-content">{experience_html}</div>
                    ''' if experience_html else ''}

                    {f'''
                    <div class="bx-box-header">Start-up & Inicjatywy</div>
                    <div class="bx-box-content">{startups_html}</div>
                    ''' if startups_html else ''}

                    {f'''
                    <div class="bx-box-header">Projekty własne</div>
                    <div class="bx-box-content">{projects_html}</div>
                    ''' if projects_html else ''}
                </td>

                <!-- RIGHT COLUMN -->
                <td class="bx-col-right">
                    {f'''
                    <div class="bx-box-header">Edukacja</div>
                    <div class="bx-box-content">{education_html}</div>
                    ''' if education_html else ''}

                    {f'''
                    <div class="bx-box-header">Języki obce</div>
                    <div class="bx-box-content">{languages_html}</div>
                    ''' if languages_html else ''}

                    {f'''
                    <div class="bx-box-header">Umiejętności</div>
                    <div class="bx-box-content">{skills_html}</div>
                    ''' if skills_html else ''}
                </td>
            </tr>
        </table>

        {f'<div class="bx-rodo">{self.esc(self.data.clause)}</div>' if self.data.clause else ''}
    </div>
</body>
</html>"""
        return self._write(output_path, full_html)
