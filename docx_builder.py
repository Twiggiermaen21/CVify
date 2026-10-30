"""
DOCX CV Generator.
Creates a modern, executive Word document (.docx) from CVData.
Features professional typography, custom color palette, elegant section dividers,
clickable links, and clean bulleted hierarchies.
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from models import CVData

# Color Palette Constants
COLOR_NAVY_HEX = "1A365D"
COLOR_ACCENT_HEX = "2B6CB0"
COLOR_MUTED_HEX = "718096"
COLOR_TEXT_HEX = "2D3748"

COLOR_NAVY = RGBColor(26, 54, 93)       # #1A365D - Main headers
COLOR_ACCENT = RGBColor(43, 108, 176)   # #2B6CB0 - Subheadings, Links
COLOR_TEXT = RGBColor(45, 55, 72)       # #2D3748 - Body text
COLOR_MUTED = RGBColor(113, 128, 150)   # #718096 - Dates, meta

FONT_FAMILY = "Calibri"

class DocxCVBuilder:
    def __init__(self, cv_data: CVData):
        self.data = cv_data
        self.doc = docx.Document()
        self._setup_page()

    def _setup_page(self):
        section = self.doc.sections[0]
        section.top_margin = Inches(0.55)
        section.bottom_margin = Inches(0.55)
        section.left_margin = Inches(0.65)
        section.right_margin = Inches(0.65)

    def _add_bottom_border(self, paragraph, color_hex=COLOR_NAVY_HEX, sz="12"):
        pPr = paragraph._element.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), sz)
        bottom.set(qn('w:space'), '3')
        bottom.set(qn('w:color'), color_hex)
        pBdr.append(bottom)
        pPr.append(pBdr)

    def _add_hyperlink(self, paragraph, url: str, text: str):
        if not url.startswith("http"):
            url = "https://" + url
        part = paragraph.part
        r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
        hyperlink = OxmlElement('w:hyperlink')
        hyperlink.set(qn('r:id'), r_id)
        
        new_run = OxmlElement('w:r')
        rPr = OxmlElement('w:rPr')
        
        # Color
        c = OxmlElement('w:color')
        c.set(qn('w:val'), COLOR_ACCENT_HEX)
        rPr.append(c)

        # Underline
        u = OxmlElement('w:u')
        u.set(qn('w:val'), 'single')
        rPr.append(u)

        # Font
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:ascii'), FONT_FAMILY)
        rFonts.set(qn('w:hAnsi'), FONT_FAMILY)
        rPr.append(rFonts)

        new_run.append(rPr)
        text_node = OxmlElement('w:t')
        text_node.text = text
        new_run.append(text_node)
        hyperlink.append(new_run)
        paragraph._p.append(hyperlink)

    def _add_section_heading(self, title: str):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        
        run = p.add_run(title.upper())
        run.font.name = FONT_FAMILY
        run.font.size = Pt(11.5)
        run.font.bold = True
        run.font.color.rgb = COLOR_NAVY
        
        self._add_bottom_border(p, COLOR_NAVY_HEX, sz="10")

    def build(self, output_path: str = "nowe_cv.docx"):
        self._build_header()
        
        if self.data.summary:
            self._build_summary()

        if self.data.experience:
            self._build_experience()

        if self.data.startups:
            self._build_startups()

        if self.data.projects:
            self._build_projects()

        if self.data.skills_technical or self.data.skills_soft:
            self._build_skills()

        if self.data.education:
            self._build_education()

        if self.data.languages:
            self._build_languages()

        if self.data.certifications:
            self._build_certifications()

        if self.data.clause:
            self._build_clause()

        self.doc.save(output_path)
        return output_path

    def _build_header(self):
        info = self.data.personal_info
        
        # Candidate Name
        p_name = self.doc.add_paragraph()
        p_name.paragraph_format.space_before = Pt(0)
        p_name.paragraph_format.space_after = Pt(1)
        r_name = p_name.add_run(info.name if info.name else "Kacper Pudełko")
        r_name.font.name = FONT_FAMILY
        r_name.font.size = Pt(22)
        r_name.font.bold = True
        r_name.font.color.rgb = COLOR_NAVY

        # Professional Title
        if info.title:
            p_title = self.doc.add_paragraph()
            p_title.paragraph_format.space_before = Pt(0)
            p_title.paragraph_format.space_after = Pt(4)
            r_title = p_title.add_run(info.title)
            r_title.font.name = FONT_FAMILY
            r_title.font.size = Pt(12)
            r_title.font.bold = True
            r_title.font.color.rgb = COLOR_ACCENT

        # Contact Info Bar
        p_contact = self.doc.add_paragraph()
        p_contact.paragraph_format.space_before = Pt(2)
        p_contact.paragraph_format.space_after = Pt(8)

        items = []
        if info.location:
            items.append(("text", info.location))
        if info.phone:
            items.append(("text", info.phone))
        if info.email:
            items.append(("link", info.email, f"mailto:{info.email}"))
        if info.linkedin:
            label = info.linkedin.replace("https://", "").replace("http://", "").replace("www.", "")
            items.append(("link", label, info.linkedin))
        if info.github:
            label = info.github.replace("https://", "").replace("http://", "").replace("www.", "")
            items.append(("link", label, info.github))
        if info.driver_license:
            items.append(("text", f"Prawo jazdy: {info.driver_license}"))

        for idx, item in enumerate(items):
            if item[0] == "text":
                r = p_contact.add_run(item[1])
                r.font.name = FONT_FAMILY
                r.font.size = Pt(9.5)
                r.font.color.rgb = COLOR_MUTED
            elif item[0] == "link":
                self._add_hyperlink(p_contact, item[2], item[1])

            if idx < len(items) - 1:
                r_sep = p_contact.add_run("  •  ")
                r_sep.font.name = FONT_FAMILY
                r_sep.font.size = Pt(9.5)
                r_sep.font.color.rgb = COLOR_MUTED

        self._add_bottom_border(p_contact, COLOR_ACCENT_HEX, sz="6")

    def _build_summary(self):
        self._add_section_heading("Profil zawodowy")
        paragraphs = self.data.summary.split("\n\n")
        for para_text in paragraphs:
            if not para_text.strip():
                continue
            p = self.doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            r = p.add_run(para_text.strip())
            r.font.name = FONT_FAMILY
            r.font.size = Pt(9.5)
            r.font.color.rgb = COLOR_TEXT

    def _build_experience(self):
        self._add_section_heading("Doświadczenie zawodowe")
        for item in self.data.experience:
            # Header line: Role and Period in 2-column borderless table
            table = self.doc.add_table(rows=1, cols=2)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = False

            # Set widths (approx 5.0 in and 2.0 in)
            table.columns[0].width = Inches(5.0)
            table.columns[1].width = Inches(2.0)

            c0 = table.cell(0, 0)
            c1 = table.cell(0, 1)

            # Role & Company in c0
            p0 = c0.paragraphs[0]
            p0.paragraph_format.space_before = Pt(4)
            p0.paragraph_format.space_after = Pt(1)
            r_role = p0.add_run(item.role)
            r_role.font.name = FONT_FAMILY
            r_role.font.size = Pt(10)
            r_role.font.bold = True
            r_role.font.color.rgb = COLOR_TEXT

            comp_str = item.company
            if item.location:
                comp_str += f", {item.location}"
            if comp_str:
                r_comp = p0.add_run(f" | {comp_str}")
                r_comp.font.name = FONT_FAMILY
                r_comp.font.size = Pt(9.5)
                r_comp.font.color.rgb = COLOR_MUTED

            # Period in c1 (right aligned)
            p1 = c1.paragraphs[0]
            p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p1.paragraph_format.space_before = Pt(4)
            p1.paragraph_format.space_after = Pt(1)
            r_per = p1.add_run(item.period)
            r_per.font.name = FONT_FAMILY
            r_per.font.size = Pt(9)
            r_per.font.italic = True
            r_per.font.color.rgb = COLOR_MUTED

            # Bullets
            for b in item.description:
                p_b = self.doc.add_paragraph(style='List Bullet')
                p_b.paragraph_format.space_before = Pt(1)
                p_b.paragraph_format.space_after = Pt(1)
                r_b = p_b.add_run(b)
                r_b.font.name = FONT_FAMILY
                r_b.font.size = Pt(9)
                r_b.font.color.rgb = COLOR_TEXT

    def _build_startups(self):
        self._add_section_heading("Start-up & Własne Inicjatywy")
        for item in self.data.startups:
            p = self.doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(1)
            r_name = p.add_run(item.name)
            r_name.font.name = FONT_FAMILY
            r_name.font.size = Pt(10)
            r_name.font.bold = True
            r_name.font.color.rgb = COLOR_ACCENT

            for b in item.description:
                p_b = self.doc.add_paragraph(style='List Bullet')
                p_b.paragraph_format.space_before = Pt(1)
                p_b.paragraph_format.space_after = Pt(1)
                r_b = p_b.add_run(b)
                r_b.font.name = FONT_FAMILY
                r_b.font.size = Pt(9)
                r_b.font.color.rgb = COLOR_TEXT

    def _build_projects(self):
        self._add_section_heading("Wybrane Projekty")
        for item in self.data.projects:
            p = self.doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(1)

            # Project Name
            r_name = p.add_run(f"• {item.name}")
            r_name.font.name = FONT_FAMILY
            r_name.font.size = Pt(10)
            r_name.font.bold = True
            r_name.font.color.rgb = COLOR_TEXT

            # Link
            if item.url:
                p.add_run("  ")
                self._add_hyperlink(p, item.url, item.url)

            # Tech Stack line
            if item.tech_stack:
                p_tech = self.doc.add_paragraph()
                p_tech.paragraph_format.space_before = Pt(0)
                p_tech.paragraph_format.space_after = Pt(1)
                r_stack_label = p_tech.add_run("  Technologie: ")
                r_stack_label.font.name = FONT_FAMILY
                r_stack_label.font.size = Pt(8.5)
                r_stack_label.font.bold = True
                r_stack_label.font.color.rgb = COLOR_MUTED

                r_stack = p_tech.add_run(", ".join(item.tech_stack))
                r_stack.font.name = FONT_FAMILY
                r_stack.font.size = Pt(8.5)
                r_stack.font.italic = True
                r_stack.font.color.rgb = COLOR_ACCENT

            # Description
            if item.description:
                p_desc = self.doc.add_paragraph()
                p_desc.paragraph_format.space_before = Pt(1)
                p_desc.paragraph_format.space_after = Pt(3)
                p_desc.paragraph_format.left_indent = Inches(0.2)
                r_desc = p_desc.add_run(item.description)
                r_desc.font.name = FONT_FAMILY
                r_desc.font.size = Pt(9)
                r_desc.font.color.rgb = COLOR_TEXT

    def _build_skills(self):
        self._add_section_heading("Umiejętności i Technologie")

        # Categorized technical skills
        if self.data.skills_categorized:
            for cat_name, skills in self.data.skills_categorized.items():
                p = self.doc.add_paragraph()
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                
                r_cat = p.add_run(f"• {cat_name}: ")
                r_cat.font.name = FONT_FAMILY
                r_cat.font.size = Pt(9.5)
                r_cat.font.bold = True
                r_cat.font.color.rgb = COLOR_NAVY

                r_skills = p.add_run(", ".join(skills))
                r_skills.font.name = FONT_FAMILY
                r_skills.font.size = Pt(9.5)
                r_skills.font.color.rgb = COLOR_TEXT
        elif self.data.skills_technical:
            for line in self.data.skills_technical:
                p = self.doc.add_paragraph(style='List Bullet')
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                r = p.add_run(line)
                r.font.name = FONT_FAMILY
                r.font.size = Pt(9.5)
                r.font.color.rgb = COLOR_TEXT

        # Soft skills
        if self.data.skills_soft:
            p_soft_title = self.doc.add_paragraph()
            p_soft_title.paragraph_format.space_before = Pt(3)
            p_soft_title.paragraph_format.space_after = Pt(1)
            r_st = p_soft_title.add_run("• Umiejętności interpersonalne i organizacyjne: ")
            r_st.font.name = FONT_FAMILY
            r_st.font.size = Pt(9.5)
            r_st.font.bold = True
            r_st.font.color.rgb = COLOR_NAVY

            r_soft = p_soft_title.add_run(", ".join(self.data.skills_soft))
            r_soft.font.name = FONT_FAMILY
            r_soft.font.size = Pt(9)
            r_soft.font.color.rgb = COLOR_TEXT

    def _build_education(self):
        self._add_section_heading("Wykształcenie")
        for item in self.data.education:
            table = self.doc.add_table(rows=1, cols=2)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = False
            table.columns[0].width = Inches(5.0)
            table.columns[1].width = Inches(2.0)

            c0 = table.cell(0, 0)
            c1 = table.cell(0, 1)

            p0 = c0.paragraphs[0]
            p0.paragraph_format.space_before = Pt(3)
            p0.paragraph_format.space_after = Pt(1)
            r_deg = p0.add_run(item.degree)
            r_deg.font.name = FONT_FAMILY
            r_deg.font.size = Pt(9.5)
            r_deg.font.bold = True
            r_deg.font.color.rgb = COLOR_TEXT

            inst_str = item.institution
            if item.location:
                inst_str += f" - {item.location}"
            if inst_str:
                r_inst = p0.add_run(f"\n{inst_str}")
                r_inst.font.name = FONT_FAMILY
                r_inst.font.size = Pt(9)
                r_inst.font.color.rgb = COLOR_MUTED

            p1 = c1.paragraphs[0]
            p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p1.paragraph_format.space_before = Pt(3)
            p1.paragraph_format.space_after = Pt(1)
            r_per = p1.add_run(item.period)
            r_per.font.name = FONT_FAMILY
            r_per.font.size = Pt(9)
            r_per.font.italic = True
            r_per.font.color.rgb = COLOR_MUTED

    def _build_languages(self):
        self._add_section_heading("Języki")
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)

        lang_strs = []
        for l in self.data.languages:
            if l.level:
                lang_strs.append(f"{l.language}: {l.level}")
            else:
                lang_strs.append(l.language)

        r = p.add_run("   •   ".join(lang_strs))
        r.font.name = FONT_FAMILY
        r.font.size = Pt(9.5)
        r.font.color.rgb = COLOR_TEXT

    def _build_certifications(self):
        self._add_section_heading("Certyfikaty i Kursy")
        for cert in self.data.certifications:
            p = self.doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(cert)
            r.font.name = FONT_FAMILY
            r.font.size = Pt(9)
            r.font.color.rgb = COLOR_TEXT

    def _build_clause(self):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(0)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        r = p.add_run(self.data.clause)
        r.font.name = FONT_FAMILY
        r.font.size = Pt(8)
        r.font.italic = True
        r.font.color.rgb = COLOR_MUTED

