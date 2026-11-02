"""
Elegant CV Template.
Refined minimalist design with left-accent borders, generous breathing room,
and crisp, sophisticated typography.
"""
from .base_template import BaseTemplate


class ElegantTemplate(BaseTemplate):
    """Minimalist & elegant single-column CV template."""

    def build(self, output_path: str = "nowe_cv.html") -> str:
        photo_html = self._photo_img(size=92, css_class="elegant-photo")

        contact_bar = self._contact_bar_html(" &nbsp;&bull;&nbsp; ")

        # Summary
        summary_html = ""
        if self.data.summary:
            summary_html = f"""
            <section class="section">
                <h2 class="section-title">O mnie</h2>
                <div class="summary-content">{self._summary_content()}</div>
            </section>"""

        # Experience
        exp_entries = self._experience_entries()
        experience_html = ""
        if exp_entries:
            experience_html = f"""
            <section class="section">
                <h2 class="section-title">Doświadczenie</h2>
                {exp_entries}
            </section>"""

        # Startups
        st_entries = self._startup_entries()
        startups_html = ""
        if st_entries:
            startups_html = f"""
            <section class="section">
                <h2 class="section-title">Inicjatywy & Start-up</h2>
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
                <h2 class="section-title">Technologie i Umiejętności</h2>
                {sk_content}
            </section>"""

        # Education
        edu_entries = self._education_entries()
        education_html = ""
        if edu_entries:
            education_html = f"""
            <section class="section">
                <h2 class="section-title">Wykształcenie</h2>
                {edu_entries}
            </section>"""

        # Languages
        lang_content = self._languages_html()
        languages_html = ""
        if lang_content:
            languages_html = f"""
            <section class="section">
                <h2 class="section-title">Języki obce</h2>
                {lang_content}
            </section>"""

        # Certifications
        cert_content = self._certifications_html()
        cert_html = ""
        if cert_content:
            cert_html = f"""
            <section class="section">
                <h2 class="section-title">Certyfikaty</h2>
                {cert_content}
            </section>"""

        header_content = f"""
        <header class="header">
            <div class="header-inner">
                {f'<div class="header-photo">{photo_html}</div>' if photo_html else ''}
                <div class="header-info">
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
            max-width: 860px;
            margin: 0 auto;
            background: #ffffff;
            padding: 44px 50px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
            border-radius: 6px;
            border-top: 4px solid var(--accent);
        }}

        .header {{
            padding-bottom: 20px;
            margin-bottom: 24px;
            border-bottom: 1px solid var(--border-color);
        }}

        .header-inner {{
            display: flex;
            align-items: center;
            gap: 24px;
        }}

        .header-photo {{
            flex-shrink: 0;
        }}

        .elegant-photo {{
            border: 2px solid var(--accent);
            padding: 2px;
            background: #ffffff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}

        .header-info {{
            flex: 1;
        }}

        .name {{
            font-size: 29px;
            font-weight: 700;
            color: var(--primary);
            letter-spacing: -0.3px;
            line-height: 1.1;
        }}

        .title {{
            font-size: 14.5px;
            font-weight: 500;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-top: 5px;
            margin-bottom: 8px;
        }}

        .contact-bar {{
            font-size: 12px;
            color: var(--text-muted);
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
            line-height: 1.5;
        }}

        .contact-bar a {{
            color: var(--text-dark);
            text-decoration: none;
        }}

        .contact-bar a:hover {{
            color: var(--accent);
            text-decoration: underline;
        }}

        .section {{
            margin-bottom: 22px;
            page-break-inside: avoid;
        }}

        .section-title {{
            font-size: 13px;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--primary);
            border-left: 3.5px solid var(--accent);
            padding-left: 10px;
            margin-bottom: 12px;
            letter-spacing: 1px;
        }}

        .summary-content p {{
            font-size: 13px;
            margin-bottom: 8px;
            color: var(--text-dark);
            text-align: justify;
            line-height: 1.6;
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

