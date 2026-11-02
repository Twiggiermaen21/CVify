"""
Creative Yellow CV Template.
Direct 1:1 recreation of Image 3 (Anne Robertson yellow agency style):
- Iconic yellow arch behind photo on top left
- Modern uppercase titles with underscore accents (JOB EXPERIENCE_, CONTACT_, SKILLS_)
- Clean geometric hierarchy with vibrant yellow (#f5b800) accents
- Skills with visual rating dots/meters
- Table-based layout for rock-solid PDF printing
"""
from .base_template import BaseTemplate


class CreativeTemplate(BaseTemplate):
    """Creative design agency template with vibrant yellow arch header."""

    def build(self, output_path: str = "nowe_cv.html") -> str:
        photo_uri = self._photo_base64()
        if photo_uri:
            photo_html = f'<img src="{photo_uri}" alt="{self.esc(self.info.name)}" class="cr-photo">'
        else:
            photo_html = '<div class="cr-photo-placeholder">👤</div>'
            photo_html = '<div class="cr-photo-placeholder"></div>'

        info = self.info
        contact_rows = []
        if info.location:
            contact_rows.append(f'<div class="cr-contact-row"><span class="cr-c-icon">📍</span><span>{self.esc(info.location)}</span></div>')
            contact_rows.append(f'<div class="cr-contact-row"><span class="cr-c-icon">{self.ICO_PIN}</span><span>{self.esc(info.location)}</span></div>')
        if info.phone:
            contact_rows.append(f'<div class="cr-contact-row"><span class="cr-c-icon">📞</span><span><a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a></span></div>')
            contact_rows.append(f'<div class="cr-contact-row"><span class="cr-c-icon">{self.ICO_PHONE}</span><span><a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a></span></div>')
        if info.email:
            contact_rows.append(f'<div class="cr-contact-row"><span class="cr-c-icon">✉</span><span><a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a></span></div>')
            contact_rows.append(f'<div class="cr-contact-row"><span class="cr-c-icon">{self.ICO_MAIL}</span><span><a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a></span></div>')
        if info.linkedin:
            lbl = info.linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_rows.append(f'<div class="cr-contact-row"><span class="cr-c-icon">💼</span><span><a href="{self.esc(info.linkedin)}" target="_blank">{self.esc(lbl)}</a></span></div>')
            contact_rows.append(f'<div class="cr-contact-row"><span class="cr-c-icon">{self.ICO_LINKEDIN}</span><span><a href="{self.esc(info.linkedin)}" target="_blank">{self.esc(lbl)}</a></span></div>')
        if info.github:
            lbl = info.github.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_rows.append(f'<div class="cr-contact-row"><span class="cr-c-icon">🐙</span><span><a href="{self.esc(info.github)}" target="_blank">{self.esc(lbl)}</a></span></div>')
            contact_rows.append(f'<div class="cr-contact-row"><span class="cr-c-icon">{self.ICO_GITHUB}</span><span><a href="{self.esc(info.github)}" target="_blank">{self.esc(lbl)}</a></span></div>')
        if info.driver_license:
            contact_rows.append(f'<div class="cr-contact-row"><span class="cr-c-icon">🚗</span><span>Prawo jazdy: {self.esc(info.driver_license)}</span></div>')
            contact_rows.append(f'<div class="cr-contact-row"><span class="cr-c-icon">{self.ICO_CAR}</span><span>Prawo jazdy: {self.esc(info.driver_license)}</span></div>')
        
        contact_html = "\n".join(contact_rows)

        # Education for sidebar
        edu_rows = []
        for ed in self.data.education:
            inst = self.esc(ed.institution)
            loc = f", {self.esc(ed.location)}" if ed.location else ""
            edu_rows.append(f"""
            <div class="cr-edu-item">
                <div class="cr-edu-degree">{self.esc(ed.degree)}</div>
                <div class="cr-edu-inst">{inst}{loc}</div>
                <div class="cr-edu-date">{self.esc(ed.period)}</div>
            </div>""")
        edu_html = "\n".join(edu_rows)

        # Languages for sidebar
        lang_rows = []
        for lg in self.data.languages:
            lvl = f' – <span class="cr-lvl">{self.esc(lg.level)}</span>' if lg.level else ""
            lang_rows.append(f'<div class="cr-lang-item"><b>{self.esc(lg.language)}</b>{lvl}</div>')
        lang_html = "\n".join(lang_rows)

        # RIGHT COLUMN: Experience with yellow accents
        exp_rows = []
        for exp in self.data.experience:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in exp.description)
            comp_loc = self.esc(exp.company)
            if exp.location:
                comp_loc += f", {self.esc(exp.location)}"
            exp_rows.append(f"""
            <div class="cr-entry">
                <div class="cr-entry-period">{self.esc(exp.period)}</div>
                <div class="cr-entry-role">{self.esc(exp.role)} &bull; {comp_loc}</div>
                <ul class="cr-bullets">{bullets}</ul>
            </div>""")
        experience_html = "\n".join(exp_rows)

        # Startups
        st_rows = []
        for st in self.data.startups:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in st.description)
            tech = f'<div class="cr-tech">Tech: {self.esc(", ".join(st.tech_stack))}</div>' if st.tech_stack else ""
            st_rows.append(f"""
            <div class="cr-entry">
                {f'<div class="cr-entry-period">{self.esc(st.period)}</div>' if st.period else ''}
                <div class="cr-entry-role">{self.esc(st.name)}</div>
                {tech}
                <ul class="cr-bullets">{bullets}</ul>
            </div>""")
        startups_html = "\n".join(st_rows)

        # Projects
        proj_rows = []
        for pr in self.data.projects:
            link = f'<a class="cr-link" href="{self.esc(pr.url)}" target="_blank">🔗 Link</a>' if pr.url else ""
            link = f'<a class="cr-link" href="{self.esc(pr.url)}" target="_blank">{self.ICO_LINK} Link</a>' if pr.url else ""
            tech = f'<span class="cr-tech-tag">{self.esc(", ".join(pr.tech_stack))}</span>' if pr.tech_stack else ""
            desc = f'<p class="cr-desc">{self.esc(pr.description)}</p>' if pr.description else ""
            proj_rows.append(f"""
            <div class="cr-entry">
                <div class="cr-entry-role">{self.esc(pr.name)} {link}</div>
                {tech}
                {desc}
            </div>""")
        projects_html = "\n".join(proj_rows)

        # Skills with meter rating dots
        # Skills with clean meter rating dots
        skills_rows = []
        dots_html = '<div class="cr-sk-dots"><span class="dot on"></span><span class="dot on"></span><span class="dot on"></span><span class="dot on"></span><span class="dot"></span></div>'
        if self.data.skills_categorized:
            for cat_name, sks in self.data.skills_categorized.items():
                pills = "".join(f'<div class="cr-skill-row"><span class="cr-sk-name">{self.esc(s)}</span><span class="cr-sk-dots">★★★★★</span></div>' for s in sks)
                pills = "".join(f'<div class="cr-skill-row"><span class="cr-sk-name">{self.esc(s)}</span>{dots_html}</div>' for s in sks)
                skills_rows.append(f"""
                <div class="cr-sk-cat">
                    <div class="cr-sk-cat-title">{self.esc(cat_name)}</div>
                    <div class="cr-sk-grid">{pills}</div>
                </div>""")
        elif self.data.skills_technical:
            pills = "".join(f'<div class="cr-skill-row"><span class="cr-sk-name">{self.esc(s)}</span><span class="cr-sk-dots">★★★★★</span></div>' for s in self.data.skills_technical)
            pills = "".join(f'<div class="cr-skill-row"><span class="cr-sk-name">{self.esc(s)}</span>{dots_html}</div>' for s in self.data.skills_technical)
            skills_rows.append(f'<div class="cr-sk-grid">{pills}</div>')
        skills_html = "\n".join(skills_rows)

        # Soft Skills / Interests
        interests_rows = []
        if self.data.skills_soft:
            for s in self.data.skills_soft:
                interests_rows.append(f'<span class="cr-pill">{self.esc(s)}</span>')
        interests_html = f'<div class="cr-pill-wrap">{"".join(interests_rows)}</div>' if interests_rows else ""

        css = f"""
        {self._css_variables()}
        {self._css_reset()}

        .cv-container {{
            max-width: 890px;
            margin: 0 auto;
            background: #ffffff;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.1);
            border-radius: 4px;
            overflow: hidden;
        }}

        .cr-table {{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            table-layout: fixed;
        }}

        /* Left Column with Yellow Arch */
        .cr-sidebar {{
            width: 34%;
            background-color: #f8fafc;
            color: #2d3748;
            padding: 0 24px 34px 24px;
            vertical-align: top;
            box-sizing: border-box;
            border-right: 1px solid #edf2f7;
        }}

        /* The yellow arched header behind photo */
        .cr-arch-container {{
            background: #f5b800;
            margin: 0 -24px 24px -24px;
            padding: 30px 20px 24px 20px;
            border-radius: 0 0 65px 65px;
            text-align: center;
            box-shadow: inset 0 -3px 8px rgba(0,0,0,0.06);
        }}

        .cr-photo {{
            width: 120px;
            height: 140px;
            object-fit: cover;
            border-radius: 18px;
            display: inline-block;
            border: 3px solid #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            background: #ffffff;
        }}

        .cr-photo-placeholder {{
            width: 120px;
            height: 140px;
            border-radius: 18px;
            background: #ffffff;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
            border: 3px solid #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}

        .cr-sb-title {{
            font-size: 13px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #1a202c;
            border-bottom: 2px solid #f5b800;
            display: inline-block;
            padding-bottom: 2px;
            margin-top: 20px;
            margin-bottom: 12px;
        }}

        .cr-contact-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11.5px;
            color: #4a5568;
            margin-bottom: 8px;
            line-height: 1.4;
            word-break: break-all;
        }}

        .cr-contact-row a {{
            color: #2d3748;
            text-decoration: none;
        }}

        .cr-contact-row a:hover {{
            color: #d99b00;
            text-decoration: underline;
        }}

        .cr-c-icon {{
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: #fef3c7;
            color: #b45309;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            flex-shrink: 0;
        }}

        .cr-edu-item {{
            margin-bottom: 12px;
        }}

        .cr-edu-degree {{
            font-size: 12px;
            font-weight: 700;
            color: #1a202c;
        }}

        .cr-edu-inst {{
            font-size: 11px;
            color: #4a5568;
        }}

        .cr-edu-date {{
            font-size: 10.5px;
            color: #718096;
        }}

        .cr-lang-item {{
            font-size: 11.5px;
            color: #2d3748;
            margin-bottom: 6px;
        }}

        .cr-lvl {{
            color: #718096;
            font-size: 11px;
        }}

        /* Right Column */
        .cr-main {{
            width: 66%;
            background-color: #ffffff;
            color: #2d3748;
            padding: 38px 36px;
            vertical-align: top;
            box-sizing: border-box;
        }}

        .cr-name {{
            font-size: 32px;
            font-weight: 800;
            color: #1a202c;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            line-height: 1.1;
            margin-bottom: 4px;
        }}

        .cr-title {{
            font-size: 14px;
            font-weight: 700;
            color: #d99b00;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            border-bottom: 2px solid #f5b800;
            display: inline-block;
            padding-bottom: 3px;
            margin-bottom: 14px;
        }}

        .cr-summary {{
            font-size: 12.5px;
            color: #4a5568;
            text-align: justify;
            line-height: 1.55;
            margin-bottom: 22px;
        }}

        .cr-section-title {{
            font-size: 13.5px;
            font-weight: 800;
            color: #1a202c;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            border-bottom: 2px solid #f5b800;
            display: inline-block;
            padding-bottom: 2px;
            margin-top: 20px;
            margin-bottom: 12px;
        }}

        .cr-entry {{
            margin-bottom: 14px;
            page-break-inside: avoid;
            border-left: 2px solid #f5b800;
            padding-left: 12px;
            margin-left: 2px;
        }}

        .cr-entry-period {{
            font-size: 11px;
            font-weight: 700;
            color: #b45309;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .cr-entry-role {{
            font-size: 13px;
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 2px;
        }}

        .cr-bullets {{
            list-style-type: disc;
            margin-left: 18px;
            font-size: 12px;
            color: #4a5568;
            line-height: 1.45;
        }}

        .cr-bullets li {{
            margin-bottom: 2px;
        }}

        .cr-tech {{
            font-size: 11px;
            color: #718096;
            margin-bottom: 3px;
        }}

        .cr-tech-tag {{
            font-size: 11px;
            background: #fef3c7;
            color: #92400e;
            padding: 1px 6px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 3px;
        }}

        .cr-desc {{
            font-size: 12px;
            color: #4a5568;
            margin-top: 2px;
            text-align: justify;
        }}

        .cr-link {{
            font-size: 11.5px;
            color: #b45309;
            text-decoration: none;
            margin-left: 6px;
        }}

        .cr-sk-cat {{
            margin-bottom: 8px;
            page-break-inside: avoid;
        }}

        .cr-sk-cat-title {{
            font-size: 12px;
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 3px;
        }}

        .cr-sk-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px 16px;
        }}

        .cr-skill-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11.5px;
            color: #2d3748;
        }}

        .cr-sk-dots {{
            color: #f5b800;
            letter-spacing: 2px;
            font-size: 10px;
            display: inline-flex;
            gap: 3px;
            align-items: center;
        }}

        .cr-sk-dots .dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #e2e8f0;
            display: inline-block;
        }}

        .cr-sk-dots .dot.on {{
            background: #f5b800;
        }}

        .cr-c-icon svg {{
            width: 11px;
            height: 11px;
            stroke: #b45309;
            margin-right: 0;
        }}

        .cr-pill-wrap {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-top: 4px;
        }}

        .cr-pill {{
            font-size: 11px;
            background: #fef3c7;
            color: #78350f;
            padding: 2px 8px;
            border-radius: 12px;
            border: 1px solid #fde68a;
        }}

        .cr-rodo {{
            margin-top: 26px;
            padding-top: 10px;
            border-top: 1px solid #edf2f7;
            font-size: 10px;
            color: #a0aec0;
            font-style: italic;
            text-align: justify;
            line-height: 1.4;
        }}

        {self._css_print_button()}
        {self._css_print_base()}

        @media print {{
            .cr-arch-container {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                background-color: #f5b800 !important;
            }}
            .cr-sidebar {{
                background-color: #f8fafc !important;
            }}
            .cr-c-icon, .cr-tech-tag, .cr-pill {{
                background-color: #fef3c7 !important;
                color: #92400e !important;
            }}
        }}
        """

        summary_p = f'<div class="cr-summary">{self._summary_content()}</div>' if self.data.summary else ""

        full_html = f"""{self._html_head(css)}
<body>
    {self._print_button()}
    <div class="cv-container">
        <table class="cr-table">
            <tr>
                <!-- LEFT ARCH COLUMN -->
                <td class="cr-sidebar">
                    <div class="cr-arch-container">
                        {photo_html}
                    </div>

                    <div class="cr-sb-title">CONTACT_</div>
                    {contact_html}

                    {f'<div class="cr-sb-title">EDUCATION_</div>{edu_html}' if edu_html else ''}
                    {f'<div class="cr-sb-title">LANGUAGES_</div>{lang_html}' if lang_html else ''}
                </td>

                <!-- RIGHT MAIN COLUMN -->
                <td class="cr-main">
                    <h1 class="cr-name">{self.esc(self.info.name or "Kacper Pudełko")}</h1>
                    {f'<div class="cr-title">{self.esc(self.info.title)}</div>' if self.info.title else ''}
                    {summary_p}

                    {f'<div class="cr-section-title">JOB EXPERIENCE_</div>{experience_html}' if experience_html else ''}
                    {f'<div class="cr-section-title">STARTUPS & INITIATIVES_</div>{startups_html}' if startups_html else ''}
                    {f'<div class="cr-section-title">PROJECTS_</div>{projects_html}' if projects_html else ''}
                    {f'<div class="cr-section-title">SKILLS_</div>{skills_html}' if skills_html else ''}
                    {f'<div class="cr-section-title">INTERESTS & SOFT SKILLS_</div>{interests_html}' if interests_html else ''}

                    {f'<div class="cr-rodo">{self.esc(self.data.clause)}</div>' if self.data.clause else ''}
                </td>
            </tr>
        </table>
    </div>
</body>
</html>"""
        return self._write(output_path, full_html)

