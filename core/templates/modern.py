"""
Modern CV Template.
Clean single-column layout with photo support, modern badge styles, and colored accents.
"""
from .base_template import BaseTemplate


class ModernTemplate(BaseTemplate):
    """Modern single-column CV template with accent highlights."""

    def build(self, output_path: str = "nowe_cv.html") -> str:
        photo_html = self._photo_img(size=96, css_class="profile-photo")

        # Contact Bar
        contact_bar = self._contact_bar_html(" &bull; ")

        # Summary
        summary_html = ""
        if self.data.summary:
            summary_html = f"""
            <section class="section">
                <h2 class="section-title">Profil zawodowy</h2>
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
                <h2 class="section-title">Start-up & Własne Inicjatywy</h2>
                {st_entries}
            </section>"""

        # Projects
        pr_entries = self._project_entries()
        projects_html = ""
        if pr_entries:
            projects_html = f"""
            <section class="section">
                <h2 class="section-title">Wybrane Projekty</h2>
                {pr_entries}
            </section>"""

        # Skills
        sk_content = self._skills_html()
        skills_html = ""
        if sk_content:
            skills_html = f"""
            <section class="section">
                <h2 class="section-title">Umiejętności i Technologie</h2>
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

        # Header layout with photo support
        header_content = f"""
        <header class="header">
            <div class="header-main">
                <div class="header-text">
                    <h1 class="name">{self.esc(self.info.name or "Kacper Pudełko")}</h1>
                    {f'<div class="title">{self.esc(self.info.title)}</div>' if self.info.title else ''}
                    <div class="contact-bar">{contact_bar}</div>
                </div>
                {f'<div class="header-photo">{photo_html}</div>' if photo_html else ''}
            </div>
        </header>"""

        css = f"""
        {self._css_variables()}
        {self._css_reset()}

        .cv-container {{
            max-width: 860px;
            margin: 0 auto;
            background: #ffffff;
            padding: 38px 46px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
            border-radius: 8px;
        }}

        .header {{
            border-bottom: 2.5px solid var(--accent);
            padding-bottom: 16px;
            margin-bottom: 20px;
        }}

        .header-main {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
        }}

        .header-text {{
            flex: 1;
        }}

        .header-photo {{
            flex-shrink: 0;
        }}

        .profile-photo {{
            border: 3px solid var(--accent-light);
            box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        }}

        .name {{
            font-size: 27px;
            font-weight: 700;
            color: var(--primary);
            letter-spacing: -0.5px;
            line-height: 1.15;
        }}

        .title {{
            font-size: 15px;
            font-weight: 600;
            color: var(--accent);
            margin-top: 4px;
            margin-bottom: 10px;
            letter-spacing: 0.2px;
        }}

        .contact-bar {{
            font-size: 12.5px;
            color: var(--text-muted);
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
            line-height: 1.6;
        }}

        .contact-bar a {{
            color: var(--accent);
            text-decoration: none;
        }}

        .contact-bar a:hover {{
            text-decoration: underline;
        }}

        .section {{
            margin-bottom: 18px;
            page-break-inside: avoid;
        }}

        .section-title {{
            font-size: 13.5px;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--primary);
            border-bottom: 1.5px solid var(--primary);
            padding-bottom: 4px;
            margin-bottom: 10px;
            letter-spacing: 0.6px;
        }}

        .summary-content p {{
            font-size: 13px;
            margin-bottom: 8px;
            color: var(--text-dark);
            text-align: justify;
            line-height: 1.55;
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

