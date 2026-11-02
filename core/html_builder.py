"""
HTML CV Generator.
Delegates generation to modular templates (Modern, Classic, Sidebar, Elegant, Compact).
Opening the generated HTML file in any browser allows 1-click printing or saving as a clean PDF (Ctrl+P).
"""
import os
from typing import Optional

try:
    from .models import CVData
    from .templates import get_template, TEMPLATES
except ImportError:
    from models import CVData
    from templates import get_template, TEMPLATES


class HtmlCVBuilder:
    """Builder that delegates to specific CV layout templates."""

    def __init__(self, cv_data: CVData, template_name: Optional[str] = None):
        self.data = cv_data
        
        # Determine template
        requested = template_name or getattr(cv_data, "template", None) or "modern"
        requested = str(requested).lower().strip()
        if requested not in TEMPLATES:
            requested = "modern"
        
        template_cls = get_template(requested)
        self.template_instance = template_cls(self.data)

    def build(self, output_path: str = "nowe_cv.html") -> str:
        """Generates the CV using the configured template."""
        return self.template_instance.build(output_path)
