"""
CV Template registry.
Maps template names to builder classes for HTML CV generation.
Includes 1:1 recreations of provided designs (Onyx, Blush, Creative, Boxes)
as well as standard templates (Modern, Classic, Sidebar, Elegant, Compact).
"""

from .classic import ClassicTemplate
from .modern import ModernTemplate
from .sidebar import SidebarTemplate
from .elegant import ElegantTemplate
from .compact import CompactTemplate
from .onyx import OnyxTemplate
from .blush import BlushTemplate
from .creative import CreativeTemplate
from .boxes import BoxesTemplate
from .rose import RoseTemplate

TEMPLATES = {
    # 1:1 Recreated designs from user images
    "onyx": OnyxTemplate,          # Image 1: Laura Kubiak black sidebar & checkmarks
    "blush": BlushTemplate,        # Image 2: Laura Kubiak warm beige / blush
    "creative": CreativeTemplate,  # Image 3: Anne Robertson yellow arch header
    "boxes": BoxesTemplate,        # Image 4: Adam Paprocki technical grid & sliders
    "rose": RoseTemplate,          # Image 5: Aleksandra Nowak cursive burgundy & blush

    # Additional standard templates
    "modern": ModernTemplate,
    "sidebar": SidebarTemplate,
    "classic": ClassicTemplate,
    "elegant": ElegantTemplate,
    "compact": CompactTemplate,
}


def get_template(name: str):
    """Return template class by name. Raises KeyError if not found."""
    key = name.lower().strip()
    if key not in TEMPLATES:
        available = ", ".join(sorted(TEMPLATES.keys()))
        raise KeyError(f"Unknown template '{name}'. Available: {available}")
    return TEMPLATES[key]


def list_templates() -> list:
    """Return sorted list of available template names."""
    return sorted(TEMPLATES.keys())
