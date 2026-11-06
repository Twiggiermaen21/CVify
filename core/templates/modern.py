"""
Modern CV Template.
Clean single-column layout optimized to fit perfectly on a single A4 page with neutral, elegant styling.
"""
from .base_template import BaseTemplate


class ModernTemplate(BaseTemplate):
    """Modern single-column CV template with neutral, executive styling and 1-page fit."""

    def build(self, output_path: str = "nowe_cv.html") -> str:
        # Photo (86x104px)
        photo_html = self._photo_img(size=104, css_class="mod-photo")

        # Contact items
        contact_items = self._contact_items()
        contact_spans = [f'<span class="mod-c-item">{ico} {label}</span>' for ico, label in contact_items]
        contact_html = "".join(contact_spans)

        # Header layout
        header_html = f"""
        <header class="mod-header">
            <div class="mod-header-text">
                <h1 class="mod-name">{self.esc(self.info.name or "Kacper Pudełko")}</h1>
                {f'<div class="mod-title">{self.esc(self.info.title)}</div>' if self.info.title else ''}
                <div class="mod-contacts">{contact_html}</div>
            </div>
            {f'<div class="mod-header-photo">{photo_html}</div>' if photo_html else ''}
        </header>"""

        # Summary / Profil zawodowy
        summary_html = ""
        if self.data.summary:
            summary_html = f"""
            <section class="mod-sec">
                <h2 class="mod-sec-title">Profil zawodowy</h2>
                <p class="mod-summary">{self.esc(self.data.summary.strip())}</p>
            </section>"""

        # Experience
        exp_html = ""
        if self.data.experience:
            cards = []
            for item in self.data.experience:
                comp_loc = self.esc(item.company)
                if item.location:
                    comp_loc += f", {self.esc(item.location)}"
                bullets = "".join(f"<li>{self.esc(b)}</li>" for b in item.description)
                cards.append(f"""
                <div class="mod-entry">
                    <div class="mod-entry-head">
                        <div>
                            <span class="mod-role">{self.esc(item.role)}</span>
                            <span class="mod-comp"> | {comp_loc}</span>
                        </div>
                        <span class="mod-date">{self.esc(item.period)}</span>
                    </div>
                    <ul class="mod-bullets">{bullets}</ul>
                </div>""")
            exp_html = f"""
            <section class="mod-sec">
                <h2 class="mod-sec-title">Doświadczenie zawodowe</h2>
                {"".join(cards)}
            </section>"""

        # Startups
        startups_html = ""
        if self.data.startups:
            cards = []
            for item in self.data.startups:
                role_part = f" | {self.esc(item.role)}" if item.role else ""
                period_part = f'<span class="mod-date">{self.esc(item.period)}</span>' if item.period else ""
                bullets = "".join(f"<li>{self.esc(b)}</li>" for b in item.description)
                cards.append(f"""
                <div class="mod-entry">
                    <div class="mod-entry-head">
                        <div>
                            <span class="mod-role">{self.esc(item.name)}</span>
                            <span class="mod-comp">{role_part}</span>
                        </div>
                        {period_part}
                    </div>
                    <ul class="mod-bullets">{bullets}</ul>
                </div>""")
            startups_html = f"""
            <section class="mod-sec">
                <h2 class="mod-sec-title">Start-up & Własne Inicjatywy</h2>
                {"".join(cards)}
            </section>"""

        # Selected Projects
        projects_html = ""
        if self.data.projects:
            cards = []
            for item in self.data.projects:
                link = ""
                if item.url:
                    clean_url = item.url.replace("https://", "").replace("http://", "").rstrip("/")
                    ico = self.ICO_GITHUB if "github.com" in clean_url else self.ICO_LINK
                    link = f'<a class="mod-proj-link" href="{self.esc(item.url)}" target="_blank" rel="noopener">{ico} {self.esc(clean_url)}</a>'
                tags = "".join(f'<span class="mod-pill">{self.esc(t)}</span>' for t in item.tech_stack) if item.tech_stack else ""
                desc = f'<div class="mod-proj-desc">{self.esc(item.description)}</div>' if item.description else ""
                cards.append(f"""
                <div class="mod-proj-item">
                    <div class="mod-proj-head">
                        <span class="mod-role">{self.esc(item.name)}</span>
                        <div class="mod-proj-tags">{tags}</div>
                        {link}
                    </div>
                    {desc}
                </div>""")
            projects_html = f"""
            <section class="mod-sec">
                <h2 class="mod-sec-title">Wybrane projekty własne</h2>
                {"".join(cards)}
            </section>"""

        # Technical Skills
        skills_html = ""
        if self.data.skills_categorized:
            rows = []
            for cat, sks in self.data.skills_categorized.items():
                pills = "".join(f'<span class="mod-pill">{self.esc(s)}</span>' for s in sks)
                rows.append(f"""
                <div class="mod-skill-row">
                    <span class="mod-skill-cat">{self.esc(cat)}:</span>
                    <div class="mod-skill-pills">{pills}</div>
                </div>""")
            skills_html = f"""
            <section class="mod-sec">
                <h2 class="mod-sec-title">Umiejętności techniczne</h2>
                <div class="mod-skills-block">{"".join(rows)}</div>
            </section>"""
        elif self.data.skills_technical:
            pills = "".join(f'<span class="mod-pill">{self.esc(s)}</span>' for s in self.data.skills_technical)
            skills_html = f"""
            <section class="mod-sec">
                <h2 class="mod-sec-title">Umiejętności techniczne</h2>
                <div class="mod-skill-pills">{pills}</div>
            </section>"""

        # Education & Languages in a balanced 2-column bottom row
        edu_html = ""
        if self.data.education:
            edu_cards = []
            for item in self.data.education:
                inst = self.esc(item.institution)
                if item.location:
                    inst += f", {self.esc(item.location)}"
                edu_cards.append(f"""
                <div class="mod-edu-item">
                    <div class="mod-edu-head">
                        <span class="mod-edu-deg">{self.esc(item.degree)}</span>
                        <span class="mod-date">{self.esc(item.period)}</span>
                    </div>
                    <div class="mod-edu-inst">{inst}</div>
                </div>""")
            edu_html = "".join(edu_cards)

        lang_html = ""
        if self.data.languages:
            lang_items = []
            for lg in self.data.languages:
                lvl = f": <b>{self.esc(lg.level)}</b>" if lg.level else ""
                lang_items.append(f'<span class="mod-lang-pill">{self.esc(lg.language)}{lvl}</span>')
            lang_html = "".join(lang_items)

        bottom_split_html = f"""
        <div class="mod-split-row">
            <div class="mod-split-col mod-col-edu">
                <h2 class="mod-sec-title">Wykształcenie</h2>
                {edu_html}
            </div>
            <div class="mod-split-col mod-col-lang">
                <h2 class="mod-sec-title">Języki obce</h2>
                <div class="mod-lang-wrap">{lang_html}</div>
            </div>
        </div>"""

        # RODO clause
        clause_html = f'<div class="mod-rodo">{self.esc(self.data.clause)}</div>' if self.data.clause else ""

        css = f"""
        {self._css_variables()}
        {self._css_reset()}

        body {{
            background: #f1f5f9;
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', Roboto, Arial, sans-serif;
            color: #1e293b;
            line-height: 1.38;
            -webkit-font-smoothing: antialiased;
        }}

        .cv-container {{
            max-width: 820px;
            margin: 16px auto;
            background: #ffffff;
            padding: 26px 32px 20px 32px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
            border-radius: 6px;
            box-sizing: border-box;
        }}

        /* Header */
        .mod-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            border-bottom: 2px solid #0f172a;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }}

        .mod-header-text {{
            flex: 1;
        }}

        .mod-header-photo {{
            flex-shrink: 0;
        }}

        .mod-photo {{
            width: 84px;
            height: 100px;
            object-fit: cover;
            border-radius: 6px;
            border: 2px solid #e2e8f0;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            display: block;
        }}

        .mod-photo-placeholder {{
            width: 84px;
            height: 100px;
            border-radius: 6px;
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }}

        .mod-name {{
            font-size: 26px;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.3px;
            line-height: 1.15;
            text-transform: uppercase;
            margin: 0;
        }}

        .mod-title {{
            font-size: 13px;
            font-weight: 600;
            color: #475569;
            margin-top: 3px;
            margin-bottom: 6px;
            letter-spacing: 0.2px;
        }}

        .mod-contacts {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px 14px;
            font-size: 10.4px;
            color: #475569;
            align-items: center;
            line-height: 1.4;
        }}

        .mod-c-item {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            color: #334155;
        }}

        .mod-c-item a {{
            color: #1e293b;
            text-decoration: none;
            font-weight: 500;
        }}

        .mod-c-item a:hover {{
            text-decoration: underline;
        }}

        /* Section Headings */
        .mod-sec {{
            margin-bottom: 10px;
            page-break-inside: avoid;
        }}

        .mod-sec-title {{
            font-size: 11.6px;
            font-weight: 800;
            text-transform: uppercase;
            color: #0f172a;
            letter-spacing: 0.8px;
            border-bottom: 1.5px solid #0f172a;
            padding-bottom: 3px;
            margin-top: 0;
            margin-bottom: 5px;
        }}

        /* Summary */
        .mod-summary {{
            font-size: 10.2px;
            line-height: 1.44;
            color: #334155;
            text-align: justify;
            margin: 0;
        }}

        /* Entries (Experience & Startup) */
        .mod-entry {{
            margin-bottom: 6.5px;
            page-break-inside: avoid;
        }}

        .mod-entry-head {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 8px;
        }}

        .mod-role {{
            font-size: 11.2px;
            font-weight: 700;
            color: #0f172a;
        }}

        .mod-comp {{
            font-size: 10.5px;
            font-weight: 500;
            color: #475569;
        }}

        .mod-date {{
            font-size: 10px;
            font-weight: 500;
            color: #64748b;
            white-space: nowrap;
            font-style: italic;
        }}

        .mod-bullets {{
            list-style: disc;
            margin-left: 15px;
            margin-top: 2px;
            margin-bottom: 0;
            padding: 0;
        }}

        .mod-bullets li {{
            font-size: 10.1px;
            line-height: 1.38;
            color: #334155;
            margin-bottom: 2px;
            text-align: justify;
        }}

        /* Projects */
        .mod-proj-item {{
            margin-bottom: 6px;
            page-break-inside: avoid;
        }}

        .mod-proj-head {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .mod-proj-tags {{
            display: inline-flex;
            gap: 3.5px;
            flex-wrap: wrap;
        }}

        .mod-pill {{
            font-size: 9.6px;
            padding: 2px 6.5px;
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 3px;
            color: #334155;
            font-weight: 500;
            white-space: nowrap;
            display: inline-block;
        }}

        .mod-proj-link {{
            font-size: 9.8px;
            color: #0f172a;
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 3px;
            margin-left: auto;
        }}

        .mod-proj-link:hover {{
            text-decoration: underline;
        }}

        .mod-proj-desc {{
            font-size: 10px;
            line-height: 1.38;
            color: #475569;
            margin-top: 2px;
            text-align: justify;
        }}

        /* Skills */
        .mod-skills-block {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .mod-skill-row {{
            display: flex;
            align-items: baseline;
            gap: 8px;
        }}

        .mod-skill-cat {{
            font-size: 10.2px;
            font-weight: 700;
            color: #0f172a;
            width: 148px;
            flex-shrink: 0;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}

        .mod-skill-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: 3.5px;
        }}

        /* Split bottom row for Education & Languages */
        .mod-split-row {{
            display: flex;
            gap: 16px;
            margin-top: 4px;
            page-break-inside: avoid;
        }}

        .mod-col-edu {{
            flex: 63;
        }}

        .mod-col-lang {{
            flex: 37;
        }}

        .mod-edu-item {{
            margin-bottom: 5px;
        }}

        .mod-edu-head {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 6px;
        }}

        .mod-edu-deg {{
            font-size: 10.5px;
            font-weight: 700;
            color: #0f172a;
        }}

        .mod-edu-inst {{
            font-size: 9.8px;
            color: #475569;
        }}

        .mod-lang-wrap {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .mod-lang-pill {{
            font-size: 10.2px;
            color: #1e293b;
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 3px;
            padding: 2.5px 8px;
            display: inline-block;
        }}

        /* RODO */
        .mod-rodo {{
            font-size: 8.2px;
            line-height: 1.3;
            color: #94a3b8;
            font-style: italic;
            border-top: 1px solid #e2e8f0;
            padding-top: 5px;
            margin-top: 8px;
            text-align: justify;
        }}

        {self._css_common_components()}
        {self._css_print_button()}
        {self._css_print_base()}

        @page {{
            size: A4 portrait;
            margin: 0;
        }}

        @media print {{
            @page {{
                size: A4 portrait;
                margin: 0;
            }}
            * {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}
            body {{
                background: #ffffff !important;
                padding: 0 !important;
                margin: 0 !important;
            }}
            .cv-container {{
                box-shadow: none !important;
                border: none !important;
                margin: 0 !important;
                padding: 24px 28px 16px 28px !important;
                max-width: 100% !important;
                width: 100% !important;
            }}
            .print-btn {{
                display: none !important;
            }}
        }}
        """

        full_html = f"""{self._html_head(css)}
<body>
    {self._print_button()}
    <div class="cv-container">
        {header_html}
        {summary_html}
        {exp_html}
        {startups_html}
        {projects_html}
        {skills_html}
        {bottom_split_html}
        {clause_html}
    </div>
</body>
</html>"""
        return self._write(output_path, full_html)
