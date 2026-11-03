"""
Onyx Dark Sidebar Template.
Direct 1:1 recreation of Image 1 (Laura Kubiak black style):
- Deep black left sidebar with rounded-rectangle photo
- White section titles with thin underlines
- Contact items with circular icons
- Clean white right column with checkmark-bulleted experience and skill entries
- Table-based layout for rock-solid PDF printing
"""
from .base_template import BaseTemplate


class OnyxTemplate(BaseTemplate):
    """Deep black sidebar template with high contrast checkmark typography."""

    CHECK_SVG = '<svg class="onyx-check-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#111111"/><path d="m7 12 3.5 3.5 6.5-7" stroke="#ffffff" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'

    def build(self, output_path: str = "nowe_cv.html") -> str:
        # Photo: rounded rectangle
        photo_uri = self._photo_base64()
        if photo_uri:
            photo_html = f'<div class="onyx-photo-wrap"><img src="{photo_uri}" alt="{self.esc(self.info.name)}" class="onyx-photo"></div>'
        else:
            photo_html = ""

        # Contact items for black sidebar
        contact_rows = []
        info = self.info
        if info.phone:
            contact_rows.append(f'<div class="sb-contact-row"><span class="sb-icon">{self.ICO_PHONE}</span><span><a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a></span></div>')
        if info.email:
            contact_rows.append(f'<div class="sb-contact-row"><span class="sb-icon">{self.ICO_MAIL}</span><span><a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a></span></div>')
        if info.location:
            contact_rows.append(f'<div class="sb-contact-row"><span class="sb-icon">{self.ICO_PIN}</span><span>{self.esc(info.location)}</span></div>')
        if info.linkedin:
            lbl = info.linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_rows.append(f'<div class="sb-contact-row"><span class="sb-icon">{self.ICO_LINKEDIN}</span><span><a href="{self.esc(info.linkedin)}" target="_blank">{self.esc(lbl)}</a></span></div>')
        if info.github:
            lbl = info.github.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_rows.append(f'<div class="sb-contact-row"><span class="sb-icon">{self.ICO_GITHUB}</span><span><a href="{self.esc(info.github)}" target="_blank">{self.esc(lbl)}</a></span></div>')
        if info.driver_license:
            contact_rows.append(f'<div class="sb-contact-row"><span class="sb-icon">{self.ICO_CAR}</span><span>Prawo jazdy: {self.esc(info.driver_license)}</span></div>')
        
        contact_html = "\n".join(contact_rows)

        # Education for sidebar
        edu_rows = []
        for ed in self.data.education:
            inst = self.esc(ed.institution)
            loc = f", {self.esc(ed.location)}" if ed.location else ""
            edu_rows.append(f"""
            <div class="sb-edu-item">
                <div class="sb-edu-degree">{self.esc(ed.degree)}</div>
                <div class="sb-edu-inst">{inst}{loc}</div>
                <div class="sb-edu-date">{self.esc(ed.period)}</div>
            </div>""")
        edu_html = "\n".join(edu_rows)

        # Languages for sidebar
        lang_rows = []
        for lg in self.data.languages:
            lvl = f'<div class="sb-lang-level">{self.esc(lg.level)}</div>' if lg.level else ""
            lang_rows.append(f"""
            <div class="sb-lang-item">
                <div class="sb-lang-name">{self.esc(lg.language)}</div>
                {lvl}
            </div>""")
        lang_html = "\n".join(lang_rows)

        # Soft Skills / Interests for sidebar
        soft_rows = []
        if self.data.skills_soft:
            for s in self.data.skills_soft:
                soft_rows.append(f'<li class="sb-bullet">{self.esc(s)}</li>')
        soft_html = f'<ul class="sb-list">{"".join(soft_rows)}</ul>' if soft_rows else ""

        # RIGHT COLUMN: Experience with checkmark badges
        exp_rows = []
        for exp in self.data.experience:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in exp.description)
            comp_loc = self.esc(exp.company)
            if exp.location:
                comp_loc += f", {self.esc(exp.location)}"
            exp_rows.append(f"""
            <div class="onyx-entry">
                <div class="onyx-entry-header">
                    <span class="onyx-check">{self.CHECK_SVG}</span>
                    <span class="onyx-check">{self.CHECK_SVG}</span>
                    <div class="onyx-title-block">
                        <span class="onyx-role">{self.esc(exp.role)}, {comp_loc}</span>
                        <div class="onyx-period">{self.esc(exp.period)}</div>
                    </div>
                </div>
                <ul class="onyx-bullets">{bullets}</ul>
            </div>""")
        experience_html = "\n".join(exp_rows)

        # Startups
        st_rows = []
        for st in self.data.startups:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in st.description)
            tech = ""
            if st.tech_stack:
                tech = f'<div class="onyx-tech">Tech: {self.esc(", ".join(st.tech_stack))}</div>'
            st_rows.append(f"""
            <div class="onyx-entry">
                <div class="onyx-entry-header">
                    <span class="onyx-check">{self.CHECK_SVG}</span>
                    <span class="onyx-check">{self.CHECK_SVG}</span>
                    <div class="onyx-title-block">
                        <span class="onyx-role">{self.esc(st.name)}</span>
                        {f'<div class="onyx-period">{self.esc(st.period)}</div>' if st.period else ''}
                    </div>
                </div>
                {tech}
                <ul class="onyx-bullets">{bullets}</ul>
            </div>""")
        startups_html = "\n".join(st_rows)

        # Projects
        proj_rows = []
        for pr in self.data.projects:
            if pr.url:
                clean_url = pr.url.replace("https://", "").replace("http://", "").rstrip("/")
                icon = self.ICO_GITHUB if "github.com" in clean_url else self.ICO_LINK
                link = f'<a class="onyx-link" href="{self.esc(pr.url)}" target="_blank" rel="noopener">{icon} {self.esc(clean_url)}</a>'
            else:
                link = ""
            tech = f'<div class="onyx-tech">[{self.esc(", ".join(pr.tech_stack))}]</div>' if pr.tech_stack else ""
            desc = f'<p class="onyx-proj-desc">{self.esc(pr.description)}</p>' if pr.description else ""
            proj_rows.append(f"""
            <div class="onyx-entry">
                <div class="onyx-entry-header">
                    <span class="onyx-check">{self.CHECK_SVG}</span>
                    <span class="onyx-check">{self.CHECK_SVG}</span>
                    <div class="onyx-title-block">
                        <span class="onyx-role">{self.esc(pr.name)}</span>
                        {link}
                    </div>
                </div>
                {tech}
                {desc}
            </div>""")
        projects_html = "\n".join(proj_rows)

        # Categorized Skills for main column
        skills_main_html = ""
        if self.data.skills_categorized:
            for cat_name, sks in self.data.skills_categorized.items():
                items = "".join(f"<li>{self.esc(s)}</li>" for s in sks)
                skills_main_html += f"""
                <div class="onyx-skill-group">
                    <div class="onyx-skill-cat-title"><span class="onyx-check">{self.CHECK_SVG}</span> <strong>{self.esc(cat_name)}:</strong></div>
                    <div class="onyx-skill-cat-title"><span class="onyx-check">{self.CHECK_SVG}</span> <strong>{self.esc(cat_name)}:</strong></div>
                    <ul class="onyx-bullets-sub">{items}</ul>
                </div>"""
        elif self.data.skills_technical:
            items = "".join(f"<li>{self.esc(s)}</li>" for s in self.data.skills_technical)
            skills_main_html = f"""
            <div class="onyx-skill-group">
                <div class="onyx-skill-cat-title"><span class="onyx-check">{self.CHECK_SVG}</span> <strong>Umiejętności techniczne:</strong></div>
                <div class="onyx-skill-cat-title"><span class="onyx-check">{self.CHECK_SVG}</span> <strong>Umiejętności techniczne:</strong></div>
                <ul class="onyx-bullets-sub">{items}</ul>
            </div>"""

        css = f"""
        {self._css_variables()}
        {self._css_reset()}

        .cv-container {{
            max-width: 890px;
            margin: 0 auto;
            background: #ffffff;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
            border-radius: 4px;
            overflow: hidden;
        }}

        .onyx-table {{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            table-layout: fixed;
        }}

        /* Left Black Sidebar */
        .onyx-sidebar {{
            width: 34%;
            background-color: #16181b;
            color: #ffffff;
            padding: 34px 24px;
            vertical-align: top;
            box-sizing: border-box;
        }}

        .onyx-photo-wrap {{
            text-align: center;
            margin-bottom: 24px;
        }}

        .onyx-photo {{
            width: 135px;
            height: 155px;
            object-fit: cover;
            border-radius: 14px;
            display: inline-block;
            border: 2px solid rgba(255, 255, 255, 0.15);
        }}

        .onyx-sb-title {{
            font-size: 13px;
            text-transform: uppercase;
            font-weight: 800;
            letter-spacing: 1.2px;
            color: #ffffff;
            border-bottom: 1px solid rgba(255, 255, 255, 0.35);
            padding-bottom: 4px;
            margin-top: 24px;
            margin-bottom: 12px;
        }}

        .sb-contact-row {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 11.5px;
            color: #e2e8f0;
            margin-bottom: 10px;
            line-height: 1.4;
            word-break: break-all;
        }}

        .sb-contact-row a {{
            color: #ffffff;
            text-decoration: none;
        }}

        .sb-contact-row a:hover {{
            text-decoration: underline;
        }}

        .sb-icon {{
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.15);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            flex-shrink: 0;
            color: #ffffff;
        }}

        .sb-icon svg {{
            width: 12px;
            height: 12px;
            stroke: #ffffff;
            margin-right: 0;
        }}

        .sb-edu-item {{
            margin-bottom: 12px;
        }}

        .sb-edu-degree {{
            font-size: 12px;
            font-weight: 700;
            color: #ffffff;
        }}

        .sb-edu-inst {{
            font-size: 11px;
            color: #cbd5e0;
        }}

        .sb-edu-date {{
            font-size: 10.5px;
            color: #a0aec0;
            font-style: italic;
        }}

        .sb-lang-item {{
            margin-bottom: 10px;
        }}

        .sb-lang-name {{
            font-size: 12px;
            font-weight: 700;
            color: #ffffff;
        }}

        .sb-lang-level {{
            font-size: 11px;
            color: #cbd5e0;
        }}

        .sb-list {{
            list-style: none;
            padding-left: 0;
        }}

        .sb-bullet {{
            font-size: 11px;
            color: #e2e8f0;
            margin-bottom: 5px;
            position: relative;
            padding-left: 14px;
        }}

        .sb-bullet::before {{
            content: "•";
            position: absolute;
            left: 0;
            color: rgba(255, 255, 255, 0.6);
        }}

        /* Right Column */
        .onyx-main {{
            width: 66%;
            background-color: #ffffff;
            color: #2d3748;
            padding: 38px 36px;
            vertical-align: top;
            box-sizing: border-box;
        }}

        .onyx-name {{
            font-size: 32px;
            font-weight: 900;
            color: #111111;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            line-height: 1.1;
            margin-bottom: 4px;
        }}

        .onyx-title {{
            font-size: 14.5px;
            font-weight: 700;
            color: #4a5568;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 14px;
        }}

        .onyx-summary {{
            font-size: 12.5px;
            color: #4a5568;
            text-align: justify;
            line-height: 1.55;
            margin-bottom: 24px;
        }}

        .onyx-section-title {{
            font-size: 13.5px;
            font-weight: 800;
            color: #111111;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            border-bottom: 1.5px solid #111111;
            padding-bottom: 4px;
            margin-top: 20px;
            margin-bottom: 14px;
        }}

        .onyx-entry {{
            margin-bottom: 14px;
            page-break-inside: avoid;
        }}

        .onyx-entry-header {{
            display: flex;
            align-items: baseline;
            gap: 8px;
            margin-bottom: 4px;
        }}

        .onyx-check {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 15px;
            height: 15px;
            border-radius: 50%;
            background: #111111;
            color: #ffffff;
            font-size: 9px;
            font-weight: 900;
            flex-shrink: 0;
            line-height: 0;
        }}

        .onyx-check-svg {{
            width: 15px;
            height: 15px;
            display: block;
        }}

        .onyx-role {{
            font-size: 13px;
            font-weight: 700;
            color: #111111;
        }}

        .onyx-period {{
            font-size: 11px;
            color: #718096;
            margin-top: 1px;
        }}

        .onyx-bullets {{
            list-style-type: disc;
            margin-left: 36px;
            font-size: 12px;
            color: #2d3748;
            line-height: 1.45;
        }}

        .onyx-bullets li {{
            margin-bottom: 3px;
        }}

        .onyx-bullets-sub {{
            list-style-type: circle;
            margin-left: 38px;
            font-size: 12px;
            color: #2d3748;
            margin-bottom: 8px;
        }}

        .onyx-bullets-sub li {{
            margin-bottom: 2px;
        }}

        .onyx-skill-group {{
            margin-bottom: 10px;
            page-break-inside: avoid;
        }}

        .onyx-skill-cat-title {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12.5px;
            color: #111111;
            margin-bottom: 4px;
        }}

        .onyx-tech {{
            font-size: 11px;
            color: #718096;
            margin-left: 23px;
            margin-bottom: 3px;
        }}

        .onyx-proj-desc {{
            font-size: 12px;
            color: #2d3748;
            margin-left: 23px;
            margin-top: 2px;
            text-align: justify;
        }}

        .onyx-link {{
            font-size: 11.5px;
            color: #2b6cb0;
            text-decoration: none;
            margin-left: 6px;
        }}

        .onyx-rodo {{
            margin-top: 26px;
            padding-top: 10px;
            border-top: 1px solid #e2e8f0;
            font-size: 10px;
            color: #a0aec0;
            font-style: italic;
            text-align: justify;
            line-height: 1.4;
        }}

        {self._css_print_button()}
        {self._css_print_base()}

        @media print {{
            .onyx-sidebar {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                background-color: #16181b !important;
                color: #ffffff !important;
            }}
            .onyx-check {{
                background-color: #111111 !important;
                color: #ffffff !important;
            }}
        }}
        """

        summary_p = f'<div class="onyx-summary">{self._summary_content()}</div>' if self.data.summary else ""

        full_html = f"""{self._html_head(css)}
<body>
    {self._print_button()}
    <div class="cv-container">
        <table class="onyx-table">
            <tr>
                <!-- LEFT BLACK SIDEBAR -->
                <td class="onyx-sidebar">
                    {photo_html}

                    <div class="onyx-sb-title">Kontakt</div>
                    {contact_html}

                    {f'<div class="onyx-sb-title">Wykształcenie</div>{edu_html}' if edu_html else ''}
                    {f'<div class="onyx-sb-title">Języki</div>{lang_html}' if lang_html else ''}
                    {f'<div class="onyx-sb-title">Umiejętności miękkie</div>{soft_html}' if soft_html else ''}
                </td>

                <!-- RIGHT MAIN COLUMN -->
                <td class="onyx-main">
                    <h1 class="onyx-name">{self.esc(self.info.name or "Kacper Pudełko")}</h1>
                    {f'<div class="onyx-title">{self.esc(self.info.title)}</div>' if self.info.title else ''}
                    {summary_p}

                    {f'<div class="onyx-section-title">Doświadczenie zawodowe</div>{experience_html}' if experience_html else ''}
                    {f'<div class="onyx-section-title">Start-up & Inicjatywy</div>{startups_html}' if startups_html else ''}
                    {f'<div class="onyx-section-title">Wybrane Projekty</div>{projects_html}' if projects_html else ''}
                    {f'<div class="onyx-section-title">Umiejętności</div>{skills_main_html}' if skills_main_html else ''}

                    {f'<div class="onyx-rodo">{self.esc(self.data.clause)}</div>' if self.data.clause else ''}
                </td>
            </tr>
        </table>
    </div>
</body>
</html>"""
        return self._write(output_path, full_html)

