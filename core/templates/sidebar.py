"""
Sidebar (2-column) CV Template.
Features a left colored sidebar with photo, contact info, skills, and languages.
The right column holds the name, title, summary, experience, projects, and education.
Uses a rock-solid table-based column layout to ensure pixel-perfect PDF export without breaks.
"""
from .base_template import BaseTemplate


class SidebarTemplate(BaseTemplate):
    """Two-column sidebar template using table layout for bulletproof PDF printing."""

    def build(self, output_path: str = "nowe_cv.html") -> str:
        photo_html = self._photo_img(size=110, css_class="sidebar-photo")

        # Contact items for sidebar (vertical)
        contact_items_html = ""
        items = self._contact_items()
        if items:
            rows = [f'<div class="sidebar-contact-item"><span class="c-icon">{emoji}</span><span class="c-text">{label}</span></div>' for emoji, label in items]
            contact_items_html = "\n".join(rows)

        # Skills for sidebar
        sidebar_skills_html = ""
        if self.data.skills_categorized:
            cat_blocks = []
            for cat_name, sks in self.data.skills_categorized.items():
                pills = "".join(f'<span class="sidebar-pill">{self.esc(s)}</span>' for s in sks)
                cat_blocks.append(f"""
                <div class="sidebar-skill-group">
                    <div class="sidebar-subheading">{self.esc(cat_name)}</div>
                    <div class="sidebar-pill-wrap">{pills}</div>
                </div>""")
            sidebar_skills_html = "\n".join(cat_blocks)
        elif self.data.skills_technical:
            pills = "".join(f'<span class="sidebar-pill">{self.esc(s)}</span>' for s in self.data.skills_technical)
            sidebar_skills_html = f'<div class="sidebar-pill-wrap">{pills}</div>'

        if self.data.skills_soft:
            soft_pills = "".join(f'<span class="sidebar-pill soft">{self.esc(s)}</span>' for s in self.data.skills_soft)
            sidebar_skills_html += f"""
            <div class="sidebar-skill-group">
                <div class="sidebar-subheading">Umiejętności miękkie</div>
                <div class="sidebar-pill-wrap">{soft_pills}</div>
            </div>"""

        # Languages for sidebar
        sidebar_languages_html = ""
        if self.data.languages:
            lang_rows = []
            for lang in self.data.languages:
                lvl = f'<div class="lang-level">{self.esc(lang.level)}</div>' if lang.level else ""
                lang_rows.append(f"""
                <div class="sidebar-lang-item">
                    <div class="lang-name">{self.esc(lang.language)}</div>
                    {lvl}
                </div>""")
            sidebar_languages_html = "\n".join(lang_rows)

        # Main Column Sections
        # Summary
        summary_html = ""
        if self.data.summary:
            summary_html = f"""
            <div class="main-section">
                <h2 class="main-section-title">Profil zawodowy</h2>
                <div class="summary-content">{self._summary_content()}</div>
            </div>"""

        # Experience
        exp_entries = self._experience_entries()
        experience_html = ""
        if exp_entries:
            experience_html = f"""
            <div class="main-section">
                <h2 class="main-section-title">Doświadczenie zawodowe</h2>
                {exp_entries}
            </div>"""

        # Startups
        st_entries = self._startup_entries()
        startups_html = ""
        if st_entries:
            startups_html = f"""
            <div class="main-section">
                <h2 class="main-section-title">Start-up & Własne Inicjatywy</h2>
                {st_entries}
            </div>"""

        # Projects
        pr_entries = self._project_entries()
        projects_html = ""
        if pr_entries:
            projects_html = f"""
            <div class="main-section">
                <h2 class="main-section-title">Wybrane Projekty</h2>
                {pr_entries}
            </div>"""

        # Education
        edu_entries = self._education_entries()
        education_html = ""
        if edu_entries:
            education_html = f"""
            <div class="main-section">
                <h2 class="main-section-title">Wykształcenie</h2>
                {edu_entries}
            </div>"""

        # Certifications
        cert_content = self._certifications_html()
        cert_html = ""
        if cert_content:
            cert_html = f"""
            <div class="main-section">
                <h2 class="main-section-title">Certyfikaty</h2>
                {cert_content}
            </div>"""

        css = f"""
        {self._css_variables()}
        {self._css_reset()}

        .cv-container {{
            max-width: 900px;
            margin: 0 auto;
            background: #ffffff;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
            border-radius: 8px;
            overflow: hidden;
        }}

        /* Table layout for printing stability */
        .cv-layout-table {{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            table-layout: fixed;
        }}

        .cv-sidebar-col {{
            width: 32%;
            background: var(--primary);
            color: #ffffff;
            padding: 32px 22px;
            vertical-align: top;
            box-sizing: border-box;
        }}

        .cv-main-col {{
            width: 68%;
            background: #ffffff;
            padding: 34px 34px;
            vertical-align: top;
            box-sizing: border-box;
        }}

        /* Sidebar Elements */
        .sidebar-photo-container {{
            text-align: center;
            margin-bottom: 20px;
        }}

        .sidebar-photo {{
            border: 3px solid rgba(255, 255, 255, 0.25);
            box-shadow: 0 3px 10px rgba(0,0,0,0.3);
        }}

        .sidebar-heading {{
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 700;
            color: #ffffff;
            border-bottom: 1.5px solid rgba(255, 255, 255, 0.25);
            padding-bottom: 4px;
            margin-top: 22px;
            margin-bottom: 12px;
        }}

        .sidebar-contact-item {{
            display: flex;
            align-items: baseline;
            gap: 8px;
            font-size: 11.5px;
            color: #e2e8f0;
            margin-bottom: 8px;
            line-height: 1.4;
            word-break: break-all;
        }}

        .sidebar-contact-item a {{
            color: #ffffff;
            text-decoration: none;
        }}

        .sidebar-contact-item a:hover {{
            text-decoration: underline;
        }}

        .c-icon {{
            font-size: 12px;
            flex-shrink: 0;
        }}

        .sidebar-subheading {{
            font-size: 11px;
            font-weight: 700;
            color: #cbd5e0;
            text-transform: uppercase;
            margin-top: 8px;
            margin-bottom: 4px;
        }}

        .sidebar-pill-wrap {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
            margin-bottom: 6px;
        }}

        .sidebar-pill {{
            background: rgba(255, 255, 255, 0.12);
            color: #ffffff;
            font-size: 11px;
            padding: 2px 7px;
            border-radius: 4px;
            border: 1px solid rgba(255, 255, 255, 0.18);
        }}

        .sidebar-pill.soft {{
            background: rgba(255, 255, 255, 0.07);
            font-size: 10.5px;
            color: #e2e8f0;
        }}

        .sidebar-lang-item {{
            margin-bottom: 8px;
        }}

        .lang-name {{
            font-size: 12px;
            font-weight: 700;
            color: #ffffff;
        }}

        .lang-level {{
            font-size: 11px;
            color: #cbd5e0;
        }}

        /* Main Elements */
        .main-header {{
            border-bottom: 2px solid var(--accent);
            padding-bottom: 12px;
            margin-bottom: 18px;
        }}

        .main-name {{
            font-size: 27px;
            font-weight: 800;
            color: var(--primary);
            letter-spacing: -0.5px;
            line-height: 1.15;
        }}

        .main-title {{
            font-size: 15px;
            font-weight: 600;
            color: var(--accent);
            margin-top: 4px;
            letter-spacing: 0.2px;
        }}

        .main-section {{
            margin-bottom: 18px;
            page-break-inside: avoid;
        }}

        .main-section-title {{
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

        @media print {{
            .cv-sidebar-col {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                background-color: {self.primary} !important;
                color: #ffffff !important;
            }}
            .sidebar-pill {{
                background-color: rgba(255, 255, 255, 0.15) !important;
                color: #ffffff !important;
                border: 1px solid rgba(255, 255, 255, 0.3) !important;
            }}
        }}
        """

        full_html = f"""{self._html_head(css)}
<body>
    {self._print_button()}
    <div class="cv-container">
        <table class="cv-layout-table">
            <tr>
                <!-- LEFT SIDEBAR -->
                <td class="cv-sidebar-col">
                    {f'<div class="sidebar-photo-container">{photo_html}</div>' if photo_html else ''}
                    
                    <div class="sidebar-heading">Kontakt</div>
                    {contact_items_html}

                    {f'<div class="sidebar-heading">Języki obce</div>{sidebar_languages_html}' if sidebar_languages_html else ''}
                    {f'<div class="sidebar-heading">Umiejętności techniczne</div>{sidebar_skills_html}' if sidebar_skills_html else ''}
                </td>

                <!-- RIGHT MAIN CONTENT -->
                <td class="cv-main-col">
                    <header class="main-header">
                        <h1 class="main-name">{self.esc(self.info.name or "Kacper Pudełko")}</h1>
                        {f'<div class="main-title">{self.esc(self.info.title)}</div>' if self.info.title else ''}
                    </header>

                    {summary_html}
                    {experience_html}
                    {startups_html}
                    {projects_html}
                    {education_html}
                    {cert_html}
                    {self._clause_html()}
                </td>
            </tr>
        </table>
    </div>
</body>
</html>"""
        return self._write(output_path, full_html)

