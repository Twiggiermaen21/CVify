"""
Merger module to consolidate CV data from multiple extracted CVs into one complete profile.
Deduplicates entries, fills missing fields, and combines skills and projects.
"""
from typing import List, Dict
import re
try:
    from .models import (
        CVData, PersonalInfo, ExperienceItem, StartupItem, 
        EducationItem, ProjectItem, LanguageItem
    )
except ImportError:
    from models import (
        CVData, PersonalInfo, ExperienceItem, StartupItem, 
        EducationItem, ProjectItem, LanguageItem
    )

class CVMerger:
    @classmethod
    def merge(cls, cvs: List[CVData]) -> CVData:
        if not cvs:
            return CVData()
        if len(cvs) == 1:
            return cvs[0]

        merged = CVData()

        # 1. Personal Info
        merged.personal_info = cls._merge_personal_info([c.personal_info for c in cvs])

        # 2. Summary (pick the longest / most comprehensive)
        summaries = [c.summary.strip() for c in cvs if c.summary.strip()]
        merged.summary = max(summaries, key=len) if summaries else ""

        # 3. Experience (deduplicate by role + company)
        merged.experience = cls._merge_experience(cvs)

        # 4. Startups (deduplicate by name)
        merged.startups = cls._merge_startups(cvs)

        # 5. Education (deduplicate by institution + degree)
        merged.education = cls._merge_education(cvs)

        # 6. Projects (deduplicate by name)
        merged.projects = cls._merge_projects(cvs)

        # 7. Skills (union preserving order)
        merged.skills_technical = cls._merge_string_lists([c.skills_technical for c in cvs])
        merged.skills_soft = cls._merge_string_lists([c.skills_soft for c in cvs])

        # Merge categorized skills
        merged.skills_categorized = cls._merge_categorized_skills([c.skills_categorized for c in cvs])

        # 8. Languages (deduplicate by language)
        merged.languages = cls._merge_languages(cvs)

        # 9. Certifications
        merged.certifications = cls._merge_string_lists([c.certifications for c in cvs])

        # 10. Clause
        clauses = [c.clause.strip() for c in cvs if c.clause.strip()]
        merged.clause = max(clauses, key=len) if clauses else ""

        return merged

    @classmethod
    def _merge_personal_info(cls, infos: List[PersonalInfo]) -> PersonalInfo:
        target = PersonalInfo()
        for info in infos:
            if not target.name and info.name:
                target.name = info.name
            if not target.title and info.title:
                target.title = info.title
            if not target.email and info.email:
                target.email = info.email
            if not target.phone and info.phone:
                target.phone = info.phone
            if not target.location and info.location:
                target.location = info.location
            if not target.linkedin and info.linkedin:
                target.linkedin = info.linkedin
            if not target.github and info.github:
                target.github = info.github
            if not target.portfolio and info.portfolio:
                target.portfolio = info.portfolio
            if not target.driver_license and info.driver_license:
                target.driver_license = info.driver_license
        return target

    @classmethod
    def _merge_experience(cls, cvs: List[CVData]) -> List[ExperienceItem]:
        seen = {}
        result = []
        for cv in cvs:
            for item in cv.experience:
                key = (item.role.lower().strip(), item.company.lower().strip())
                if key not in seen:
                    seen[key] = item
                    result.append(item)
                else:
                    # Enrich descriptions if the new one has more bullet points
                    existing = seen[key]
                    if len(item.description) > len(existing.description):
                        existing.description = item.description
                    if not existing.period and item.period:
                        existing.period = item.period
                    if not existing.location and item.location:
                        existing.location = item.location
        return result

    @classmethod
    def _merge_startups(cls, cvs: List[CVData]) -> List[StartupItem]:
        seen = {}
        result = []
        for cv in cvs:
            for item in cv.startups:
                key = item.name.lower().strip()
                if key not in seen:
                    seen[key] = item
                    result.append(item)
                else:
                    existing = seen[key]
                    if len(item.description) > len(existing.description):
                        existing.description = item.description
                    if not existing.role and item.role:
                        existing.role = item.role
        return result

    @classmethod
    def _merge_education(cls, cvs: List[CVData]) -> List[EducationItem]:
        seen = {}
        result = []
        for cv in cvs:
            for item in cv.education:
                key = (item.degree.lower().strip()[:20], item.institution.lower().strip()[:20])
                if key not in seen:
                    seen[key] = item
                    result.append(item)
                else:
                    existing = seen[key]
                    if not existing.period and item.period:
                        existing.period = item.period
                    if not existing.location and item.location:
                        existing.location = item.location
        return result

    @classmethod
    def _merge_projects(cls, cvs: List[CVData]) -> List[ProjectItem]:
        seen = {}
        result = []
        for cv in cvs:
            for item in cv.projects:
                key = item.name.lower().strip()
                if key not in seen:
                    seen[key] = item
                    result.append(item)
                else:
                    existing = seen[key]
                    if not existing.url and item.url:
                        existing.url = item.url
                    if len(item.tech_stack) > len(existing.tech_stack):
                        existing.tech_stack = item.tech_stack
                    if len(item.description) > len(existing.description):
                        existing.description = item.description
        return result

    @classmethod
    def _merge_languages(cls, cvs: List[CVData]) -> List[LanguageItem]:
        seen = {}
        result = []
        for cv in cvs:
            for item in cv.languages:
                key = item.language.lower().strip()
                if key not in seen:
                    seen[key] = item
                    result.append(item)
                else:
                    existing = seen[key]
                    if not existing.level and item.level:
                        existing.level = item.level
        return result

    @classmethod
    def _merge_string_lists(cls, lists: List[List[str]]) -> List[str]:
        seen = set()
        result = []
        for l in lists:
            for item in l:
                clean = item.strip()
                key = clean.lower()
                if key and key not in seen:
                    seen.add(key)
                    result.append(clean)
        return result

    @classmethod
    def _merge_categorized_skills(cls, cat_dicts: List[Dict[str, List[str]]]) -> Dict[str, List[str]]:
        merged_cats: Dict[str, List[str]] = {}
        for d in cat_dicts:
            for cat_name, skill_list in d.items():
                if cat_name not in merged_cats:
                    merged_cats[cat_name] = []
                for s in skill_list:
                    if s not in merged_cats[cat_name]:
                        merged_cats[cat_name].append(s)
        return merged_cats

