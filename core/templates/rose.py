"""
Rose Script & Burgundy CV Template.
Direct 1:1 recreation of Image 5 (Aleksandra Nowak):
- Elegant cursive / script burgundy header for candidate name (Dancing Script / Brush Script)
- Clean subtitle for professional title
- Soft pale rose/blush left sidebar with circular photo
- Underlined section headers (Dane osobowe, Umiejętności, Języki, Zainteresowania)
- Two-line entry headers (Role/Degree left, Location right; Company/School left, Period right)
- Subtle full-width section divider lines
- Table-based layout for rock-solid PDF printing
"""
from .base_template import BaseTemplate


class RoseTemplate(BaseTemplate):
    """Elegant cursive script & burgundy template with soft blush sidebar."""

    def _get_palette(self):
        """Derive dynamic palette from theme_primary or default to #7b113a (burgundy)."""
        primary = getattr(self.data, "theme_primary", None) or "#7b113a"
        primary = primary.strip()
        if not primary.startswith("#") or len(primary) not in (4, 7):
            primary = "#7b113a"

        # If current theme_primary is yellow (#f5b800) from Creative template or navy (#1a365d) default,
        # default Rose template to its signature elegant burgundy #7b113a
        if primary.lower() in ("#f5b800", "#1a365d"):
            primary = "#7b113a"

        try:
            if len(primary) == 4:
                r = int(primary[1] * 2, 16)
                g = int(primary[2] * 2, 16)
                b = int(primary[3] * 2, 16)
            else:
                r = int(primary[1:3], 16)
                g = int(primary[3:5], 16)
                b = int(primary[5:7], 16)
        except Exception:
            r, g, b = 123, 17, 58
            primary = "#7b113a"

        # Very light pale tint for sidebar background (95% mix with white)
        sb_r = int(r + (255 - r) * 0.955)
        sb_g = int(g + (255 - g) * 0.955)
        sb_b = int(b + (255 - b) * 0.955)
        sidebar_bg = f"#{sb_r:02x}{sb_g:02x}{sb_b:02x}"

        # Subtle sidebar border (88% mix with white)
        br_r = int(r + (255 - r) * 0.88)
        br_g = int(g + (255 - g) * 0.88)
        br_b = int(b + (255 - b) * 0.88)
        sidebar_border = f"#{br_r:02x}{br_g:02x}{br_b:02x}"

        return {
            "primary": primary,
            "sidebar_bg": sidebar_bg,
            "sidebar_border": sidebar_border,
        }

    def build(self, output_path: str = "nowe_cv.html") -> str:
        palette = self._get_palette()
        pri = palette["primary"]
        sb_bg = palette["sidebar_bg"]
        sb_br = palette["sidebar_border"]

        # Photo: circular with delicate white ring and subtle shadow
        photo_uri = self._photo_base64()
        if photo_uri:
            photo_html = f'<div class="rose-photo-wrap"><img src="{photo_uri}" alt="{self.esc(self.info.name)}" class="rose-photo"></div>'
        else:
            photo_html = f'<div class="rose-photo-wrap"><div class="rose-photo-empty"><svg class="rose-user-svg" viewBox="0 0 24 24" fill="none" stroke="{pri}" stroke-width="1.5"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 4-6 8-6s8 2 8 6"/></svg></div></div>'

        info = self.info
        contact_rows = []
        if info.email:
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">{self.ICO_MAIL}</span><span><a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a></span></div>')
        if info.phone:
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">{self.ICO_PHONE}</span><span><a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a></span></div>')
        if info.location:
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">{self.ICO_PIN}</span><span>{self.esc(info.location)}</span></div>')
        if info.linkedin:
            lbl = info.linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">{self.ICO_LINKEDIN}</span><span><a href="{self.esc(info.linkedin)}" target="_blank" rel="noopener">{self.esc(lbl)}</a></span></div>')
        if info.github:
            lbl = info.github.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">{self.ICO_GITHUB}</span><span><a href="{self.esc(info.github)}" target="_blank" rel="noopener">{self.esc(lbl)}</a></span></div>')
        if info.driver_license:
            contact_rows.append(f'<div class="rose-contact-row"><span class="rose-c-icon">{self.ICO_CAR}</span><span>Prawo jazdy: {self.esc(info.driver_license)}</span></div>')

        contact_html = "\n".join(contact_rows)

        # Skills for sidebar (inline category: items like Aleksandra Nowak reference)
        skills_sidebar_rows = []
        if self.data.skills_categorized:
            for cat_name, sks in self.data.skills_categorized.items():
                items = ", ".join(self.esc(s) for s in sks)
                skills_sidebar_rows.append(f"""
                <div class="rose-sb-skill-block">
                    <span class="rose-sb-skill-cat">{self.esc(cat_name)}:</span>
                    <span class="rose-sb-skill-items">{items}</span>
                </div>""")
        elif self.data.skills_technical:
            skills_sidebar_rows.append(f"""
            <div class="rose-sb-skill-block">
                <span class="rose-sb-skill-cat">Umiejętności techniczne:</span>
                <span class="rose-sb-skill-items">{", ".join(self.esc(s) for s in self.data.skills_technical)}</span>
            </div>""")

        skills_sidebar_html = "\n".join(skills_sidebar_rows)

        # Languages for sidebar
        lang_rows = []
        for lg in self.data.languages:
            lvl = f" ({self.esc(lg.level)})" if lg.level else ""
            lang_rows.append(f'<div class="rose-lang-item"><b>{self.esc(lg.language)}</b>{lvl}</div>')
        lang_html = "\n".join(lang_rows)

        # Zainteresowania / Umiejętności miękkie
        interests_html = ""
        if self.data.skills_soft:
            interests_html = f'<div class="rose-sb-skill-items">{", ".join(self.esc(s) for s in self.data.skills_soft)}</div>'

        # RIGHT COLUMN: Experience with 2-line header (Role left / Location right, Company left / Period right)
        exp_rows = []
        for exp in self.data.experience:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in exp.description)
            loc = f'<span class="rose-meta-right">{self.esc(exp.location)}</span>' if exp.location else ""
            period = f'<span class="rose-meta-right">{self.esc(exp.period)}</span>' if exp.period else ""
            bullets_html = f'<ul class="rose-bullets">{bullets}</ul>' if bullets else ""
            exp_rows.append(f"""
            <div class="rose-entry">
                <div class="rose-entry-row">
                    <span class="rose-role">{self.esc(exp.role)}</span>
                    {loc}
                </div>
                <div class="rose-entry-row rose-entry-sub">
                    <span class="rose-company">{self.esc(exp.company)}</span>
                    {period}
                </div>
                {bullets_html}
            </div>""")
        experience_html = "\n".join(exp_rows)

        # Startups
        st_rows = []
        for st in self.data.startups:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in st.description)
            period = f'<span class="rose-meta-right">{self.esc(st.period)}</span>' if st.period else ""
            tech = f'<div class="rose-tech">Tech stack: {self.esc(", ".join(st.tech_stack))}</div>' if st.tech_stack else ""
            bullets_html = f'<ul class="rose-bullets">{bullets}</ul>' if bullets else ""
            st_rows.append(f"""
            <div class="rose-entry">
                <div class="rose-entry-row">
                    <span class="rose-role">{self.esc(st.name)}</span>
                    {period}
                </div>
                {tech}
                {bullets_html}
            </div>""")
        startups_html = "\n".join(st_rows)

        # Projects
        proj_rows = []
        for pr in self.data.projects:
            if pr.url:
                clean_url = pr.url.replace("https://", "").replace("http://", "").rstrip("/")
                icon = self.ICO_GITHUB if "github.com" in clean_url else self.ICO_LINK
                link = f'<a class="rose-link" href="{self.esc(pr.url)}" target="_blank" rel="noopener">{icon} {self.esc(clean_url)}</a>'
            else:
                link = ""
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

        # Education with 2-line header (Degree left / Location right, Institution left / Period right)
        edu_rows = []
        for ed in self.data.education:
            loc = f'<span class="rose-meta-right">{self.esc(ed.location)}</span>' if ed.location else ""
            period = f'<span class="rose-meta-right">{self.esc(ed.period)}</span>' if ed.period else ""
            details = f'<div class="rose-details">{self.esc(ed.details)}</div>' if ed.details else ""
            edu_rows.append(f"""
            <div class="rose-entry">
                <div class="rose-entry-row">
                    <span class="rose-role">{self.esc(ed.degree)}</span>
                    {loc}
                </div>
                <div class="rose-entry-row rose-entry-sub">
                    <span class="rose-company">{self.esc(ed.institution)}</span>
                    {period}
                </div>
                {details}
            </div>""")
        education_html = "\n".join(edu_rows)

        css = f"""
        @import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Inter:wght@400;500;600;700&display=swap');

        {self._css_variables()}
        {self._css_reset()}
        {self._css_common_components()}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: #2d3748;
            background: #f4f6f8;
            padding: 24px 12px;
        }}

        .cv-container {{
            max-width: 860px;
            margin: 0 auto;
            background: #ffffff;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
            border-radius: 4px;
            overflow: hidden;
        }}

        .rose-table {{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            table-layout: fixed;
        }}

        /* Left Pale Blush / Rose Sidebar */
        .rose-sidebar {{
            width: 30%;
            background-color: {sb_bg};
            color: #333333;
            padding: 34px 22px 28px 22px;
            vertical-align: top;
            box-sizing: border-box;
            border-right: 1px solid {sb_br};
        }}

        .rose-photo-wrap {{
            text-align: center;
            margin-bottom: 22px;
        }}

        .rose-photo {{
            width: 125px;
            height: 125px;
            object-fit: cover;
            border-radius: 50%;
            display: inline-block;
            border: 3px solid #ffffff;
            box-shadow: 0 4px 12px rgba(123, 17, 58, 0.12);
        }}

        .rose-photo-empty {{
            width: 125px;
            height: 125px;
            border-radius: 50%;
            background: #ffffff;
            border: 3px solid #ffffff;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(123, 17, 58, 0.12);
        }}

        .rose-user-svg {{
            width: 50px;
            height: 50px;
        }}

        .rose-sb-title {{
            font-size: 13.5px;
            font-weight: 700;
            color: #222222;
            border-bottom: 1px solid #718096;
            padding-bottom: 3px;
            margin-top: 22px;
            margin-bottom: 11px;
            letter-spacing: 0.2px;
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
            color: {pri};
            text-decoration: underline;
        }}

        .rose-c-icon {{
            width: 14px;
            height: 14px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: #222222;
            flex-shrink: 0;
        }}

        .rose-c-icon svg {{
            width: 13px;
            height: 13px;
        }}

        .rose-sb-skill-block {{
            margin-bottom: 5px;
            line-height: 1.35;
        }}

        .rose-sb-skill-cat {{
            font-size: 10.5px;
            font-weight: 700;
            color: #222222;
        }}

        .rose-sb-skill-items {{
            font-size: 10.5px;
            color: #4a5568;
            line-height: 1.35;
        }}

        .rose-lang-item {{
            font-size: 11.5px;
            color: #333333;
            margin-bottom: 6px;
        }}

        /* Right Column with Elegant Burgundy Script Header */
        .rose-main {{
            width: 70%;
            background-color: #ffffff;
            color: #2d3748;
            padding: 36px 36px 28px 36px;
            vertical-align: top;
            box-sizing: border-box;
        }}

        .rose-name {{
            font-family: 'Dancing Script', 'Brush Script MT', 'Segoe Script', cursive;
            font-size: 40px;
            font-weight: 700;
            color: {pri};
            letter-spacing: 0.3px;
            line-height: 1.15;
            margin-bottom: 2px;
        }}

        .rose-title {{
            font-size: 14px;
            font-weight: 500;
            color: #4a5568;
            margin-bottom: 20px;
        }}

        .rose-summary {{
            font-size: 12px;
            color: #4a5568;
            text-align: justify;
            line-height: 1.55;
            margin-bottom: 16px;
        }}

        .rose-section-title {{
            font-size: 13.5px;
            font-weight: 700;
            color: #222222;
            border-bottom: 1px solid #d2d6dc;
            padding-bottom: 4px;
            margin-top: 20px;
            margin-bottom: 11px;
            letter-spacing: 0.2px;
        }}

        .rose-entry {{
            margin-bottom: 12px;
            page-break-inside: avoid;
        }}

        .rose-entry-row {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            gap: 12px;
        }}

        .rose-entry-sub {{
            margin-bottom: 2px;
        }}

        .rose-role {{
            font-size: 13px;
            font-weight: 700;
            color: #222222;
        }}

        .rose-company {{
            font-size: 12px;
            color: #444444;
        }}

        .rose-meta-right {{
            font-size: 11.5px;
            color: #666666;
            white-space: nowrap;
            text-align: right;
        }}

        .rose-bullets {{
            list-style-type: disc;
            margin-left: 18px;
            font-size: 11.5px;
            color: #333333;
            line-height: 1.48;
            margin-top: 3px;
        }}

        .rose-bullets li {{
            margin-bottom: 2px;
        }}

        .rose-tech {{
            font-size: 11px;
            color: #718096;
            margin-top: 2px;
            margin-bottom: 3px;
        }}

        .rose-tech-inline {{
            font-size: 11px;
            color: {pri};
            font-weight: 500;
        }}

        .rose-desc {{
            font-size: 11.5px;
            color: #4a5568;
            margin-top: 2px;
            text-align: justify;
            line-height: 1.42;
        }}

        .rose-link {{
            font-size: 11px;
            color: {pri};
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            white-space: nowrap;
        }}

        .rose-link:hover {{
            text-decoration: underline;
        }}

        .rose-details {{
            font-size: 11px;
            color: #718096;
            margin-top: 2px;
        }}

        .rose-rodo {{
            margin-top: 24px;
            padding-top: 8px;
            border-top: 1px solid #f0e6e6;
            font-size: 9.5px;
            color: #a0aec0;
            font-style: italic;
            text-align: justify;
            line-height: 1.35;
        }}

        {self._css_print_button()}
        {self._css_print_base()}

        @media print {{
            .rose-sidebar {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
                background-color: {sb_bg} !important;
            }}
            .rose-name {{
                color: {pri} !important;
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

                    {f'<div class="rose-sb-title">Języki obce</div>{lang_html}' if lang_html else ''}
                    {f'<div class="rose-sb-title">Umiejętności techniczne</div>{skills_sidebar_html}' if skills_sidebar_html else ''}
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
