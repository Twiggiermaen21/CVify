"""
Compact (High-Density) CV Template.
Engineered to maximize information density while maintaining supreme readability.
Uses a stable 2-column table grid to fit rich experience cleanly.
"""
from .base_template import BaseTemplate


class CompactTemplate(BaseTemplate):
    """Compact high-density two-column CV template."""

    def build(self, output_path: str = "nowe_cv.html") -> str:
        photo_html = self._photo_img(size=80, css_class="compact-photo")

        contact_bar = self._contact_bar_html(" &bull; ")

        # Left Column: Experience + Startups + Education
        exp_entries = self._experience_entries()
        experience_html = ""
        if exp_entries:
            experience_html = f"""
            <div class="col-section">
                <h2 class="col-section-title">Doświadczenie zawodowe</h2>
                {exp_entries}
            </div>"""

        st_entries = self._startup_entries()
        startups_html = ""
        if st_entries:
            startups_html = f"""
            <div class="col-section">
                <h2 class="col-section-title">Start-up & Własne Inicjatywy</h2>
                {st_entries}
            </div>"""

        edu_entries = self._education_entries()
        education_html = ""
        if edu_entries:
            education_html = f"""
            <div class="col-section">
                <h2 class="col-section-title">Wykształcenie</h2>
                {edu_entries}
            </div>"""

        # Right Column: Summary + Projects + Skills + Languages + Certs
        summary_html = ""
        if self.data.summary:
            summary_html = f"""
            <div class="col-section">
                <h2 class="col-section-title">Profil zawodowy</h2>
                <div class="summary-content">{self._summary_content()}</div>
            </div>"""

        pr_entries = self._project_entries()
        projects_html = ""
        if pr_entries:
            projects_html = f"""
            <div class="col-section">
                <h2 class="col-section-title">Projekty</h2>
                {pr_entries}
            </div>"""

        sk_content = self._skills_html()
        skills_html = ""
        if sk_content:
            skills_html = f"""
            <div class="col-section">
                <h2 class="col-section-title">Umiejętności i Technologie</h2>
                {sk_content}
            </div>"""

        lang_content = self._languages_html()
        languages_html = ""
        if lang_content:
            languages_html = f"""
            <div class="col-section">
                <h2 class="col-section-title">Języki obce</h2>
                {lang_content}
            </div>"""

        cert_content = self._certifications_html()
        cert_html = ""
        if cert_content:
            cert_html = f"""
            <div class="col-section">
                <h2 class="col-section-title">Certyfikaty</h2>
                {cert_content}
            </div>"""

        header_content = f"""
        <header class="header">
            <div class="header-inner">
                {f'<div class="header-photo">{photo_html}</div>' if photo_html else ''}
                <div class="header-text">
                    <h1 class="name">{self.esc(self.info.name or "Kacper Pudełko")}</h1>
                    {f'<div class="title">{self.esc(self.info.title)}</div>' if self.info.title else ''}
                    <div class="contact-bar">{contact_bar}</div>
                </div>
            </div>
        </header>"""

        css = f"""
        {self._css_variables()}
        {self._css_reset()}

        .cv-container {{
            max-width: 900px;
            margin: 0 auto;
            background: #ffffff;
            padding: 28px 34px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            border-radius: 6px;
        }}

        .header {{
            border-bottom: 2px solid var(--accent);
            padding-bottom: 12px;
            margin-bottom: 14px;
        }}

        .header-inner {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .header-photo {{
            flex-shrink: 0;
        }}

        .compact-photo {{
            border: 2px solid var(--accent);
        }}

        .header-text {{
            flex: 1;
        }}

        .name {{
            font-size: 24px;
            font-weight: 700;
            color: var(--primary);
            line-height: 1.1;
        }}

        .title {{
            font-size: 13.5px;
            font-weight: 600;
            color: var(--accent);
            margin-top: 2px;
            margin-bottom: 6px;
        }}

        .contact-bar {{
            font-size: 11.5px;
            color: var(--text-muted);
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
            line-height: 1.4;
        }}

        .contact-bar a {{
            color: var(--accent);
            text-decoration: none;
        }}

        .contact-bar a:hover {{
            text-decoration: underline;
        }}

        /* 2-Column Table */
        .compact-table {{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            table-layout: fixed;
        }}

        .col-left {{
            width: 53%;
            vertical-align: top;
            padding-right: 18px;
            border-right: 1px solid var(--border-color);
            box-sizing: border-box;
        }}

        .col-right {{
            width: 47%;
            vertical-align: top;
            padding-left: 18px;
            box-sizing: border-box;
        }}

        .col-section {{
            margin-bottom: 14px;
            page-break-inside: avoid;
        }}

        .col-section-title {{
            font-size: 12.5px;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--primary);
            border-bottom: 1.5px solid var(--primary);
            padding-bottom: 2px;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }}

        .summary-content p {{
            font-size: 12px;
            margin-bottom: 6px;
            color: var(--text-dark);
            text-align: justify;
            line-height: 1.45;
        }}

        {self._css_common_components()}

        /* Compact sizing tweaks */
        .entry-card {{
            margin-bottom: 9px;
        }}
        .entry-title {{
            font-size: 12.5px;
        }}
        .entry-subtitle {{
            font-size: 12px;
        }}
        .entry-date {{
            font-size: 11px;
        }}
        .bullet-list {{
            font-size: 11.5px;
            margin-left: 16px;
        }}
        .bullet-list li {{
            margin-bottom: 2px;
        }}
        .skill-pill {{
            font-size: 11px;
            padding: 1.5px 6px;
        }}
        .skill-cat-name {{
            font-size: 11.5px;
            min-width: 110px;
        }}
        .proj-desc {{
            font-size: 11.5px;
        }}
        .tech-badge {{
            font-size: 10px;
            padding: 1px 5px;
        }}

        {self._css_print_button()}
        {self._css_print_base()}
        """

        full_html = f"""{self._html_head(css)}
<body>
    {self._print_button()}
    <div class="cv-container">
        {header_content}
        <table class="compact-table">
            <tr>
                <td class="col-left">
                    {experience_html}
                    {startups_html}
                    {education_html}
                </td>
                <td class="col-right">
                    {summary_html}
                    {projects_html}
                    {skills_html}
                    {languages_html}
                    {cert_html}
                </td>
            </tr>
        </table>
        {self._clause_html()}
    </div>
</body>
</html>"""
        return self._write(output_path, full_html)

