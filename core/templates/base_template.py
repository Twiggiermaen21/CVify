"""
Abstract base class for all CV templates.
Provides common HTML helpers: escaping, contact bar, photo embedding, favicon, section generation.
"""
import os
import html
import base64
from abc import ABC, abstractmethod

try:
    from ..models import CVData
except ImportError:
    from core.models import CVData


class BaseTemplate(ABC):
    """Base class for all CV template builders."""

    SYSTEM_FONT_STACK = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'

    def __init__(self, cv_data: CVData):
        self.data = cv_data
        self.info = cv_data.personal_info
        self.primary = cv_data.theme_primary or "#1a365d"
        self.accent = cv_data.theme_accent or "#2b6cb0"

    @abstractmethod
    def build(self, output_path: str) -> str:
        """Build the HTML CV and write to output_path. Returns the output path."""
        ...

    # ── HTML helpers ──────────────────────────────────────────────────

    @staticmethod
    def esc(text: str) -> str:
        """HTML-escape a string."""
        return html.escape(str(text)) if text else ""

    def _write(self, output_path: str, html_content: str) -> str:
        """Write HTML string to file and return the path."""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return output_path

    # ── Photo helper ──────────────────────────────────────────────────

    def _photo_base64(self) -> str:
        """Return base64 data URI for the photo, or empty string if not available."""
        photo_path = self.info.photo
        if not photo_path:
            return ""

        # Resolve relative paths from project root
        if not os.path.isabs(photo_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            photo_path = os.path.join(base_dir, photo_path)

        if not os.path.isfile(photo_path):
            return ""

        try:
            ext = os.path.splitext(photo_path)[1].lower()
            mime_map = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
                ".svg": "image/svg+xml",
                ".ico": "image/x-icon",
            }
            mime = mime_map.get(ext, "image/jpeg")
            with open(photo_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            return f"data:{mime};base64,{b64}"
        except Exception:
            return ""

    def _photo_img(self, size: int = 90, css_class: str = "photo") -> str:
        """Return <img> tag for photo or empty string."""
        data_uri = self._photo_base64()
        if not data_uri:
            return ""
        return (
            f'<img src="{data_uri}" alt="{self.esc(self.info.name)}" '
            f'class="{css_class}" width="{size}" height="{size}" '
            f'style="border-radius:50%;object-fit:cover;width:{size}px;height:{size}px;">'
        )

    # ── Favicon helper ────────────────────────────────────────────────

    def _favicon_tag(self) -> str:
        """Return favicon link tag, embedded as base64 if the file exists."""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Try both spellings
        for fname in ("favicon.ico", "favoicon.ico"):
            icon_path = os.path.join(base_dir, "..", "web", "static", fname)
            icon_path = os.path.normpath(icon_path)
            if os.path.isfile(icon_path):
                try:
                    with open(icon_path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode("ascii")
                    return f'<link rel="icon" type="image/x-icon" href="data:image/x-icon;base64,{b64}">'
                except Exception:
                    pass
        return '<link rel="icon" type="image/x-icon" href="/static/favicon.ico">'

    # ── SVG vector icons (Zero childish emojis) ────────────────────────
    ICO_PIN = '<svg class="cv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"></path><circle cx="12" cy="10" r="3"></circle></svg>'
    ICO_PHONE = '<svg class="cv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>'
    ICO_MAIL = '<svg class="cv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path></svg>'
    ICO_LINKEDIN = '<svg class="cv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>'
    ICO_GITHUB = '<svg class="cv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"></path><path d="M9 18c-4.51 2-5-2-7-2"></path></svg>'
    ICO_GLOBE = '<svg class="cv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
    ICO_CAR = '<svg class="cv-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.5 2.8C2.1 11.1 2 11.5 2 12v4c0 .6.4 1 1 1h2"></path><circle cx="7" cy="17" r="2"></circle><path d="M9 17h6"></path><circle cx="17" cy="17" r="2"></circle></svg>'
    ICO_LINK = '<svg class="cv-ico-sm" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>'

    # ── Contact helpers ───────────────────────────────────────────────

    def _contact_items(self) -> list:
        """Return list of (icon_html, label_html) tuples for contact info."""
        info = self.info
        items = []
        if info.location:
            items.append((self.ICO_PIN, self.esc(info.location)))
        if info.phone:
            items.append((self.ICO_PHONE, f'<a href="tel:{self.esc(info.phone)}">{self.esc(info.phone)}</a>'))
        if info.email:
            items.append((self.ICO_MAIL, f'<a href="mailto:{self.esc(info.email)}">{self.esc(info.email)}</a>'))
        if info.linkedin:
            label = info.linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
            items.append((self.ICO_LINKEDIN, f'<a href="{self.esc(info.linkedin)}" target="_blank">{self.esc(label)}</a>'))
        if info.github:
            label = info.github.replace("https://", "").replace("http://", "").replace("www.", "")
            items.append((self.ICO_GITHUB, f'<a href="{self.esc(info.github)}" target="_blank">{self.esc(label)}</a>'))
        if info.portfolio:
            label = info.portfolio.replace("https://", "").replace("http://", "").replace("www.", "")
            items.append((self.ICO_GLOBE, f'<a href="{self.esc(info.portfolio)}" target="_blank">{self.esc(label)}</a>'))
        if info.driver_license:
            items.append((self.ICO_CAR, f'Prawo jazdy: {self.esc(info.driver_license)}'))
        return items

    def _contact_bar_html(self, separator: str = " &bull; ") -> str:
        """Return horizontal contact bar HTML."""
        items = self._contact_items()
        spans = [f'<span class="contact-entry">{ico} {label}</span>' for ico, label in items]
        return separator.join(spans)

    def _contact_vertical_html(self) -> str:
        """Return vertical contact list HTML."""
        items = self._contact_items()
        lines = [f'<div class="contact-item">{emoji} {label}</div>' for emoji, label in items]
        lines = [f'<div class="contact-item">{ico} {label}</div>' for ico, label in items]
        return "\n".join(lines)

    # ── Section content helpers ───────────────────────────────────────

    def _summary_content(self) -> str:
        """Return summary paragraphs HTML (without section wrapper)."""
        if not self.data.summary:
            return ""
        paras = self.data.summary.split("\n\n")
        return "".join(f"<p>{self.esc(p.strip())}</p>" for p in paras if p.strip())

    def _experience_entries(self) -> str:
        """Return experience entry cards HTML."""
        if not self.data.experience:
            return ""
        parts = []
        for item in self.data.experience:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in item.description)
            comp_loc = self.esc(item.company)
            if item.location:
                comp_loc += f", {self.esc(item.location)}"
            parts.append(f"""
            <div class="entry-card">
                <div class="entry-header">
                    <div>
                        <span class="entry-title">{self.esc(item.role)}</span>
                        <span class="entry-subtitle"> | {comp_loc}</span>
                    </div>
                    <span class="entry-date">{self.esc(item.period)}</span>
                </div>
                <ul class="bullet-list">{bullets}</ul>
            </div>""")
        return "\n".join(parts)

    def _startup_entries(self) -> str:
        """Return startup entry cards HTML."""
        if not self.data.startups:
            return ""
        parts = []
        for item in self.data.startups:
            bullets = "".join(f"<li>{self.esc(b)}</li>" for b in item.description)
            tech_tags = ""
            if item.tech_stack:
                tags = "".join(f'<span class="tech-badge">{self.esc(t)}</span>' for t in item.tech_stack)
                tech_tags = f'<div class="tech-badges-container">{tags}</div>'

            role_period = ""
            if item.role or item.period:
                role_part = f'<span class="entry-subtitle">{self.esc(item.role)}</span>' if item.role else ""
                period_part = f'<span class="entry-date">{self.esc(item.period)}</span>' if item.period else ""
                role_period = f'<div class="entry-meta">{role_part} {period_part}</div>'

            parts.append(f"""
            <div class="entry-card">
                <div class="entry-header">
                    <span class="entry-title accent">{self.esc(item.name)}</span>
                </div>
                {role_period}
                {tech_tags}
                <ul class="bullet-list">{bullets}</ul>
            </div>""")
        return "\n".join(parts)

    def _project_entries(self) -> str:
        """Return project entry cards HTML."""
        if not self.data.projects:
            return ""
        parts = []
        for item in self.data.projects:
            link = ""
            if item.url:
                clean_url = item.url.replace("https://", "").replace("http://", "").rstrip("/")
                icon = self.ICO_GITHUB if "github.com" in clean_url else self.ICO_LINK
                link = f'<a class="proj-link" href="{self.esc(item.url)}" target="_blank" rel="noopener">{icon} {self.esc(clean_url)}</a>'
            tech_tags = ""
            if item.tech_stack:
                tags = "".join(f'<span class="tech-badge">{self.esc(t)}</span>' for t in item.tech_stack)
                tech_tags = f'<div class="tech-badges-container">{tags}</div>'
            desc = f'<p class="proj-desc">{self.esc(item.description)}</p>' if item.description else ""
            highlights_html = ""
            if item.highlights:
                hl = "".join(f"<li>{self.esc(h)}</li>" for h in item.highlights)
                highlights_html = f'<ul class="bullet-list">{hl}</ul>'
            parts.append(f"""
            <div class="entry-card">
                <div class="entry-header">
                    <span class="entry-title">{self.esc(item.name)}</span>
                    {link}
                </div>
                {tech_tags}
                {desc}
                {highlights_html}
            </div>""")
        return "\n".join(parts)

    def _education_entries(self) -> str:
        """Return education entry cards HTML."""
        if not self.data.education:
            return ""
        parts = []
        for item in self.data.education:
            inst = self.esc(item.institution)
            if item.location:
                inst += f" – {self.esc(item.location)}"
            details = f'<p class="edu-details">{self.esc(item.details)}</p>' if item.details else ""
            parts.append(f"""
            <div class="entry-card">
                <div class="entry-header">
                    <div>
                        <span class="entry-title">{self.esc(item.degree)}</span>
                        <div class="entry-subtitle">{inst}</div>
                    </div>
                    <span class="entry-date">{self.esc(item.period)}</span>
                </div>
                {details}
            </div>""")
        return "\n".join(parts)

    def _skills_html(self) -> str:
        """Return skills section content HTML."""
        if not (self.data.skills_categorized or self.data.skills_technical or self.data.skills_soft):
            return ""
        cats = ""
        if self.data.skills_categorized:
            for cat_name, sks in self.data.skills_categorized.items():
                badges = "".join(f'<span class="skill-pill">{self.esc(s)}</span>' for s in sks)
                cats += f"""
                <div class="skill-category-row">
                    <span class="skill-cat-name">{self.esc(cat_name)}:</span>
                    <div class="skill-pill-group">{badges}</div>
                </div>"""
        elif self.data.skills_technical:
            badges = "".join(f'<span class="skill-pill">{self.esc(s)}</span>' for s in self.data.skills_technical)
            cats = f'<div class="skill-pill-group">{badges}</div>'

        soft = ""
        if self.data.skills_soft:
            soft_badges = "".join(f'<span class="skill-pill soft">{self.esc(s)}</span>' for s in self.data.skills_soft)
            soft = f"""
            <div class="skill-category-row" style="margin-top:8px;">
                <span class="skill-cat-name">Umiejętności miękkie:</span>
                <div class="skill-pill-group">{soft_badges}</div>
            </div>"""

        return f'<div class="skills-block">{cats}{soft}</div>'

    def _languages_html(self) -> str:
        """Return languages content HTML."""
        if not self.data.languages:
            return ""
        tags = []
        for lang in self.data.languages:
            lvl = f": {self.esc(lang.level)}" if lang.level else ""
            tags.append(f'<span class="lang-tag"><b>{self.esc(lang.language)}</b>{lvl}</span>')
        return f'<div class="languages-row">{"".join(tags)}</div>'

    def _certifications_html(self) -> str:
        """Return certifications list HTML."""
        if not self.data.certifications:
            return ""
        items = "".join(f"<li>{self.esc(c)}</li>" for c in self.data.certifications)
        return f'<ul class="cert-list">{items}</ul>'

    def _clause_html(self) -> str:
        """Return RODO clause footer HTML."""
        if not self.data.clause:
            return ""
        return f"""
        <footer class="rodo-footer">
            <p>{self.esc(self.data.clause)}</p>
        </footer>"""

    # ── Print button ──────────────────────────────────────────────────

    def _print_button(self) -> str:
        """Return floating print button HTML."""
        return '<button class="print-btn" onclick="window.print()">Drukuj / Zapisz jako PDF</button>'

    # ── Common CSS blocks ─────────────────────────────────────────────

    def _css_variables(self) -> str:
        """Return CSS :root variables block."""
        return f"""
        :root {{
            --primary: {self.primary};
            --accent: {self.accent};
            --accent-light: {self._lighten_color(self.accent)};
            --text-dark: #2d3748;
            --text-muted: #718096;
            --bg-pill: #edf2f7;
            --border-color: #e2e8f0;
        }}"""

    def _css_reset(self) -> str:
        """Return CSS reset / base styles."""
        return f"""
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: {self.SYSTEM_FONT_STACK};
            color: var(--text-dark);
            background: #f7fafc;
            line-height: 1.5;
            padding: 24px 12px;
        }}"""

    def _css_print_base(self) -> str:
        """Return base @media print rules."""
        return """
        @media print {
            @page {
                size: A4;
                margin: 12mm 14mm;
            }
            body {
                background: none;
                padding: 0;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
            .cv-container {
                box-shadow: none;
                padding: 0;
                max-width: 100%;
                border-radius: 0;
            }
            .print-btn {
                display: none !important;
            }
            a {
                text-decoration: none;
                color: inherit;
            }
        }"""

    def _css_print_button(self) -> str:
        """Return CSS for the print button."""
        return """
        .print-btn {
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
            z-index: 1000;
        }
        .print-btn:hover {
            background: var(--primary);
            transform: translateY(-2px);
        }"""

    def _css_common_components(self) -> str:
        """Return CSS for commonly used components across templates."""
        return """
        .cv-ico {
            width: 12px;
            height: 12px;
            display: inline-block;
            vertical-align: -1.5px;
            stroke: currentColor;
            margin-right: 3px;
        }
        .cv-ico-sm {
            width: 10px;
            height: 10px;
            display: inline-block;
            vertical-align: -0.5px;
            stroke: currentColor;
            margin-right: 3px;
        }
        .contact-entry {
            display: inline-flex;
            align-items: center;
        }
        .entry-card {
            margin-bottom: 12px;
            page-break-inside: avoid;
        }
        .entry-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 4px;
        }
        .entry-title {
            font-size: 13.5px;
            font-weight: 700;
            color: var(--text-dark);
        }
        .entry-title.accent {
            color: var(--accent);
        }
        .entry-subtitle {
            font-size: 13px;
            color: var(--text-muted);
        }
        .entry-meta {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 4px;
        }
        .entry-date {
            font-size: 12px;
            font-style: italic;
            color: var(--text-muted);
            white-space: nowrap;
        }
        .bullet-list {
            list-style-type: disc;
            margin-left: 20px;
            font-size: 12.5px;
            color: var(--text-dark);
        }
        .bullet-list li {
            margin-bottom: 3px;
        }
        .proj-link {
            font-size: 12px;
            color: var(--accent);
            text-decoration: none;
            word-break: break-all;
        }
        .proj-link:hover {
            text-decoration: underline;
        }
        .tech-badges-container {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin: 4px 0;
        }
        .tech-badge {
            font-size: 11px;
            background: var(--accent-light);
            color: var(--accent);
            font-weight: 500;
            padding: 2px 7px;
            border-radius: 4px;
            border: 1px solid #bee3f8;
        }
        .proj-desc {
            font-size: 12.5px;
            color: var(--text-dark);
            margin-top: 3px;
            text-align: justify;
        }
        .skills-block {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .skill-category-row {
            display: flex;
            align-items: baseline;
            gap: 8px;
            flex-wrap: wrap;
        }
        .skill-cat-name {
            font-size: 12.5px;
            font-weight: 700;
            color: var(--primary);
            min-width: 140px;
        }
        .skill-pill-group {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        .skill-pill {
            font-size: 12px;
            background: var(--bg-pill);
            color: var(--text-dark);
            padding: 2px 8px;
            border-radius: 4px;
            border: 1px solid var(--border-color);
        }
        .skill-pill.soft {
            background: #f7fafc;
            font-size: 11.5px;
        }
        .languages-row {
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
        }
        .lang-tag {
            font-size: 12.5px;
            background: var(--bg-pill);
            padding: 3px 10px;
            border-radius: 4px;
            border: 1px solid var(--border-color);
        }
        .cert-list {
            list-style-type: disc;
            margin-left: 20px;
            font-size: 12.5px;
        }
        .edu-details {
            font-size: 12.5px;
            color: var(--text-muted);
            margin-top: 2px;
        }
        .rodo-footer {
            margin-top: 28px;
            padding-top: 10px;
            border-top: 1px solid var(--border-color);
            font-size: 10.5px;
            color: var(--text-muted);
            font-style: italic;
            text-align: justify;
            line-height: 1.4;
        }"""

    # ── Utility ───────────────────────────────────────────────────────

    @staticmethod
    def _lighten_color(hex_color: str) -> str:
        """Create a very light version of a hex color for backgrounds."""
        try:
            hex_color = hex_color.lstrip("#")
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            # Mix with white at 90%
            r = int(r + (255 - r) * 0.90)
            g = int(g + (255 - g) * 0.90)
            b = int(b + (255 - b) * 0.90)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return "#ebf8ff"

    def _html_head(self, css: str) -> str:
        """Return complete <head> block."""
        return f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CV – {self.esc(self.info.name)}</title>
    {self._favicon_tag()}
    <style>
{css}
    </style>
</head>"""
