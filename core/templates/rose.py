"""
Rose Script & Burgundy CV Template.
Direct 1:1 recreation of Image 5 (Aleksandra Nowak):
- Elegant cursive / script burgundy header for candidate name
- Soft pale rose/blush left sidebar with circular photo
- Underlined section headers (Dane osobowe, Umiejętności, Języki, Zainteresowania)
- Right-aligned location & dates for jobs and education
- Full-width subtle section divider lines
- Table-based layout for rock-solid PDF printing
"""
from .base_template import BaseTemplate


class RoseTemplate(BaseTemplate):
    """Elegant cursive script & burgundy template with soft blush sidebar."""

    def build(self, output_path: str = "nowe_cv.html") -> str:
        photo_uri = self._photo_base64()
        if photo_uri:
            photo_html = f'<div class="rose-photo-wrap"><img src="{photo_uri}" alt="{self.esc(self.info.name)}" class="rose-photo"></div>'
        else:
            photo_html = '<div class="rose-photo-wrap"><div class="rose-photo-empty">👤</div></div>'
            photo_html = '<div class="rose-photo-wrap"><div class="rose-photo-empty"><svg class="rose-user-svg" viewBox="0 0 24 24" fill="none" stroke="#8b1538" stroke-width="1.5"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 4-6 8-6s8 2 8 6"/></svg></div></div>'

        info = self.info
        contact_rows = []
        if info.email:
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">✉</span><span><a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a></span></div>')
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">{self.ICO_MAIL}</span><span><a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a></span></div>')
        if info.phone:
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">📞</span><span><a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a></span></div>')
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">{self.ICO_PHONE}</span><span><a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a></span></div>')
        if info.location:
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">📍</span><span>{self.esc(info.location)}</span></div>')
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">{self.ICO_PIN}</span><span>{self.esc(info.location)}</span></div>')
        if info.linkedin:
            lbl = info.linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">💼</span><span><a href="{self.esc(info.linkedin)}" target="_blank">{self.esc(lbl)}</a></span></div>')
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">{self.ICO_LINKEDIN}</span><span><a href="{self.esc(info.linkedin)}" target="_blank">{self.esc(lbl)}</a></span></div>')
        if info.github:
            lbl = info.github.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">🐙</span><span><a href="{self.esc(info.github)}" target="_blank">{self.esc(lbl)}</a></span></div>')
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">{self.ICO_GITHUB}</span><span><a href="{self.esc(info.github)}" target="_blank">{self.esc(lbl)}</a></span></div>')
        if info.driver_license:
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">🚗</span><span>Prawo jazdy: {self.esc(info.driver_license)}</span></div>')
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">{self.ICO_CAR}</span><span>Prawo jazdy: {self.esc(info.driver_license)}</span></div>')
        
        contact_html = "\n".join(contact_rows)

        # Skills for sidebar
        skills_sidebar_rows = []
        if self.data.skills_categorized:
            for cat_name, sks in self.data.skills_categorized.items():
                items = ", ".join(self.esc(s) for s in sks)
                skills_sidebar_rows.append(f"""
                <div class="rose-sb-skill-block">
                    <div class="rose-sb-skill-cat">{self.esc(cat_name)}:</div>
                    <div class="rose-sb-skill-items">{items}</div>
                </div>""")
        elif self.data.skills_technical:
            skills_sidebar_rows.append(f"""
            <div class="rose-sb-skill-block">
                <div class="rose-sb-skill-cat">Umiejętności techniczne:</div>
                <div class="rose-sb-skill-items">{", ".join(self.esc(s) for s in self.data.skills_technical)}</div>
            </div>""")

        if self.data.skills_soft:
            skills_sidebar_rows.append(f"""
            <div class="rose-sb-skill-block">
                <div class="rose-sb-skill-cat">Komunikacja & Zespół:</div>
                <div class="rose-sb-skill-items">{", ".join(self.esc(s) for s in self.data.skills_soft)}</div>
            </div>""")

        skills_sidebar_html = "\n".join(skills_sidebar_rows)

        # Languages for sidebar
        lang_rows = []
        for lg in self.data.languages:
            lvl = f" ({self.esc(lg.level)})" if lg.level else ""
            lang_rows.append(f'<div class="rose-lang-item">{self.esc(lg.language)}{lvl}</div>')
        lang_html = "\n".join(lang_rows)

        # Soft skills / interests
        interests_html = ""
        if self.data.skills_soft:
            interests_html = f'<div class="rose-sb-skill-items">{", ".join(self.esc(s) for s in self.data.skills_soft)}</div>'

        # RIGHT COLUMN: Experience with right-aligned dates & locations
        exp_rows = []
        for exp in self.data.experience:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in exp.description)
            loc = self.esc(exp.location) if exp.location else ""
            date_loc = f"{loc} &nbsp;&bull;&nbsp; {self.esc(exp.period)}" if loc else self.esc(exp.period)
            exp_rows.append(f"""
            <div class="rose-entry">
                <div class="rose-entry-row">
                    <span class="rose-role">{self.esc(exp.role)}</span>
                    <span class="rose-meta">{date_loc}</span>
                </div>
                <div class="rose-company">{self.esc(exp.company)}</div>
                <ul class="rose-bullets">{bullets}</ul>
            </div>""")
        experience_html = "\n".join(exp_rows)

        # Startups
        st_rows = []
        for st in self.data.startups:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in st.description)
            tech = f'<div class="rose-tech">Tech: {self.esc(", ".join(st.tech_stack))}</div>' if st.tech_stack else ""
            st_rows.append(f"""
            <div class="rose-entry">
                <div class="rose-entry-row">
                    <span class="rose-role">{self.esc(st.name)}</span>
                    {f'<span class="rose-meta">{self.esc(st.period)}</span>' if st.period else ''}
                </div>
                {tech}
                <ul class="rose-bullets">{bullets}</ul>
            </div>""")
        startups_html = "\n".join(st_rows)

        # Projects
        proj_rows = []
        for pr in self.data.projects:
            link = f'<a class="rose-link" href="{self.esc(pr.url)}" target="_blank">🔗 Link</a>' if pr.url else ""
            link = f'<a class="rose-link" href="{self.esc(pr.url)}" target="_blank">{self.ICO_LINK} Link</a>' if pr.url else ""
            tech = f'<span class="rose-tech-inline">[{self.esc(", ".join(pr.tech_stack))}]</span>' if pr.tech_stack else ""
            desc = f'<p class="rose-desc">{self.esc(pr.description)}</p>' if pr.description else ""
            proj_rows.append(f"""
            <div class="rose-entry">
                <div class="rose-entry-row">
                    <span class="rose-role">{self.esc(pr.name)} {tech}</span>
                    {link}
                </div>
                {desc}
            </div>""")
        projects_html = "\n".join(proj_rows)

        # Education
        edu_rows = []
        for ed in self.data.education:
            loc = self.esc(ed.location) if ed.location else ""
            date_loc = f"{loc} &nbsp;&bull;&nbsp; {self.esc(ed.period)}" if loc else self.esc(ed.period)
            edu_rows.append(f"""
            <div class="rose-entry">
                <div class="rose-entry-row">
                    <span class="rose-role">{self.esc(ed.degree)}</span>
                    <span class="rose-meta">{date_loc}</span>
                </div>
                <div class="rose-company">{self.esc(ed.institution)}</div>
            </div>""")
        education_html = "\n".join(edu_rows)

        css = f"""
        {self._css_variables()}
        {self._css_reset()}
        {self._css_common_components()}

        .rose-user-svg {{
            width: 54px;
            height: 54px;
            stroke: #8b1538;
        }}

        .cv-container {{
            max-width: 890px;
            margin: 0 auto;
            background: #ffffff;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
            border-radius: 4px;
            overflow: hidden;
        }}

        .rose-table {{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            table-layout: fixed;
        }}

        /* Left Pale Rose Sidebar */
        .rose-sidebar {{
            width: 32%;
            background-color: #fcf7f7;
            color: #333333;
            padding: 38px 24px;
            vertical-align: top;
            box-sizing: border-box;
            border-right: 1px solid #f2e4e4;
        }}

        .rose-photo-wrap {{
            text-align: center;
            margin-bottom: 24px;
        }}

        .rose-photo {{
            width: 130px;
            height: 130px;
            object-fit: cover;
            border-radius: 50%;
            display: inline-block;
            border: 4px solid #ffffff;
            box-shadow: 0 4px 12px rgba(139, 21, 56, 0.12);
        }}

        .rose-photo-empty {{
            width: 130px;
            height: 130px;
            border-radius: 50%;
            background: #ffffff;
            border: 4px solid #ffffff;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 38px;
            box-shadow: 0 4px 12px rgba(139, 21, 56, 0.12);
        }}

        .rose-sb-title {{
            font-size: 13.5px;
            font-weight: 700;
            color: #222222;
            border-bottom: 1px solid #718096;
            padding-bottom: 3px;
            margin-top: 24px;
            margin-bottom: 12px;
        }}

        .rose-contact-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11.5px;
            color: #4a5568;
            margin-bottom: 8px;
            line-height: 1.4;
            word-break: break-all;
        }}

        .rose-contact-row a {{
            color: #222222;
            text-decoration: none;
        }}

        .rose-contact-row a:hover {{
            color: #8b1538;
            text-decoration: underline;
        }}

        .rose-c-icon {{
            font-size: 11.5px;
            color: #222222;
            flex-shrink: 0;
        }}

        .rose-sb-skill-block {{
            margin-bottom: 10px;
        }}

        .rose-sb-skill-cat {{
            font-size: 11.5px;
            font-weight: 700;
            color: #333333;
            margin-bottom: 2px;
        }}

        .rose-sb-skill-items {{
            font-size: 11px;
            color: #555555;
            line-height: 1.45;
        }}

        .rose-lang-item {{
            font-size: 11.5px;
            color: #444444;
            margin-bottom: 6px;
        }}

        /* Right Column with Elegant Burgundy Script Header */
        .rose-main {{
            width: 68%;
            background-color: #ffffff;
            color: #2d3748;
            padding: 40px 38px;
            vertical-align: top;
            box-sizing: border-box;
        }}

        .rose-name {{
            font-family: 'Playfair Display', Georgia, 'Brush Script MT', 'Dancing Script', 'Caveat', cursive, serif;
            font-size: 38px;
            font-weight: 700;
            font-style: italic;
            color: #8b1538;
            letter-spacing: 0.5px;
            line-height: 1.1;
            margin-bottom: 2px;
        }}

        .rose-title {{
            font-size: 14.5px;
            font-weight: 600;
            color: #4a5568;
            margin-bottom: 16px;
        }}

        .rose-summary {{
            font-size: 12.5px;
            color: #4a5568;
            text-align: justify;
            line-height: 1.55;
            margin-bottom: 20px;
        }}

        .rose-section-title {{
            font-size: 13.5px;
            font-weight: 700;
            color: #222222;
            border-bottom: 1px solid #d2d6dc;
            padding-bottom: 4px;
            margin-top: 22px;
            margin-bottom: 12px;
        }}

        .rose-entry {{
            margin-bottom: 14px;
            page-break-inside: avoid;
        }}

        .rose-entry-row {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 2px;
        }}

        .rose-role {{
            font-size: 13.5px;
            font-weight: 700;
            color: #222222;
        }}

        .rose-meta {{
            font-size: 11.5px;
            color: #718096;
            white-space: nowrap;
        }}

        .rose-company {{
            font-size: 12px;
            color: #555555;
            font-style: italic;
            margin-bottom: 4px;
        }}

        .rose-bullets {{
            list-style-type: disc;
            margin-left: 20px;
            font-size: 12px;
            color: #333333;
            line-height: 1.5;
        }}

        .rose-bullets li {{
            margin-bottom: 2.5px;
        }}

        .rose-tech {{
            font-size: 11px;
            color: #718096;
            margin-bottom: 3px;
        }}

        .rose-tech-inline {{
            font-size: 11px;
            color: #8b1538;
            font-weight: normal;
        }}

        .rose-desc {{
            font-size: 12px;
            color: #4a5568;
            margin-top: 2px;
            text-align: justify;
        }}

        .rose-link {{
            font-size: 11.5px;
            color: #8b1538;
            text-decoration: none;
        }}

        .rose-rodo {{
            margin-top: 28px;
            padding-top: 10px;
            border-top: 1px solid #f2e4e4;
            font-size: 10px;
            color: #a0aec0;
            font-style: italic;
            text-align: justify;
            line-height: 1.4;
        }}

        {self._css_print_button()}
        {self._css_print_base()}

        @media print {{
            .rose-sidebar {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                background-color: #fcf7f7 !important;
            }}
            .rose-name {{
                color: #8b1538 !important;
            }}
        }}
        """

        summary_p = f'<div class="rose-summary">{self._summary_content()}</div>' if self.data.summary else ""

        full_html = f"""{self._html_head(css)}
<body>
    {self._print_button()}
    <div class="cv-container">
        <table class="rose-table">
            <tr>
                <!-- LEFT BLUSH SIDEBAR -->
                <td class="rose-sidebar">
                    {photo_html}

                    <div class="rose-sb-title">Dane osobowe</div>
                    {contact_html}

                    {f'<div class="rose-sb-title">Umiejętności</div>{skills_sidebar_html}' if skills_sidebar_html else ''}
                    {f'<div class="rose-sb-title">Języki</div>{lang_html}' if lang_html else ''}
                    {f'<div class="rose-sb-title">Zainteresowania</div>{interests_html}' if interests_html else ''}
                </td>

                <!-- RIGHT MAIN CONTENT -->
                <td class="rose-main">
                    <h1 class="rose-name">{self.esc(self.info.name or "Kacper Pudełko")}</h1>
                    {f'<div class="rose-title">{self.esc(self.info.title)}</div>' if self.info.title else ''}

                    {f'<div class="rose-section-title">Podsumowanie</div>{summary_p}' if summary_p else ''}
                    {f'<div class="rose-section-title">Doświadczenie</div>{experience_html}' if experience_html else ''}
                    {f'<div class="rose-section-title">Start-up & Inicjatywy</div>{startups_html}' if startups_html else ''}
                    {f'<div class="rose-section-title">Wybrane Projekty</div>{projects_html}' if projects_html else ''}
                    {f'<div class="rose-section-title">Wykształcenie</div>{education_html}' if education_html else ''}

                    {f'<div class="rose-rodo">{self.esc(self.data.clause)}</div>' if self.data.clause else ''}
                </td>
            </tr>
        </table>
    </div>
</body>
</html>"""
        return self._write(output_path, full_html)

