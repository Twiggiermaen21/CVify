"""
Technical Boxes CV Template.
Direct 1:1 recreation of Image 4 (Adam Paprocki technical grid style):
- Rectangular photo on the top right
- Boxed section headers with solid borders
- Dashed/solid container boxes for content grouping
- Visual level sliders for languages (interactive-style track + knob)
- Clean, structured, engineering aesthetic
"""
from .base_template import BaseTemplate


class BoxesTemplate(BaseTemplate):
    """Technical boxed grid template with rectangular photo and language level sliders."""

    def build(self, output_path: str = "nowe_cv.html") -> str:
        photo_uri = self._photo_base64()
        if photo_uri:
            photo_html = f'<div class="bx-photo-wrap"><img src="{photo_uri}" alt="{self.esc(self.info.name)}" class="bx-photo"></div>'
        else:
            photo_html = '<div class="bx-photo-wrap"><div class="bx-photo-empty">👤</div></div>'
            photo_html = '<div class="bx-photo-wrap"><div class="bx-photo-empty"><svg class="bx-user-svg" viewBox="0 0 24 24" fill="none" stroke="#718096" stroke-width="1.5"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 4-6 8-6s8 2 8 6"/></svg></div></div>'

        info = self.info
        contact_parts = []
        if info.phone:
            contact_parts.append(f'<span>☎ <a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a></span>')
            contact_parts.append(f'<span>{self.ICO_PHONE} <a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a></span>')
        if info.email:
            contact_parts.append(f'<span>✉ <a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a></span>')
            contact_parts.append(f'<span>{self.ICO_MAIL} <a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a></span>')
        if info.location:
            contact_parts.append(f'<span>📍 {self.esc(info.location)}</span>')
            contact_parts.append(f'<span>{self.ICO_PIN} {self.esc(info.location)}</span>')
        if info.linkedin:
            lbl = info.linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_parts.append(f'<span>💼 <a href="{self.esc(info.linkedin)}" target="_blank">{self.esc(lbl)}</a></span>')
            contact_parts.append(f'<span>{self.ICO_LINKEDIN} <a href="{self.esc(info.linkedin)}" target="_blank">{self.esc(lbl)}</a></span>')
        if info.github:
            lbl = info.github.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_parts.append(f'<span>🐙 <a href="{self.esc(info.github)}" target="_blank">{self.esc(lbl)}</a></span>')
            contact_parts.append(f'<span>{self.ICO_GITHUB} <a href="{self.esc(info.github)}" target="_blank">{self.esc(lbl)}</a></span>')
        if info.driver_license:
            contact_parts.append(f'<span>🚗 Prawo jazdy: {self.esc(info.driver_license)}</span>')
            contact_parts.append(f'<span>{self.ICO_CAR} Prawo jazdy: {self.esc(info.driver_license)}</span>')

        contact_bar = " &nbsp;|&nbsp; ".join(contact_parts)

        # Experience entries
        exp_rows = []
        for exp in self.data.experience:
            bullets = "".join(f"<li>- {self.esc(b)}</li>" for b in exp.description)
            comp_loc = self.esc(exp.company)
            if exp.location:
                comp_loc += f", {self.esc(exp.location)}"
            exp_rows.append(f"""
            <div class="bx-job-item">
                <div class="bx-job-date">{self.esc(exp.period)} - {comp_loc}</div>
                <div class="bx-job-role">&bull; {self.esc(exp.role).upper()}</div>
                <ul class="bx-dash-list">{bullets}</ul>
            </div>""")
        experience_html = "\n".join(exp_rows)

        # Startups
        st_rows = []
        for st in self.data.startups:
            bullets = "".join(f"<li>- {self.esc(b)}</li>" for b in st.description)
            st_rows.append(f"""
            <div class="bx-job-item">
                {f'<div class="bx-job-date">{self.esc(st.period)}</div>' if st.period else ''}
                <div class="bx-job-role">&bull; {self.esc(st.name).upper()}</div>
                <ul class="bx-dash-list">{bullets}</ul>
            </div>""")
        startups_html = "\n".join(st_rows)

        # Education
        edu_rows = []
        for ed in self.data.education:
            inst = self.esc(ed.institution)
            loc = f", {self.esc(ed.location)}" if ed.location else ""
            edu_rows.append(f"""
            <div class="bx-edu-item">
                <div class="bx-edu-date">{self.esc(ed.period)}</div>
                <div class="bx-edu-school">{inst}{loc}</div>
                <div class="bx-edu-degree">{self.esc(ed.degree)}</div>
            </div>""")
        education_html = "\n".join(edu_rows)

        # Languages with visual SLIDER LEVEL METERS
        lang_rows = []
        for lg in self.data.languages:
            lvl_text = lg.level or ""
            # Estimate slider percentage based on level description
            lvl_lower = lvl_text.lower()
            if "ojczysty" in lvl_lower or "c2" in lvl_lower or "biegły" in lvl_lower:
                pos = 92
            elif "c1" in lvl_lower or "zaawansowany" in lvl_lower:
                pos = 80
            elif "b2" in lvl_lower or "wyższy średnio" in lvl_lower:
                pos = 65
            elif "b1" in lvl_lower or "średni" in lvl_lower:
                pos = 50
            elif "a2" in lvl_lower:
                pos = 35
            elif "a1" in lvl_lower or "podstawowy" in lvl_lower or "początkujący" in lvl_lower:
                pos = 20
            else:
                pos = 50

            full_label = f"{lg.language.upper()}{(' - ' + lvl_text.upper()) if lvl_text else ''}"
            lang_rows.append(f"""
            <div class="bx-slider-item">
                <div class="bx-slider-label">{self.esc(full_label)}</div>
                <div class="bx-slider-track">
                    <div class="bx-slider-fill" style="width: {pos}%;"></div>
                    <div class="bx-slider-thumb" style="left: calc({pos}% - 10px);"></div>
                </div>
            </div>""")
        languages_html = "\n".join(lang_rows)

        # Projects
        proj_rows = []
        for pr in self.data.projects:
            link = f'<a class="bx-link" href="{self.esc(pr.url)}" target="_blank">🔗 {self.esc(pr.url)}</a>' if pr.url else ""
            link = f'<a class="bx-link" href="{self.esc(pr.url)}" target="_blank">{self.ICO_LINK} {self.esc(pr.url)}</a>' if pr.url else ""
            tech = f'<span class="bx-tech-info">[{self.esc(", ".join(pr.tech_stack))}]</span>' if pr.tech_stack else ""
            desc = f'<div class="bx-proj-desc">{self.esc(pr.description)}</div>' if pr.description else ""
            proj_rows.append(f"""
            <div class="bx-job-item">
                <div class="bx-job-role">&bull; {self.esc(pr.name).upper()} {link}</div>
                {tech}
                {desc}
            </div>""")
        projects_html = "\n".join(proj_rows)

        # Skills (Technical & Soft)
        skills_items = []
        if self.data.skills_categorized:
            for cat_name, sks in self.data.skills_categorized.items():
                for s in sks:
                    skills_items.append(f"<li>- {self.esc(s)} ({self.esc(cat_name)})</li>")
        elif self.data.skills_technical:
            for s in self.data.skills_technical:
                skills_items.append(f"<li>- {self.esc(s)}</li>")

        if self.data.skills_soft:
            for s in self.data.skills_soft:
                skills_items.append(f"<li>- {self.esc(s)}</li>")

        skills_html = f'<ul class="bx-dash-list">{"".join(skills_items)}</ul>' if skills_items else ""

        css = f"""
        {self._css_variables()}
        {self._css_reset()}
        {self._css_common_components()}

        .bx-user-svg {{
            width: 48px;
            height: 48px;
            stroke: #94a3b8;
        }}

        .cv-container {{
            max-width: 880px;
            margin: 0 auto;
            background: #ffffff;
            padding: 34px 38px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
            border-radius: 2px;
            border: 1px solid #111111;
        }}

        /* Header with Rectangular Photo Top Right */
        .bx-header-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}

        .bx-header-left {{
            vertical-align: top;
        }}

        .bx-header-right {{
            width: 125px;
            vertical-align: top;
            text-align: right;
        }}

        .bx-name {{
            font-size: 34px;
            font-weight: 900;
            color: #000000;
            letter-spacing: 1px;
            text-transform: uppercase;
            line-height: 1.1;
        }}

        .bx-sub {{
            font-size: 14.5px;
            color: #4a5568;
            margin-top: 4px;
            margin-bottom: 12px;
        }}

        .bx-contact-bar {{
            font-size: 11.5px;
            color: #111111;
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            align-items: center;
        }}

        .bx-contact-bar a {{
            color: #111111;
            text-decoration: none;
        }}

        .bx-contact-bar a:hover {{
            text-decoration: underline;
        }}

        .bx-photo-wrap {{
            display: inline-block;
        }}

        .bx-photo {{
            width: 115px;
            height: 140px;
            object-fit: cover;
            border: 1.5px solid #111111;
            display: block;
        }}

        .bx-photo-empty {{
            width: 115px;
            height: 140px;
            border: 1.5px solid #111111;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 36px;
            background: #f7fafc;
        }}

        /* 2-Column Table Body */
        .bx-grid-table {{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            table-layout: fixed;
        }}

        .bx-col-left {{
            width: 58%;
            vertical-align: top;
            padding-right: 14px;
            box-sizing: border-box;
        }}

        .bx-col-right {{
            width: 42%;
            vertical-align: top;
            padding-left: 14px;
            box-sizing: border-box;
        }}

        /* Boxed Section Headers */
        .bx-box-header {{
            border: 1.5px solid #111111;
            background: #ffffff;
            padding: 5px 10px;
            font-size: 13.5px;
            font-weight: 800;
            color: #000000;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}

        /* Dashed Content Containers */
        .bx-box-content {{
            border: 1px dashed #718096;
            padding: 12px 14px;
            margin-bottom: 16px;
            page-break-inside: avoid;
        }}

        .bx-job-item {{
            margin-bottom: 12px;
            page-break-inside: avoid;
        }}

        .bx-job-item:last-child {{
            margin-bottom: 0;
        }}

        .bx-job-date {{
            font-size: 12px;
            font-weight: 700;
            color: #111111;
        }}

        .bx-job-role {{
            font-size: 12.5px;
            font-weight: 800;
            color: #000000;
            margin-top: 1px;
            margin-bottom: 3px;
        }}

        .bx-dash-list {{
            list-style: none;
            padding-left: 0;
            font-size: 11.5px;
            color: #2d3748;
            line-height: 1.45;
        }}

        .bx-dash-list li {{
            margin-bottom: 2px;
        }}

        .bx-edu-item {{
            margin-bottom: 10px;
        }}

        .bx-edu-date {{
            font-size: 11.5px;
            font-weight: 700;
            color: #111111;
        }}

        .bx-edu-school {{
            font-size: 11.5px;
            color: #2d3748;
        }}

        .bx-edu-degree {{
            font-size: 11px;
            color: #718096;
            font-style: italic;
        }}

        /* Slider Controls for Languages */
        .bx-slider-item {{
            margin-bottom: 12px;
        }}

        .bx-slider-label {{
            font-size: 11px;
            font-weight: 800;
            color: #000000;
            margin-bottom: 4px;
            letter-spacing: 0.5px;
        }}

        .bx-slider-track {{
            position: relative;
            height: 14px;
            background: #ffffff;
            border: 1.5px solid #111111;
            border-radius: 2px;
        }}

        .bx-slider-fill {{
            height: 100%;
            background: #e2e8f0;
        }}

        .bx-slider-thumb {{
            position: absolute;
            top: -3px;
            width: 20px;
            height: 18px;
            background: #111111;
            border-radius: 3px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.4);
        }}

        .bx-link {{
            font-size: 11px;
            color: #2b6cb0;
            text-decoration: none;
            font-weight: normal;
        }}

        .bx-tech-info {{
            font-size: 11px;
            color: #718096;
            display: block;
            margin-bottom: 2px;
        }}

        .bx-proj-desc {{
            font-size: 11.5px;
            color: #2d3748;
            margin-top: 2px;
            text-align: justify;
        }}

        .bx-rodo {{
            margin-top: 22px;
            padding-top: 8px;
            border-top: 1px solid #cbd5e0;
            font-size: 9.5px;
            color: #718096;
            font-style: italic;
            text-align: justify;
            line-height: 1.35;
        }}

        {self._css_print_button()}
        {self._css_print_base()}

        @media print {{
            .bx-slider-thumb {{
                background-color: #111111 !important;
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}
            .bx-slider-track {{
                border-color: #111111 !important;
            }}
        }}
        """

        loc_str = f", {self.info.location}" if self.info.location else ""
        sub_title = f"{self.info.title}{loc_str}" if self.info.title else (self.info.location or "")

        full_html = f"""{self._html_head(css)}
<body>
    {self._print_button()}
    <div class="cv-container">
        <!-- TOP HEADER -->
        <table class="bx-header-table">
            <tr>
                <td class="bx-header-left">
                    <h1 class="bx-name">{self.esc(self.info.name or "Kacper Pudełko")}</h1>
                    {f'<div class="bx-sub">{self.esc(sub_title)}</div>' if sub_title else ''}
                    <div class="bx-contact-bar">{contact_bar}</div>
                </td>
                <td class="bx-header-right">
                    {photo_html}
                </td>
            </tr>
        </table>

        <!-- 2-COLUMN GRID -->
        <table class="bx-grid-table">
            <tr>
                <!-- LEFT COLUMN -->
                <td class="bx-col-left">
                    {f'''
                    <div class="bx-box-header">doświadczenie</div>
                    <div class="bx-box-content">{experience_html}</div>
                    ''' if experience_html else ''}

                    {f'''
                    <div class="bx-box-header">start-up & inicjatywy</div>
                    <div class="bx-box-content">{startups_html}</div>
                    ''' if startups_html else ''}

                    {f'''
                    <div class="bx-box-header">projekty</div>
                    <div class="bx-box-content">{projects_html}</div>
                    ''' if projects_html else ''}
                </td>

                <!-- RIGHT COLUMN -->
                <td class="bx-col-right">
                    {f'''
                    <div class="bx-box-header">edukacja</div>
                    <div class="bx-box-content">{education_html}</div>
                    ''' if education_html else ''}

                    {f'''
                    <div class="bx-box-header">języki obce</div>
                    <div class="bx-box-content">{languages_html}</div>
                    ''' if languages_html else ''}

                    {f'''
                    <div class="bx-box-header">umiejętności</div>
                    <div class="bx-box-content">{skills_html}</div>
                    ''' if skills_html else ''}
                </td>
            </tr>
        </table>

        {f'<div class="bx-rodo">{self.esc(self.data.clause)}</div>' if self.data.clause else ''}
    </div>
</body>
</html>"""
        return self._write(output_path, full_html)

