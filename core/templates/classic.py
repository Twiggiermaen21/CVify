"""
Classic CV Template.
Traditional, elegant single-column layout. Centered header with subtle serif accents,
crisp borders, and clear hierarchical typography.
"""
from .base_template import BaseTemplate


class ClassicTemplate(BaseTemplate):
    """Classic single-column CV template with traditional styling."""

    def build(self, output_path: str = "nowe_cv.html") -> str:
        photo_html = self._photo_img(size=90, css_class="classic-photo")

        contact_bar = self._contact_bar_html(" &nbsp;|&nbsp; ")

        # Summary
        summary_html = ""
        if self.data.summary:
            summary_html = f"""
            <section class="section">
                <h2 class="section-title">Podsumowanie zawodowe</h2>
                <div class="summary-content">{self._summary_content()}</div>
            </section>"""

        # Experience
        exp_entries = self._experience_entries()
        experience_html = ""
        if exp_entries:
            experience_html = f"""
            <section class="section">
                <h2 class="section-title">Doświadczenie zawodowe</h2>
                {exp_entries}
            </section>"""

        # Startups
        st_entries = self._startup_entries()
        startups_html = ""
        if st_entries:
            startups_html = f"""
            <section class="section">
                <h2 class="section-title">Inicjatywy & Start-upy</h2>
                {st_entries}
            </section>"""

        # Projects
        pr_entries = self._project_entries()
        projects_html = ""
        if pr_entries:
            projects_html = f"""
            <section class="section">
                <h2 class="section-title">Projekty</h2>
                {pr_entries}
            </section>"""

        # Skills
        sk_content = self._skills_html()
        skills_html = ""
        if sk_content:
            skills_html = f"""
            <section class="section">
                <h2 class="section-title">Umiejętności</h2>
                {sk_content}
            </section>"""

        # Education
        edu_entries = self._education_entries()
        education_html = ""
        if edu_entries:
            education_html = f"""
            <section class="section">
                <h2 class="section-title">Edukacja</h2>
                {edu_entries}
            </section>"""

        # Languages
        lang_content = self._languages_html()
        languages_html = ""
        if lang_content:
            languages_html = f"""
            <section class="section">
                <h2 class="section-title">Języki</h2>
                {lang_content}
            </section>"""

        # Certifications
        cert_content = self._certifications_html()
        cert_html = ""
        if cert_content:
            cert_html = f"""
            <section class="section">
                <h2 class="section-title">Certyfikaty i kursy</h2>
                {cert_content}
            </section>"""

        header_content = f"""
        <header class="header">
            {f'<div class="header-photo">{photo_html}</div>' if photo_html else ''}
            <h1 class="name">{self.esc(self.info.name or "Kacper Pudełko")}</h1>
            {f'<div class="title">{self.esc(self.info.title)}</div>' if self.info.title else ''}
            <div class="contact-bar">{contact_bar}</div>
        </header>"""

        css = f"""
        {self._css_variables()}
        {self._css_reset()}

        .cv-container {{
            max-width: 840px;
            margin: 0 auto;
            background: #ffffff;
            padding: 42px 48px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            border-radius: 4px;
        }}

        .header {{
            text-align: center;
            border-bottom: 2px double var(--primary);
            padding-bottom: 16px;
            margin-bottom: 22px;
        }}

        .header-photo {{
            margin-bottom: 12px;
        }}

        .classic-photo {{
            border: 2px solid var(--border-color);
            display: inline-block;
        }}

        .name {{
            font-size: 28px;
            font-weight: 700;
            color: var(--primary);
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }}

        .title {{
            font-size: 14.5px;
            font-weight: 600;
            color: var(--accent);
            margin-top: 4px;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }}

        .contact-bar {{
            font-size: 12.5px;
            color: var(--text-dark);
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 6px;
        }}

        .contact-bar a {{
            color: var(--primary);
            text-decoration: none;
        }}

        .contact-bar a:hover {{
            text-decoration: underline;
        }}

        .section {{
            margin-bottom: 20px;
            page-break-inside: avoid;
        }}

        .section-title {{
            font-size: 14px;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--primary);
            border-bottom: 1px solid var(--primary);
            padding-bottom: 3px;
            margin-bottom: 10px;
            letter-spacing: 0.8px;
        }}

        .summary-content p {{
            font-size: 13px;
            margin-bottom: 8px;
            color: var(--text-dark);
            text-align: justify;
            line-height: 1.5;
        }}

        {self._css_common_components()}
        {self._css_print_button()}
        {self._css_print_base()}
        """

        full_html = f"""{self._html_head(css)}
<body>
    {self._print_button()}
    <div class="cv-container">
        {header_content}
        {summary_html}
        {experience_html}
        {startups_html}
        {projects_html}
        {skills_html}
        {education_html}
        {languages_html}
        {cert_html}
        {self._clause_html()}
    </div>
</body>
</html>"""
        return self._write(output_path, full_html)

