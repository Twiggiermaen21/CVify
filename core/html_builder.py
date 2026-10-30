"""
HTML CV Generator.
Creates a responsive, modern HTML CV with print stylesheet (@media print).
Opening this file in any browser allows 1-click printing or saving as a clean PDF (Ctrl+P).
"""
import os
import html
try:
    from .models import CVData
except ImportError:
    from models import CVData

class HtmlCVBuilder:
    def __init__(self, cv_data: CVData):
        self.data = cv_data

    def build(self, output_path: str = "nowe_cv.html") -> str:
        info = self.data.personal_info
        
        # Build contact items
        contact_html_parts = []
        if info.location:
            contact_html_parts.append(f'<span>📍 {html.escape(info.location)}</span>')
        if info.phone:
            contact_html_parts.append(f'<span>📞 <a href="tel:{html.escape(info.phone)}">{html.escape(info.phone)}</a></span>')
        if info.email:
            contact_html_parts.append(f'<span>✉️ <a href="mailto:{html.escape(info.email)}">{html.escape(info.email)}</a></span>')
        if info.linkedin:
            label = info.linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_html_parts.append(f'<span>💼 <a href="{html.escape(info.linkedin)}" target="_blank">{html.escape(label)}</a></span>')
        if info.github:
            label = info.github.replace("https://", "").replace("http://", "").replace("www.", "")
            contact_html_parts.append(f'<span>🐙 <a href="{html.escape(info.github)}" target="_blank">{html.escape(label)}</a></span>')
        if info.driver_license:
            contact_html_parts.append(f'<span>🚗 Prawo jazdy: {html.escape(info.driver_license)}</span>')

        contact_bar = " &bull; ".join(contact_html_parts)

        # Build summary
        summary_html = ""
        if self.data.summary:
            paras = self.data.summary.split("\n\n")
            p_tags = "".join(f"<p>{html.escape(p.strip())}</p>" for p in paras if p.strip())
            summary_html = f"""
            <section class="section">
                <h2 class="section-title">Profil zawodowy</h2>
                <div class="summary-content">{p_tags}</div>
            </section>
            """

        # Build experience
        experience_html = ""
        if self.data.experience:
            items_html = ""
            for item in self.data.experience:
                bullets = "".join(f"<li>{html.escape(b)}</li>" for b in item.description)
                comp_loc = html.escape(item.company)
                if item.location:
                    comp_loc += f", {html.escape(item.location)}"
                items_html += f"""
                <div class="entry-card">
                    <div class="entry-header">
                        <div>
                            <span class="entry-title">{html.escape(item.role)}</span>
                            <span class="entry-subtitle"> | {comp_loc}</span>
                        </div>
                        <span class="entry-date">{html.escape(item.period)}</span>
                    </div>
                    <ul class="bullet-list">{bullets}</ul>
                </div>
                """
            experience_html = f"""
            <section class="section">
                <h2 class="section-title">Doświadczenie zawodowe</h2>
                {items_html}
            </section>
            """

        # Build startups
        startups_html = ""
        if self.data.startups:
            items_html = ""
            for item in self.data.startups:
                bullets = "".join(f"<li>{html.escape(b)}</li>" for b in item.description)
                items_html += f"""
                <div class="entry-card">
                    <div class="entry-header">
                        <span class="entry-title accent">{html.escape(item.name)}</span>
                    </div>
                    <ul class="bullet-list">{bullets}</ul>
                </div>
                """
            startups_html = f"""
            <section class="section">
                <h2 class="section-title">Start-up & Własne Inicjatywy</h2>
                {items_html}
            </section>
            """

        # Build projects
        projects_html = ""
        if self.data.projects:
            items_html = ""
            for item in self.data.projects:
                link_html = ""
                if item.url:
                    link_html = f'<a class="proj-link" href="{html.escape(item.url)}" target="_blank">🔗 {html.escape(item.url)}</a>'
                
                tech_tags = "".join(f'<span class="tech-badge">{html.escape(t)}</span>' for t in item.tech_stack)
                tech_container = f'<div class="tech-badges-container">{tech_tags}</div>' if tech_tags else ""

                desc_html = f'<p class="proj-desc">{html.escape(item.description)}</p>' if item.description else ""

                items_html += f"""
                <div class="entry-card">
                    <div class="entry-header">
                        <span class="entry-title">{html.escape(item.name)}</span>
                        {link_html}
                    </div>
                    {tech_container}
                    {desc_html}
                </div>
                """
            projects_html = f"""
            <section class="section">
                <h2 class="section-title">Wybrane Projekty</h2>
                {items_html}
            </section>
            """

        # Build skills
        skills_html = ""
        if self.data.skills_categorized or self.data.skills_technical or self.data.skills_soft:
            cats_html = ""
            if self.data.skills_categorized:
                for cat_name, sks in self.data.skills_categorized.items():
                    badges = "".join(f'<span class="skill-pill">{html.escape(s)}</span>' for s in sks)
                    cats_html += f"""
                    <div class="skill-category-row">
                        <span class="skill-cat-name">{html.escape(cat_name)}:</span>
                        <div class="skill-pill-group">{badges}</div>
                    </div>
                    """
            elif self.data.skills_technical:
                badges = "".join(f'<span class="skill-pill">{html.escape(s)}</span>' for s in self.data.skills_technical)
                cats_html += f'<div class="skill-pill-group">{badges}</div>'

            soft_html = ""
            if self.data.skills_soft:
                soft_badges = "".join(f'<span class="skill-pill soft">{html.escape(s)}</span>' for s in self.data.skills_soft)
                soft_html = f"""
                <div class="skill-category-row" style="margin-top: 8px;">
                    <span class="skill-cat-name">Umiejętności miękkie:</span>
                    <div class="skill-pill-group">{soft_badges}</div>
                </div>
                """

            skills_html = f"""
            <section class="section">
                <h2 class="section-title">Umiejętności i Technologie</h2>
                <div class="skills-block">
                    {cats_html}
                    {soft_html}
                </div>
            </section>
            """

        # Build education
        education_html = ""
        if self.data.education:
            items_html = ""
            for item in self.data.education:
                inst_str = html.escape(item.institution)
                if item.location:
                    inst_str += f" - {html.escape(item.location)}"
                items_html += f"""
                <div class="entry-card">
                    <div class="entry-header">
                        <div>
                            <span class="entry-title">{html.escape(item.degree)}</span>
                            <div class="entry-subtitle">{inst_str}</div>
                        </div>
                        <span class="entry-date">{html.escape(item.period)}</span>
                    </div>
                </div>
                """
            education_html = f"""
            <section class="section">
                <h2 class="section-title">Wykształcenie</h2>
                {items_html}
            </section>
            """

        # Build languages
        languages_html = ""
        if self.data.languages:
            items_html = ""
            for l in self.data.languages:
                lvl = f": {html.escape(l.level)}" if l.level else ""
                items_html += f'<span class="lang-tag"><b>{html.escape(l.language)}</b>{lvl}</span>'
            languages_html = f"""
            <section class="section">
                <h2 class="section-title">Języki obce</h2>
                <div class="languages-row">{items_html}</div>
            </section>
            """

        # Build clause
        clause_html = ""
        if self.data.clause:
            clause_html = f"""
            <footer class="rodo-footer">
                <p>{html.escape(self.data.clause)}</p>
            </footer>
            """

        full_html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV - {html.escape(info.name)}</title>
    <style>
        :root {{
            --primary: #1a365d;
            --accent: #2b6cb0;
            --accent-light: #ebf8ff;
            --text-dark: #2d3748;
            --text-muted: #718096;
            --bg-pill: #edf2f7;
            --border-color: #e2e8f0;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            color: var(--text-dark);
            background: #f7fafc;
            line-height: 1.5;
            padding: 24px 12px;
        }}

        .cv-container {{
            max-width: 860px;
            margin: 0 auto;
            background: #ffffff;
            padding: 40px 48px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            border-radius: 8px;
        }}

        .header {{
            border-bottom: 2px solid var(--accent);
            padding-bottom: 12px;
            margin-bottom: 20px;
        }}

        .name {{
            font-size: 26px;
            font-weight: 700;
            color: var(--primary);
            letter-spacing: -0.5px;
        }}

        .title {{
            font-size: 15px;
            font-weight: 600;
            color: var(--accent);
            margin-top: 2px;
            margin-bottom: 8px;
        }}

        .contact-bar {{
            font-size: 13px;
            color: var(--text-muted);
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }}

        .contact-bar a {{
            color: var(--accent);
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
            border-bottom: 1.5px solid var(--primary);
            padding-bottom: 4px;
            margin-bottom: 10px;
            letter-spacing: 0.5px;
        }}

        .summary-content p {{
            font-size: 13px;
            margin-bottom: 8px;
            color: var(--text-dark);
            text-align: justify;
        }}

        .entry-card {{
            margin-bottom: 12px;
            page-break-inside: avoid;
        }}

        .entry-header {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 4px;
        }}

        .entry-title {{
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-dark);
        }}

        .entry-title.accent {{
            color: var(--accent);
        }}

        .entry-subtitle {{
            font-size: 13px;
            color: var(--text-muted);
        }}

        .entry-date {{
            font-size: 12px;
            font-style: italic;
            color: var(--text-muted);
            white-space: nowrap;
        }}

        .bullet-list {{
            list-style-type: disc;
            margin-left: 20px;
            font-size: 12.5px;
            color: var(--text-dark);
        }}

        .bullet-list li {{
            margin-bottom: 3px;
        }}

        .proj-link {{
            font-size: 12px;
            color: var(--accent);
            text-decoration: none;
            word-break: break-all;
        }}

        .proj-link:hover {{
            text-decoration: underline;
        }}

        .tech-badges-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin: 4px 0;
        }}

        .tech-badge {{
            font-size: 11px;
            background: var(--accent-light);
            color: var(--accent);
            font-weight: 500;
            padding: 2px 7px;
            border-radius: 4px;
            border: 1px solid #bee3f8;
        }}

        .proj-desc {{
            font-size: 12.5px;
            color: var(--text-dark);
            margin-top: 3px;
            text-align: justify;
        }}

        .skills-block {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .skill-category-row {{
            display: flex;
            align-items: baseline;
            gap: 8px;
        }}

        .skill-cat-name {{
            font-size: 12.5px;
            font-weight: 700;
            color: var(--primary);
            min-width: 140px;
        }}

        .skill-pill-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}

        .skill-pill {{
            font-size: 12px;
            background: var(--bg-pill);
            color: var(--text-dark);
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid var(--border-color);
        }}

        .skill-pill.soft {{
            background: #f7fafc;
            font-size: 11.5px;
        }}

        .languages-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
        }}

        .lang-tag {{
            font-size: 12.5px;
            background: var(--bg-pill);
            padding: 3px 10px;
            border-radius: 4px;
            border: 1px solid var(--border-color);
        }}

        .rodo-footer {{
            margin-top: 28px;
            padding-top: 10px;
            border-top: 1px solid var(--border-color);
            font-size: 10.5px;
            color: var(--text-muted);
            font-style: italic;
            text-align: justify;
            line-height: 1.4;
        }}

        .print-btn {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--accent);
            color: #ffffff;
            border: none;
            padding: 12px 20px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            box-shadow: 0 4px 14px rgba(43, 108, 176, 0.4);
            transition: all 0.2s ease;
        }}

        .print-btn:hover {{
            background: var(--primary);
            transform: translateY(-2px);
        }}

        @media print {{
            @page {{
                size: A4;
                margin: 12mm 14mm;
            }}

            body {{
                background: none;
                padding: 0;
            }}

            .cv-container {{
                box-shadow: none;
                padding: 0;
                max-width: 100%;
                border-radius: 0;
            }}

            .print-btn {{
                display: none;
            }}

            a {{
                text-decoration: none;
                color: inherit;
            }}
        }}
    </style>
</head>
<body>
    <button class="print-btn" onclick="window.print()">🖨️ Drukuj / Zapisz jako PDF</button>
    <div class="cv-container">
        <header class="header">
            <h1 class="name">{html.escape(info.name if info.name else "Kacper Pudełko")}</h1>
            {f'<div class="title">{html.escape(info.title)}</div>' if info.title else ''}
            <div class="contact-bar">{contact_bar}</div>
        </header>

        {summary_html}
        {experience_html}
        {startups_html}
        {projects_html}
        {skills_html}
        {education_html}
        {languages_html}
        {clause_html}
    </div>
</body>
</html>
"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_html)
        return output_path

