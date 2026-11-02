"""
Data models for structured CV information.
Supports JSON and YAML serialization/deserialization for easy AI and human editing.
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
import json
import yaml

class YamlIndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

def _yaml_str_presenter(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.add_representer(str, _yaml_str_presenter, Dumper=YamlIndentDumper)

@dataclass
class PersonalInfo:
    name: str = ""
    title: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""
    portfolio: str = ""
    driver_license: str = ""
    photo: str = ""

@dataclass
class ExperienceItem:
    role: str = ""
    company: str = ""
    location: str = ""
    period: str = ""
    description: List[str] = field(default_factory=list)

@dataclass
class StartupItem:
    name: str = ""
    role: str = ""
    period: str = ""
    description: List[str] = field(default_factory=list)
    tech_stack: List[str] = field(default_factory=list)

@dataclass
class EducationItem:
    degree: str = ""
    institution: str = ""
    location: str = ""
    period: str = ""
    details: str = ""

@dataclass
class ProjectItem:
    name: str = ""
    url: str = ""
    tech_stack: List[str] = field(default_factory=list)
    description: str = ""
    highlights: List[str] = field(default_factory=list)

@dataclass
class LanguageItem:
    language: str = ""
    level: str = ""

@dataclass
class CVData:
    personal_info: PersonalInfo = field(default_factory=PersonalInfo)
    summary: str = ""
    skills_technical: List[str] = field(default_factory=list)
    skills_soft: List[str] = field(default_factory=list)
    skills_categorized: Dict[str, List[str]] = field(default_factory=dict)
    experience: List[ExperienceItem] = field(default_factory=list)
    startups: List[StartupItem] = field(default_factory=list)
    education: List[EducationItem] = field(default_factory=list)
    projects: List[ProjectItem] = field(default_factory=list)
    languages: List[LanguageItem] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    clause: str = ""
    template: str = "modern"
    theme_primary: str = "#1a365d"
    theme_accent: str = "#2b6cb0"

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def to_yaml(self) -> str:
        return yaml.dump(self.to_dict(), Dumper=YamlIndentDumper, allow_unicode=True, sort_keys=False)

    @classmethod
    def from_dict(cls, data: dict) -> "CVData":
        personal_info = PersonalInfo(**data.get("personal_info", {}))
        
        experience = [
            ExperienceItem(**item) for item in data.get("experience", [])
        ]
        startups = [
            StartupItem(**item) for item in data.get("startups", [])
        ]
        education = [
            EducationItem(**item) for item in data.get("education", [])
        ]
        projects = [
            ProjectItem(**item) for item in data.get("projects", [])
        ]
        languages = [
            LanguageItem(**item) for item in data.get("languages", [])
        ]

        return cls(
            personal_info=personal_info,
            summary=data.get("summary", ""),
            skills_technical=data.get("skills_technical", []),
            skills_soft=data.get("skills_soft", []),
            skills_categorized=data.get("skills_categorized", {}),
            experience=experience,
            startups=startups,
            education=education,
            projects=projects,
            languages=languages,
            certifications=data.get("certifications", []),
            clause=data.get("clause", ""),
            template=data.get("template", "modern"),
            theme_primary=data.get("theme_primary", "#1a365d"),
            theme_accent=data.get("theme_accent", "#2b6cb0"),
        )

    @classmethod
    def from_yaml(cls, yaml_content: str) -> "CVData":
        data = yaml.safe_load(yaml_content) or {}
        return cls.from_dict(data)

    @classmethod
    def from_json(cls, json_content: str) -> "CVData":
        data = json.loads(json_content) or {}
        return cls.from_dict(data)
