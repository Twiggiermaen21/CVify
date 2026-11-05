"""
Creative CV Template.
Direct recreation of Image 3 (Anne Robertson agency style):
- Iconic arched header behind photo on top left
- Dynamic color theme support: user can choose any color (yellow, blue, emerald, red, violet, etc.)
- Contact block moved to the top header in the main column (clean & compact)
- Left sidebar holds Photo arch, Education, Languages, and Soft Skills
- Clean section headers with no trailing underscores
- Skills with visual rating dot meters
- Clean, direct project links with GitHub vector icons
- Rock-solid table layout for seamless PDF printing
"""
from .base_template import BaseTemplate


class CreativeTemplate(BaseTemplate):
    """Creative design agency template with dynamic color arch header."""

    def _get_palette(self) -> dict:
        """Derive full coordinated palette from user's primary theme color."""
        theme_hex = (self.data.theme_primary or "").strip()
        if not theme_hex or not theme_hex.startswith("#") or len(theme_hex) not in (4, 7):
            theme_hex = "#f5b800"

        # Expand shorthand #rgb to #rrggbb
        h = theme_hex.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)

        try:
            r = int(h[0:2], 16)
            g = int(h[2:4], 16)
            b = int(h[4:6], 16)
        except ValueError:
            r, g, b = 245, 184, 0
            h = "f5b800"

        # Tint for badges / icon backgrounds (approx 88% white mix)
        r_light = int(r + (255 - r) * 0.88)
        g_light = int(g + (255 - g) * 0.88)
        b_light = int(b + (255 - b) * 0.88)
        light_hex = f"#{r_light:02x}{g_light:02x}{b_light:02x}"

        # Border tint (approx 70% white mix)
        r_border = int(r + (255 - r) * 0.70)
        g_border = int(g + (255 - g) * 0.70)
        b_border = int(b + (255 - b) * 0.70)
        border_hex = f"#{r_border:02x}{g_border:02x}{b_border:02x}"

        # Dark contrast accent for text/headings (40% darker)
        r_dark = int(r * 0.65)
        g_dark = int(g * 0.65)
        b_dark = int(b * 0.65)
        dark_hex = f"#{r_dark:02x}{g_dark:02x}{b_dark:02x}"

        # Deep accent for badges text
        r_deep = int(r * 0.48)
        g_deep = int(g * 0.48)
        b_deep = int(b * 0.48)
        deep_hex = f"#{r_deep:02x}{g_deep:02x}{b_deep:02x}"

        return {
            "primary": f"#{h}",
            "light": light_hex,
            "border": border_hex,
            "dark": dark_hex,
            "deep": deep_hex,
        }

    def build(self, output_path: str = "nowe_cv.html") -> str:
        pal = self._get_palette()

        photo_uri = self._photo_base64()
        if photo_uri:
            photo_html = f'<img src="{photo_uri}" alt="{self.esc(self.info.name)}" class="cr-photo">'
        else:
            photo_html = (
                '<div class="cr-photo-placeholder">'
                f'<svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="{pal["dark"]}" stroke-width="1.6">'
                '<circle cx="12" cy="8" r="4"/>'
                '<path d="M4 20c0-4 4-6 8-6s8 2 8 6"/>'
                '</svg>'
                '</div>'
            )

        info = self.info
        contact_rows = []
        if info.location:
            contact_rows.append(f'<span class="cr-c-item"><span class="cr-c-icon">{self.ICO_PIN}</span><span>{self.esc(info.location)}</span></span>')
        if info.phone:
            contact_rows.append(f'<span class="cr-c-item"><span class="cr-c-icon">{self.ICO_PHONE}</span><span><a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a></span></span>')
        if info.email:
            contact_rows.append(f'<span class="cr-c-item"><span class="cr-c-icon">{self.ICO_MAIL}</span><span><a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a></span></span>')
        if info.linkedin:
            lbl = info.linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_rows.append(f'<span class="cr-c-item"><span class="cr-c-icon">{self.ICO_LINKEDIN}</span><span><a href="{self.esc(info.linkedin)}" target="_blank">{self.esc(lbl)}</a></span></span>')
        if info.github:
            lbl = info.github.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_rows.append(f'<span class="cr-c-item"><span class="cr-c-icon">{self.ICO_GITHUB}</span><span><a href="{self.esc(info.github)}" target="_blank">{self.esc(lbl)}</a></span></span>')
        if info.driver_license:
            contact_rows.append(f'<span class="cr-c-item"><span class="cr-c-icon">{self.ICO_CAR}</span><span>Prawo jazdy: {self.esc(info.driver_license)}</span></span>')
        
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

        # Soft Skills / Interests for sidebar
        interests_rows = []
        if self.data.skills_soft:
            for s in self.data.skills_soft:
                interests_rows.append(f'<span class="cr-pill">{self.esc(s)}</span>')
        interests_html = f'<div class="cr-pill-wrap">{"".join(interests_rows)}</div>' if interests_rows else ""

        # RIGHT COLUMN: Experience
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
            if pr.url:
                clean_url = pr.url.replace("https://", "").replace("http://", "").rstrip("/")
                icon = self.ICO_GITHUB if "github.com" in clean_url else self.ICO_LINK
                link = f'<a class="cr-link" href="{self.esc(pr.url)}" target="_blank" rel="noopener">{icon} <span>{self.esc(clean_url)}</span></a>'
            else:
                link = ""
            tech = f'<span class="cr-tech-tag">{self.esc(", ".join(pr.tech_stack))}</span>' if pr.tech_stack else ""
            desc = f'<p class="cr-desc">{self.esc(pr.description)}</p>' if pr.description else ""
            proj_rows.append(f"""
            <div class="cr-entry">
                <div class="cr-entry-header">
                    <span class="cr-entry-role">{self.esc(pr.name)}</span>
                    {link}
                </div>
                {tech}
                {desc}
            </div>""")
        projects_html = "\n".join(proj_rows)

        # Technical skills for sidebar (replaces soft skills in the sidebar)
        skills_sidebar_blocks = []
        if self.data.skills_categorized:
            for cat_name, sks in self.data.skills_categorized.items():
                pills = "".join(f'<span class="cr-sb-pill">{self.esc(s)}</span>' for s in sks)
                skills_sidebar_blocks.append(f"""
                <div class="cr-sb-skill-group">
                    <div class="cr-sb-skill-cat">{self.esc(cat_name)}</div>
                    <div class="cr-sb-skill-pills">{pills}</div>
                </div>""")
        elif self.data.skills_technical:
            pills = "".join(f'<span class="cr-sb-pill">{self.esc(s)}</span>' for s in self.data.skills_technical)
            skills_sidebar_blocks.append(f"""
            <div class="cr-sb-skill-group">
                <div class="cr-sb-skill-pills">{pills}</div>
            </div>""")
        skills_sidebar_html = "\n".join(skills_sidebar_blocks)

        css = f"""
        :root {{
            --cr-theme: {pal['primary']};
            --cr-light: {pal['light']};
            --cr-border: {pal['border']};
            --cr-dark: {pal['dark']};
            --cr-deep: {pal['deep']};
        }}

        {self._css_variables()}
        {self._css_reset()}
        {self._css_common_components()}

        body {{
            background: #f1f5f9;
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Inter', Roboto, 'Helvetica Neue', Arial, sans-serif;
            color: #1e293b;
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }}

        .cv-container {{
            max-width: 900px;
            margin: 20px auto;
            background: #ffffff;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border-radius: 6px;
            overflow: hidden;
        }}

        .cr-table {{
            width: 100%;
            border-collapse: collapse;
            border-spacing: 0;
            table-layout: fixed;
        }}

        /* Left Column (28% width) */
        .cr-sidebar {{
            width: 28%;
            background-color: #f8fafc;
            color: #2d3748;
            padding: 0 16px 20px 16px;
            vertical-align: top;
            box-sizing: border-box;
            border-right: 1px solid #edf2f7;
        }}

        /* The iconic arched header behind photo */
        .cr-arch-container {{
            background: var(--cr-theme);
            margin: 0 -16px 14px -16px;
            padding: 18px 12px 14px 12px;
            border-radius: 0 0 46px 46px;
            text-align: center;
            box-shadow: inset 0 -3px 8px rgba(0,0,0,0.06);
            transition: background 0.25s ease;
        }}

        .cr-photo {{
            width: 98px;
            height: 118px;
            object-fit: cover;
            border-radius: 14px;
            display: inline-block;
            border: 3px solid #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.14);
            background: #ffffff;
        }}

        .cr-photo-placeholder {{
            width: 98px;
            height: 118px;
            border-radius: 14px;
            background: #ffffff;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border: 3px solid #ffffff;
            box-shadow: 0 4px 12px rgba(0,0,0,0.14);
        }}

        .cr-sb-title {{
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #0f172a;
            border-bottom: 2px solid var(--cr-theme);
            display: inline-block;
            padding-bottom: 2px;
            margin-top: 12px;
            margin-bottom: 6px;
        }}

        /* Contact Bar in Top of Main Column */
        .cr-contact-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px 6px;
            align-items: center;
            margin-top: 3px;
            margin-bottom: 8px;
            padding-bottom: 7px;
            border-bottom: 1px solid #f1f5f9;
        }}

        .cr-c-item {{
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 10px;
            font-weight: 500;
            color: #334155;
            background: #f8fafc;
            padding: 2px 7px;
            border-radius: 5px;
            border: 1px solid #e2e8f0;
        }}

        .cr-c-item a {{
            color: #1e293b;
            text-decoration: none;
        }}

        .cr-c-item a:hover {{
            color: var(--cr-dark);
            text-decoration: underline;
        }}

        .cr-c-icon {{
            width: 17px;
            height: 17px;
            border-radius: 50%;
            background: var(--cr-light);
            color: var(--cr-dark);
            display: inline-flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            transition: all 0.2s ease;
        }}

        .cr-c-icon svg {{
            width: 9.5px;
            height: 9.5px;
            stroke: var(--cr-dark);
            margin-right: 0;
        }}

        .cr-edu-item {{
            margin-bottom: 10px;
        }}

        .cr-edu-item:last-child {{
            margin-bottom: 0;
        }}

        .cr-edu-degree {{
            font-size: 11px;
            font-weight: 700;
            color: #0f172a;
            line-height: 1.3;
        }}

        .cr-edu-inst {{
            font-size: 10.5px;
            color: #475569;
            margin-top: 1px;
        }}

        .cr-edu-date {{
            font-size: 10px;
            font-weight: 600;
            color: #64748b;
        }}

        .cr-lang-item {{
            font-size: 11px;
            color: #334155;
            margin-bottom: 5px;
        }}

        .cr-lvl {{
            color: #64748b;
            font-size: 10px;
        }}

        /* Right Column (Widened to 72%) */
        .cr-main {{
            width: 72%;
            background-color: #ffffff;
            color: #1e293b;
            padding: 20px 26px;
            vertical-align: top;
            box-sizing: border-box;
        }}

        .cr-name {{
            font-size: 29px;
            font-weight: 800;
            color: #0f172a;
            letter-spacing: -0.5px;
            text-transform: uppercase;
            line-height: 1.05;
            margin: 0 0 2px 0;
        }}

        .cr-title {{
            font-size: 12px;
            font-weight: 700;
            color: var(--cr-dark);
            letter-spacing: 0.8px;
            text-transform: uppercase;
            border-bottom: 2px solid var(--cr-theme);
            display: inline-block;
            padding-bottom: 1px;
            margin-bottom: 4px;
            transition: all 0.2s ease;
        }}

        .cr-summary {{
            font-size: 11.5px;
            color: #475569;
            text-align: justify;
            line-height: 1.45;
            margin-top: 2px;
            margin-bottom: 8px;
        }}

        .cr-summary p {{
            margin: 0;
            padding: 0;
        }}

        .cr-section-title {{
            font-size: 12px;
            font-weight: 800;
            color: #0f172a;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            border-bottom: 2px solid var(--cr-theme);
            display: inline-block;
            padding-bottom: 1px;
            margin-top: 10px;
            margin-bottom: 6px;
            transition: border-color 0.2s ease;
        }}

        .cr-entry {{
            margin-bottom: 9px;
            page-break-inside: avoid;
            border-left: 2px solid var(--cr-theme);
            padding-left: 10px;
            margin-left: 1px;
            transition: border-color 0.2s ease;
        }}

        .cr-entry-period {{
            font-size: 10.5px;
            font-weight: 700;
            color: var(--cr-dark);
            text-transform: uppercase;
            letter-spacing: 0.4px;
        }}

        .cr-entry-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 1px;
            margin-bottom: 3px;
        }}

        .cr-entry-role {{
            font-size: 13px;
            font-weight: 700;
            color: #0f172a;
        }}

        .cr-bullets {{
            list-style-type: disc;
            margin-left: 15px;
            font-size: 11px;
            color: #334155;
            line-height: 1.42;
        }}

        .cr-bullets li {{
            margin-bottom: 1.5px;
        }}

        .cr-tech {{
            font-size: 10.5px;
            color: #64748b;
            margin-bottom: 2px;
        }}

        .cr-tech-tag {{
            font-size: 10px;
            background: var(--cr-light);
            color: var(--cr-deep);
            padding: 1px 6px;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 2px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}

        .cr-desc {{
            font-size: 11px;
            color: #475569;
            line-height: 1.4;
            margin-top: 2px;
            margin-bottom: 0;
            text-align: justify;
        }}

        .cr-link {{
            font-size: 10px;
            color: var(--cr-deep);
            background: var(--cr-light);
            padding: 2px 7px;
            border-radius: 4px;
            border: 1px solid var(--cr-border);
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            transition: all 0.15s ease-in-out;
        }}

        .cr-link:hover {{
            background: var(--cr-border);
            text-decoration: none;
        }}

        .cr-link svg {{
            width: 11px;
            height: 11px;
            stroke: var(--cr-deep);
            flex-shrink: 0;
        }}

        .cr-sb-skill-group {{
            margin-bottom: 9px;
            page-break-inside: avoid;
        }}

        .cr-sb-skill-group:last-child {{
            margin-bottom: 0;
        }}

        .cr-sb-skill-cat {{
            font-size: 11px;
            font-weight: 700;
            color: #0f172a;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            margin-bottom: 4px;
        }}

        .cr-sb-skill-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }}

        .cr-sb-pill {{
            font-size: 10px;
            background: rgba(255, 255, 255, 0.75);
            color: #1e293b;
            padding: 2px 7px;
            border-radius: 4px;
            font-weight: 500;
            border: 1px solid rgba(0, 0, 0, 0.08);
            white-space: nowrap;
            display: inline-block;
        }}

        .cr-pill-wrap {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-top: 3px;
        }}

        .cr-pill {{
            font-size: 10.5px;
            background: var(--cr-light);
            color: var(--cr-deep);
            padding: 2px 8px;
            border-radius: 12px;
            border: 1px solid var(--cr-border);
            font-weight: 500;
            transition: all 0.2s ease;
        }}

        .cr-rodo {{
            margin-top: 24px;
            padding-top: 10px;
            border-top: 1px solid #edf2f7;
            font-size: 9.5px;
            color: #94a3b8;
            font-style: italic;
            text-align: justify;
            line-height: 1.4;
        }}

        {self._css_print_button()}
        {self._css_print_base()}

        @media print {{
            * {{
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}
            body, .cv-container, .cr-main, .cr-sidebar {{
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Arial, sans-serif !important;
            }}
            body {{
                background: #ffffff !important;
            }}
            .cv-container {{
                box-shadow: none !important;
                border: none !important;
                margin: 0 !important;
                padding: 0 !important;
                max-width: 100% !important;
                width: 100% !important;
            }}
            .cr-arch-container {{
                background-color: var(--cr-theme) !important;
            }}
            .cr-sidebar {{
                background-color: #f8fafc !important;
            }}
            .cr-c-item {{
                background-color: #f8fafc !important;
                border-color: #e2e8f0 !important;
            }}
            .cr-c-icon, .cr-tech-tag, .cr-pill, .cr-link {{
                background-color: var(--cr-light) !important;
                color: var(--cr-deep) !important;
                border-color: var(--cr-border) !important;
            }}
            .cr-sk-dots .dot.on {{
                background-color: var(--cr-theme) !important;
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
                <!-- LEFT ARCH COLUMN (28%) -->
                <td class="cr-sidebar">
                    <div class="cr-arch-container">
                        {photo_html}
                    </div>

                    {f'<div class="cr-sb-title">EDUKACJA</div>{edu_html}' if edu_html else ''}
                    {f'<div class="cr-sb-title">JĘZYKI OBCE</div>{lang_html}' if lang_html else ''}
                    {f'<div class="cr-sb-title">UMIEJĘTNOŚCI TECHNICZNE</div>{skills_sidebar_html}' if skills_sidebar_html else ''}
                </td>

                <!-- RIGHT MAIN COLUMN (72%) -->
                <td class="cr-main">
                    <h1 class="cr-name">{self.esc(self.info.name or "Kacper Pudełko")}</h1>
                    {f'<div class="cr-title">{self.esc(self.info.title)}</div>' if self.info.title else ''}
                    <div class="cr-contact-bar">{contact_html}</div>
                    {summary_p}

                    {f'<div class="cr-section-title">DOŚWIADCZENIE ZAWODOWE</div>{experience_html}' if experience_html else ''}
                    {f'<div class="cr-section-title">START-UP & INICJATYWY</div>{startups_html}' if startups_html else ''}
                    {f'<div class="cr-section-title">PROJEKTY WŁASNE</div>{projects_html}' if projects_html else ''}
                    

                    {f'<div class="cr-rodo">{self.esc(self.data.clause)}</div>' if self.data.clause else ''}
                </td>
            </tr>
        </table>
    </div>
</body>
</html>"""
        return self._write(output_path, full_html)
