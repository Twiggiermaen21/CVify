"""
Blush Pastel CV Template.
Direct 1:1 recreation of Image 2 (Laura Kubiak warm beige / blush style):
- Warm beige/blush left sidebar with ring-bordered circular photo
- Icon-prefixed section titles with full-width divider lines (💼 DOŚWIADCZENIE, 🎓 WYKSZTAŁCENIE, ⭐ UMIEJĘTNOŚCI)
- Section titles with full-width divider lines (DOSWIADCZENIE, WYKSZTALCENIE, UMIEJETNOSCI)
- Right-aligned job dates on the role line
- Warm cocoa/mocha typography and delicate bullet points
- Table-based layout for rock-solid PDF printing
"""
from .base_template import BaseTemplate


class BlushTemplate(BaseTemplate):
    """Warm beige / blush palette template with icon-prefixed section dividers."""

    def build(self, output_path: str = "nowe_cv.html") -> str:
        # Photo: circular with delicate double ring
        photo_uri = self._photo_base64()
        if photo_uri:
            photo_html = f'<div class="blush-photo-wrap"><img src="{photo_uri}" alt="{self.esc(self.info.name)}" class="blush-photo"></div>'
        else:
            photo_html = ""

        info = self.info
        contact_rows = []
        if info.phone:
            contact_rows.append(f'<div class="blush-contact-row"><span class="blush-icon">📞</span><span><a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a></span></div>')
            contact_rows.append(f'<div class="blush-contact-row"><span class="blush-icon">{self.ICO_PHONE}</span><span><a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a></span></div>')
        if info.email:
            contact_rows.append(f'<div class="blush-contact-row"><span class="blush-icon">✉</span><span><a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a></span></div>')
            contact_rows.append(f'<div class="blush-contact-row"><span class="blush-icon">{self.ICO_MAIL}</span><span><a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a></span></div>')
        if info.location:
            contact_rows.append(f'<div class="blush-contact-row"><span class="blush-icon">📍</span><span>{self.esc(info.location)}</span></div>')
            contact_rows.append(f'<div class="blush-contact-row"><span class="blush-icon">{self.ICO_PIN}</span><span>{self.esc(info.location)}</span></div>')
        if info.linkedin:
            lbl = info.linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_rows.append(f'<div class="blush-contact-row"><span class="blush-icon">💼</span><span><a href="{self.esc(info.linkedin)}" target="_blank">{self.esc(lbl)}</a></span></div>')
            contact_rows.append(f'<div class="blush-contact-row"><span class="blush-icon">{self.ICO_LINKEDIN}</span><span><a href="{self.esc(info.linkedin)}" target="_blank">{self.esc(lbl)}</a></span></div>')
        if info.github:
            lbl = info.github.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_rows.append(f'<div class="blush-contact-row"><span class="blush-icon">🐙</span><span><a href="{self.esc(info.github)}" target="_blank">{self.esc(lbl)}</a></span></div>')
            contact_rows.append(f'<div class="blush-contact-row"><span class="blush-icon">{self.ICO_GITHUB}</span><span><a href="{self.esc(info.github)}" target="_blank">{self.esc(lbl)}</a></span></div>')
        if info.driver_license:
            contact_rows.append(f'<div class="blush-contact-row"><span class="blush-icon">🚗</span><span>Prawo jazdy: {self.esc(info.driver_license)}</span></div>')
            contact_rows.append(f'<div class="blush-contact-row"><span class="blush-icon">{self.ICO_CAR}</span><span>Prawo jazdy: {self.esc(info.driver_license)}</span></div>')
        
        contact_html = "\n".join(contact_rows)

        # Languages for sidebar
        lang_rows = []
        for lg in self.data.languages:
            lvl = f" – {self.esc(lg.level)}" if lg.level else ""
            lang_rows.append(f'<li class="blush-sb-bullet"><b>{self.esc(lg.language)}</b>{lvl}</li>')
        lang_html = f'<ul class="blush-sb-list">{"".join(lang_rows)}</ul>' if lang_rows else ""

        # Soft skills / Additional info for sidebar
        add_rows = []
        if info.driver_license:
            add_rows.append(f'<li class="blush-sb-bullet">Prawo jazdy kat. {self.esc(info.driver_license)}</li>')
        if self.data.skills_soft:
            for s in self.data.skills_soft:
                add_rows.append(f'<li class="blush-sb-bullet">{self.esc(s)}</li>')
        add_info_html = f'<ul class="blush-sb-list">{"".join(add_rows)}</ul>' if add_rows else ""

        # Certifications for sidebar
        cert_rows = []
        for c in self.data.certifications:
            cert_rows.append(f'<li class="blush-sb-bullet">{self.esc(c)}</li>')
        cert_html = f'<ul class="blush-sb-list">{"".join(cert_rows)}</ul>' if cert_rows else ""

        # RIGHT COLUMN: Experience with right-aligned dates
        exp_rows = []
        for exp in self.data.experience:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in exp.description)
            comp_loc = self.esc(exp.company)
            if exp.location:
                comp_loc += f", {self.esc(exp.location)}"
            exp_rows.append(f"""
            <div class="blush-entry">
                <div class="blush-entry-row">
                    <span class="blush-role">{self.esc(exp.role)}</span>
                    <span class="blush-date">{self.esc(exp.period)}</span>
                </div>
                <div class="blush-company">{comp_loc}</div>
                <ul class="blush-bullets">{bullets}</ul>
            </div>""")
        experience_html = "\n".join(exp_rows)

        # Startups
        st_rows = []
        for st in self.data.startups:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in st.description)
            tech = f'<div class="blush-tech">Tech stack: {self.esc(", ".join(st.tech_stack))}</div>' if st.tech_stack else ""
            st_rows.append(f"""
            <div class="blush-entry">
                <div class="blush-entry-row">
                    <span class="blush-role">{self.esc(st.name)}</span>
                    {f'<span class="blush-date">{self.esc(st.period)}</span>' if st.period else ''}
                </div>
                {tech}
                <ul class="blush-bullets">{bullets}</ul>
            </div>""")
        startups_html = "\n".join(st_rows)

        # Education
        edu_rows = []
        for ed in self.data.education:
            inst = self.esc(ed.institution)
            loc = f" – {self.esc(ed.location)}" if ed.location else ""
            edu_rows.append(f"""
            <div class="blush-entry">
                <div class="blush-entry-row">
                    <span class="blush-role">{self.esc(ed.degree)}</span>
                    <span class="blush-date">{self.esc(ed.period)}</span>
                </div>
                <div class="blush-company">{inst}{loc}</div>
            </div>""")
        education_html = "\n".join(edu_rows)

        # Projects
        proj_rows = []
        for pr in self.data.projects:
            link = f'<a class="blush-link" href="{self.esc(pr.url)}" target="_blank">🔗 Link</a>' if pr.url else ""
            link = f'<a class="blush-link" href="{self.esc(pr.url)}" target="_blank">{self.ICO_LINK} Link</a>' if pr.url else ""
            tech = f'<span class="blush-tech-inline">[{self.esc(", ".join(pr.tech_stack))}]</span>' if pr.tech_stack else ""
            desc = f'<p class="blush-desc">{self.esc(pr.description)}</p>' if pr.description else ""
            proj_rows.append(f"""
            <div class="blush-entry">
                <div class="blush-entry-row">
                    <span class="blush-role">{self.esc(pr.name)} {tech}</span>
                    {link}
                </div>
                {desc}
            </div>""")
        projects_html = "\n".join(proj_rows)

        # Skills (Categorized)
        skills_rows = []
        if self.data.skills_categorized:
            for cat_name, sks in self.data.skills_categorized.items():
                items = "".join(f"<li>{self.esc(s)}</li>" for s in sks)
                skills_rows.append(f"""
                <div class="blush-skill-group">
                    <div class="blush-skill-cat-title">{self.esc(cat_name)}:</div>
                    <ul class="blush-bullets">{items}</ul>
                </div>""")
        elif self.data.skills_technical:
            items = "".join(f"<li>{self.esc(s)}</li>" for s in self.data.skills_technical)
            skills_rows.append(f'<ul class="blush-bullets">{items}</ul>')
        skills_html = "\n".join(skills_rows)

        css = f"""
        {self._css_variables()}
        {self._css_reset()}

        .cv-container {{
            max-width: 890px;
            margin: 0 auto;
            background: #ffffff;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
            border-radius: 4px;
            overflow: hidden;
        }}

        .blush-table {{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            table-layout: fixed;
        }}

        /* Left Warm Beige / Blush Sidebar */
        .blush-sidebar {{
            width: 32%;
            background-color: #f6f1ed;
            color: #3d312a;
            padding: 38px 22px;
            vertical-align: top;
            box-sizing: border-box;
            border-right: 1px solid #ebdcd3;
        }}

        .blush-photo-wrap {{
            text-align: center;
            margin-bottom: 24px;
        }}

        .blush-photo {{
            width: 130px;
            height: 130px;
            object-fit: cover;
            border-radius: 50%;
            display: inline-block;
            border: 4px solid #ffffff;
            box-shadow: 0 0 0 1.5px #cbb5a8, 0 4px 10px rgba(0,0,0,0.06);
        }}

        .blush-sb-title {{
            font-size: 12.5px;
            text-transform: uppercase;
            font-weight: 800;
            letter-spacing: 1px;
            color: #3d312a;
            margin-top: 24px;
            margin-bottom: 12px;
        }}

        .blush-contact-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11.5px;
            color: #4f423a;
            margin-bottom: 8px;
            line-height: 1.4;
            word-break: break-all;
        }}

        .blush-contact-row a {{
            color: #3d312a;
            text-decoration: none;
        }}

        .blush-contact-row a:hover {{
            text-decoration: underline;
        }}

        .blush-icon {{
            font-size: 12px;
            flex-shrink: 0;
            opacity: 0.8;
        }}

        .blush-sb-list {{
            list-style-type: disc;
            margin-left: 16px;
            font-size: 11.5px;
            color: #4f423a;
            line-height: 1.45;
        }}

        .blush-sb-bullet {{
            margin-bottom: 4px;
        }}

        /* Right Column */
        .blush-main {{
            width: 68%;
            background-color: #ffffff;
            color: #2d3748;
            padding: 40px 38px;
            vertical-align: top;
            box-sizing: border-box;
        }}

        .blush-name {{
            font-size: 32px;
            font-weight: 800;
            color: #332a24;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            line-height: 1.1;
            margin-bottom: 4px;
        }}

        .blush-title {{
            font-size: 14px;
            font-weight: 700;
            color: #7d6b60;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 14px;
        }}

        .blush-summary {{
            font-size: 12.5px;
            color: #4a5568;
            text-align: justify;
            line-height: 1.6;
            margin-bottom: 24px;
        }}

        .blush-section-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 22px;
            margin-bottom: 14px;
            border-bottom: 1px solid #d8ccc4;
            padding-bottom: 4px;
        }}

        .blush-sec-icon {{
            font-size: 14px;
        .blush-sec-indicator {{
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #7d6b60;
            display: inline-block;
            flex-shrink: 0;
        }}

        .blush-section-title {{
            font-size: 13.5px;
            font-weight: 800;
            color: #332a24;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .blush-entry {{
            margin-bottom: 14px;
            page-break-inside: avoid;
        }}

        .blush-entry-row {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 2px;
        }}

        .blush-role {{
            font-size: 13.5px;
            font-weight: 700;
            color: #2d3748;
        }}

        .blush-date {{
            font-size: 12px;
            color: #718096;
            white-space: nowrap;
        }}

        .blush-company {{
            font-size: 12px;
            color: #7d6b60;
            font-style: italic;
            margin-bottom: 4px;
        }}

        .blush-bullets {{
            list-style-type: disc;
            margin-left: 20px;
            font-size: 12px;
            color: #2d3748;
            line-height: 1.5;
        }}

        .blush-bullets li {{
            margin-bottom: 2.5px;
        }}

        .blush-skill-group {{
            margin-bottom: 8px;
            page-break-inside: avoid;
        }}

        .blush-skill-cat-title {{
            font-size: 12.5px;
            font-weight: 700;
            color: #332a24;
            margin-bottom: 2px;
        }}

        .blush-tech {{
            font-size: 11px;
            color: #7d6b60;
            margin-bottom: 3px;
        }}

        .blush-tech-inline {{
            font-size: 11px;
            color: #7d6b60;
            font-weight: normal;
        }}

        .blush-desc {{
            font-size: 12px;
            color: #4a5568;
            margin-top: 2px;
            text-align: justify;
        }}

        .blush-link {{
            font-size: 11.5px;
            color: #7d6b60;
            text-decoration: none;
        }}

        .blush-rodo {{
            margin-top: 28px;
            padding-top: 10px;
            border-top: 1px solid #ebdcd3;
            font-size: 10px;
            color: #a0aec0;
            font-style: italic;
            text-align: justify;
            line-height: 1.4;
        }}

        {self._css_print_button()}
        {self._css_print_base()}

        @media print {{
            .blush-sidebar {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                background-color: #f6f1ed !important;
                color: #3d312a !important;
            }}
            .blush-photo {{
                border-color: #ffffff !important;
            }}
        }}
        """

        summary_p = f'<div class="blush-summary">{self._summary_content()}</div>' if self.data.summary else ""

        full_html = f"""{self._html_head(css)}
<body>
    {self._print_button()}
    <div class="cv-container">
        <table class="blush-table">
            <tr>
                <!-- LEFT BLUSH SIDEBAR -->
                <td class="blush-sidebar">
                    {photo_html}

                    <div class="blush-sb-title">Kontakt</div>
                    {contact_html}

                    {f'<div class="blush-sb-title">Kursy i Szkolenia</div>{cert_html}' if cert_html else ''}
                    {f'<div class="blush-sb-title">Dodatkowe informacje</div>{add_info_html}' if add_info_html else ''}
                    {f'<div class="blush-sb-title">Języki obce</div>{lang_html}' if lang_html else ''}
                </td>

                <!-- RIGHT MAIN CONTENT -->
                <td class="blush-main">
                    <h1 class="blush-name">{self.esc(self.info.name or "Kacper Pudełko")}</h1>
                    {f'<div class="blush-title">{self.esc(self.info.title)}</div>' if self.info.title else ''}
                    {summary_p}

                    {f'''<div class="blush-section-header">
                        <span class="blush-sec-icon">💼</span>
                        <span class="blush-sec-indicator"></span>
                        <span class="blush-section-title">Doświadczenie</span>
                    </div>{experience_html}''' if experience_html else ''}

                    {f'''<div class="blush-section-header">
                        <span class="blush-sec-icon">🚀</span>
                        <span class="blush-sec-indicator"></span>
                        <span class="blush-section-title">Start-up & Inicjatywy</span>
                    </div>{startups_html}''' if startups_html else ''}

                    {f'''<div class="blush-section-header">
                        <span class="blush-sec-icon">💻</span>
                        <span class="blush-sec-indicator"></span>
                        <span class="blush-section-title">Wybrane Projekty</span>
                    </div>{projects_html}''' if projects_html else ''}

                    {f'''<div class="blush-section-header">
                        <span class="blush-sec-icon">🎓</span>
                        <span class="blush-sec-indicator"></span>
                        <span class="blush-section-title">Wykształcenie</span>
                    </div>{education_html}''' if education_html else ''}

                    {f'''<div class="blush-section-header">
                        <span class="blush-sec-icon">⭐</span>
                        <span class="blush-sec-indicator"></span>
                        <span class="blush-section-title">Umiejętności</span>
                    </div>{skills_html}''' if skills_html else ''}

                    {f'<div class="blush-rodo">{self.esc(self.data.clause)}</div>' if self.data.clause else ''}
                </td>
            </tr>
        </table>
    </div>
</body>
</html>"""
        return self._write(output_path, full_html)

