"""
Parser module to turn extracted document lines into structured CVData.
Supports Polish and English CV headers and formats.
"""
import re
from typing import List, Dict, Tuple, Optional
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

# Regex patterns for detecting section headers
SECTION_PATTERNS = [
    ('contact', re.compile(r'^(?:◆\s*|■\s*|•\s*|#+\s*)?(?:kontakt|dane\s+kontaktowe|dane\s+osobowe|contact\s+info|contact)\b', re.IGNORECASE)),
    ('languages', re.compile(r'^(?:◆\s*|■\s*|•\s*|#+\s*)?(?:języki|jezyki|języki\s+obce|znajomość\s+języków|languages)\b', re.IGNORECASE)),
    ('skills', re.compile(r'^(?:◆\s*|■\s*|•\s*|#+\s*)?(?:umiejętności|umiejetnosci|kwalifikacje|technologie|skills|tech\s+stack)\b', re.IGNORECASE)),
    ('summary', re.compile(r'^(?:◆\s*|■\s*|•\s*|#+\s*)?(?:o\s+mnie|podsumowanie|profil\s+zawodowy|o\s+sobie|about\s+me|summary|profile)\b', re.IGNORECASE)),
    ('experience', re.compile(r'^(?:◆\s*|■\s*|•\s*|#+\s*)?(?:doświadczenie\s+zawodowe|doswiadczenie\s+zawodowe|doświadczenie|historia\s+zatrudnienia|praktyki|experience|work\s+experience)\b', re.IGNORECASE)),
    ('startups', re.compile(r'^(?:◆\s*|■\s*|•\s*|#+\s*)?(?:start-up|startup|własna\s+działalność|własne\s+inicjatywy|przedsięwzięcia|startups)\b', re.IGNORECASE)),
    ('education', re.compile(r'^(?:◆\s*|■\s*|•\s*|#+\s*)?(?:wykształcenie|wyksztalcenie|edukacja|studia|education)\b', re.IGNORECASE)),
    ('projects', re.compile(r'^(?:◆\s*|■\s*|•\s*|#+\s*)?(?:projekty|portfolio|wybrane\s+projekty|projects)\b', re.IGNORECASE)),
    ('certifications', re.compile(r'^(?:◆\s*|■\s*|•\s*|#+\s*)?(?:certyfikaty|kursy|szkolenia|certifications|courses)\b', re.IGNORECASE)),
    ('clause', re.compile(r'^(?:◆\s*|■\s*|•\s*|#+\s*)?(?:klauzula|wyrażam\s+zgodę|zgoda\s+na\s+przetwarzanie|rodo|gdpr)\b', re.IGNORECASE)),
]

DATE_RANGE_RE = re.compile(
    r'(\d{2}\.\d{4}|\d{4})\s*[-–—]\s*(\d{2}\.\d{4}|\d{4}|obecnie|teraz|present|now)', 
    re.IGNORECASE
)

EMAIL_RE = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
PHONE_RE = re.compile(r'(?:(?:\+|00)\d{1,3}[\s-]*)?(?:\d{3}[\s-]?\d{3}[\s-]?\d{3}|\d{2}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2})')
LINKEDIN_RE = re.compile(r'(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+', re.IGNORECASE)
GITHUB_RE = re.compile(r'(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+', re.IGNORECASE)

SOFT_SKILL_STEMS = [
    'organi', 'motywac', 'uczen', 'nauk', 'odpowiedzialn', 'problem', 
    'czas', 'zesp', 'komunikac', 'kreatyw', 'elastycz', 'samodziel', 
    'analitycz', 'dokładn', 'zaangaż', 'zarządzan', 'relacj', 'inicjatyw'
]

TECH_CATEGORIES = {
    "Frontend": ["react", "vite", "next", "vue", "angular", "html", "css", "tailwind", "javascript", "typescript", "sass", "redux"],
    "Backend": ["python", "django", "fastapi", "flask", "pytorch", "node", "express", "php", "java", "c++", "c#", ".net", "spring", "golang"],
    "Bazy danych": ["sql", "postgresql", "postgres", "mongodb", "mysql", "redis", "sqlite", "oracle", "mariadb"],
    "DevOps & Narzędzia": ["docker", "git", "github", "gitlab", "vs code", "linux", "windows", "bash", "ci/cd", "kubernetes", "aws", "gcp", "azure"]
}

class CVParser:
    @classmethod
    def parse(cls, lines: List[str]) -> CVData:
        # Step 1: Divide lines into designated sections
        sections = cls._segment_sections(lines)

        # Step 2: Parse individual sections
        personal_info = cls._parse_personal_info(sections.get('header', []), sections.get('contact', []), sections.get('summary', []))
        summary = cls._parse_summary(sections.get('summary', []))
        languages = cls._parse_languages(sections.get('languages', []))
        tech_skills, soft_skills, categorized_skills = cls._parse_skills(sections.get('skills', []))
        experience = cls._parse_experience(sections.get('experience', []))
        startups = cls._parse_startups(sections.get('startups', []))
        education = cls._parse_education(sections.get('education', []))
        projects = cls._parse_projects(sections.get('projects', []))
        certifications = cls._parse_certifications(sections.get('certifications', []))
        clause = cls._parse_clause(sections.get('clause', []))

        # Check if title was extracted; if not, look in summary or header
        if not personal_info.title:
            personal_info.title = cls._extract_title(summary, sections.get('header', []))

        return CVData(
            personal_info=personal_info,
            summary=summary,
            skills_technical=tech_skills,
            skills_soft=soft_skills,
            skills_categorized=categorized_skills,
            experience=experience,
            startups=startups,
            education=education,
            projects=projects,
            languages=languages,
            certifications=certifications,
            clause=clause
        )

    @classmethod
    def _segment_sections(cls, lines: List[str]) -> Dict[str, List[str]]:
        sections: Dict[str, List[str]] = {'header': []}
        current_section = 'header'

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            matched_sec = None
            for sec_name, pattern in SECTION_PATTERNS:
                if pattern.search(line):
                    matched_sec = sec_name
                    break

            if matched_sec:
                current_section = matched_sec
                if current_section not in sections:
                    sections[current_section] = []
            else:
                sections[current_section].append(line)

        return sections

    @classmethod
    def _parse_personal_info(cls, header_lines: List[str], contact_lines: List[str], summary_lines: List[str]) -> PersonalInfo:
        info = PersonalInfo()

        # Name extraction: usually first 1-2 non-empty lines in header
        candidate_name_parts = []
        for line in header_lines[:3]:
            # If line contains email, phone, or symbols, skip
            if EMAIL_RE.search(line) or PHONE_RE.search(line) or '◆' in line or '@' in line:
                continue
            words = line.split()
            if len(words) in (1, 2, 3) and all(w[0].isupper() for w in words if w.isalpha()):
                candidate_name_parts.append(line)
                if len(candidate_name_parts) >= 2:
                    break

        if candidate_name_parts:
            info.name = " ".join(candidate_name_parts)

        # Contact lines parsing
        full_contact_text = "\n".join(contact_lines + header_lines)

        # Email
        email_match = EMAIL_RE.search(full_contact_text)
        if email_match:
            info.email = email_match.group(0).strip()

        # Phone
        phone_match = PHONE_RE.search(full_contact_text)
        if phone_match:
            info.phone = phone_match.group(0).strip()

        # LinkedIn
        li_match = LINKEDIN_RE.search(full_contact_text)
        if li_match:
            li_url = li_match.group(0).strip()
            if not li_url.startswith("http"):
                li_url = "https://" + li_url
            info.linkedin = li_url

        # GitHub
        gh_match = GITHUB_RE.search(full_contact_text)
        if gh_match:
            gh_url = gh_match.group(0).strip()
            if not gh_url.startswith("http"):
                gh_url = "https://" + gh_url
            info.github = gh_url

        # Location & Driver License from lines
        for i, line in enumerate(contact_lines):
            lower = line.lower()
            if lower in ('adres', 'lokalizacja', 'miasto', 'miejscowość', 'address', 'location') and i + 1 < len(contact_lines):
                info.location = contact_lines[i + 1].strip()
            elif 'adres:' in lower or 'lokalizacja:' in lower:
                info.location = line.split(':', 1)[1].strip()

            if lower in ('pozwolenie', 'prawo jazdy', 'prawo jazdy kat.', 'driving license') and i + 1 < len(contact_lines):
                info.driver_license = contact_lines[i + 1].strip()
            elif 'pozwolenie:' in lower or 'prawo jazdy:' in lower:
                info.driver_license = line.split(':', 1)[1].strip()

        return info

    @classmethod
    def _extract_title(cls, summary: str, header_lines: List[str]) -> str:
        # Check standard engineering titles
        titles = [
            "Full Stack Software Engineer", "Full Stack Developer", "Software Engineer",
            "Python Developer", "Frontend Developer", "Backend Developer", "DevOps Engineer",
            "Inżynier Informatyki", "Programista Python", "Programista"
        ]
        for t in titles:
            if re.search(r'\b' + re.escape(t) + r'\b', summary, re.IGNORECASE):
                return t
        for l in header_lines:
            for t in titles:
                if re.search(r'\b' + re.escape(t) + r'\b', l, re.IGNORECASE):
                    return t
        return "Software Engineer"

    @classmethod
    def _parse_summary(cls, summary_lines: List[str]) -> str:
        if not summary_lines:
            return ""
        # Join wrapped lines nicely into paragraphs
        paragraphs = []
        curr_p = []
        for l in summary_lines:
            curr_p.append(l)
            if l.endswith('.'):
                paragraphs.append(" ".join(curr_p))
                curr_p = []
        if curr_p:
            paragraphs.append(" ".join(curr_p))
        return "\n\n".join(paragraphs)

    @classmethod
    def _parse_languages(cls, lang_lines: List[str]) -> List[LanguageItem]:
        # Unwrap continuation lines (e.g. 'Angielski - Wyższy średnio' + 'zaawansowany (B2)')
        unwrapped = []
        for l in lang_lines:
            if unwrapped and (l[0].islower() or l.startswith('(')):
                unwrapped[-1] += ' ' + l
            else:
                unwrapped.append(l)

        items: List[LanguageItem] = []
        for l in unwrapped:
            # Match formats: "Polski: Ojczysty", "Angielski - B2", "English (Fluent)"
            if ':' in l:
                parts = l.split(':', 1)
                items.append(LanguageItem(language=parts[0].strip(), level=parts[1].strip()))
            elif '-' in l or '–' in l:
                sep = '-' if '-' in l else '–'
                parts = l.split(sep, 1)
                items.append(LanguageItem(language=parts[0].strip(), level=parts[1].strip()))
            elif '(' in l and l.endswith(')'):
                match = re.match(r'^(.*?)\s*\((.*?)\)$', l)
                if match:
                    items.append(LanguageItem(language=match.group(1).strip(), level=match.group(2).strip()))
            else:
                items.append(LanguageItem(language=l.strip(), level=""))
        return items

    @classmethod
    def _parse_skills(cls, skill_lines: List[str]) -> Tuple[List[str], List[str], Dict[str, List[str]]]:
        # Unwrap continuation lines (e.g. trailing comma)
        unwrapped = []
        for l in skill_lines:
            if unwrapped and (unwrapped[-1].endswith(',') or (l[0].islower() and not unwrapped[-1].endswith('.'))):
                unwrapped[-1] += ' ' + l
            else:
                unwrapped.append(l)

        tech_skills: List[str] = []
        soft_skills: List[str] = []

        for line in unwrapped:
            lower = line.lower()
            if any(stem in lower for stem in SOFT_SKILL_STEMS):
                soft_skills.append(line)
            else:
                tech_skills.append(line)

        # Categorize technical skills
        categorized: Dict[str, List[str]] = {
            "Frontend": [],
            "Backend": [],
            "Bazy danych": [],
            "Narzędzia & DevOps": []
        }

        all_tech_tokens = []
        for line in tech_skills:
            # Tokenize comma separated items outside parentheses
            tokens = [t.strip() for t in re.split(r',\s*(?![^()]*\))', line) if t.strip()]
            for token in tokens:
                all_tech_tokens.append(token)

        for token in all_tech_tokens:
            t_lower = token.lower()
            placed = False
            for cat_name, keywords in TECH_CATEGORIES.items():
                cat_key = "Narzędzia & DevOps" if "DevOps" in cat_name else cat_name
                if any(kw in t_lower for kw in keywords):
                    if token not in categorized[cat_key]:
                        categorized[cat_key].append(token)
                    placed = True
                    break

        # Remove empty categories
        categorized = {k: v for k, v in categorized.items() if v}

        return tech_skills, soft_skills, categorized

    @classmethod
    def _parse_experience(cls, exp_lines: List[str]) -> List[ExperienceItem]:
        # 1. Unwrap broken dates
        unwrapped_dates = []
        i = 0
        while i < len(exp_lines):
            l = exp_lines[i]
            if i + 1 < len(exp_lines) and re.search(r'\d{2}\.\d{4}\s*[-–]$', l):
                l = l + ' ' + exp_lines[i+1]
                i += 1
            unwrapped_dates.append(l)
            i += 1

        # 2. Unwrap bullet lines continuation
        unwrapped = []
        for l in unwrapped_dates:
            if unwrapped and not l.startswith(('•', '-', '*')) and (l[0].islower() and not unwrapped[-1].endswith('.')):
                unwrapped[-1] += ' ' + l
            else:
                unwrapped.append(l)

        items: List[ExperienceItem] = []
        curr = None

        for l in unwrapped:
            m = DATE_RANGE_RE.search(l)
            if m:
                if curr:
                    items.append(curr)
                curr = {'period': m.group(0), 'headers': [], 'bullets': []}
            elif curr:
                if l.startswith(('•', '-', '*')):
                    curr['bullets'].append(re.sub(r'^[•\-\*]\s*', '', l))
                else:
                    curr['headers'].append(l)

        if curr:
            items.append(curr)

        parsed_items: List[ExperienceItem] = []
        for raw_item in items:
            headers = raw_item['headers']
            role = ""
            company = ""
            location = ""

            if len(headers) == 1:
                role = headers[0]
            elif len(headers) >= 2:
                # Typically line 0 is role, line 1 is company & location
                role = headers[0]
                company_line = headers[-1]
                if ',' in company_line:
                    c_parts = company_line.split(',', 1)
                    company = c_parts[0].strip()
                    location = c_parts[1].strip()
                else:
                    company = company_line

            parsed_items.append(ExperienceItem(
                role=role,
                company=company,
                location=location,
                period=raw_item['period'],
                description=raw_item['bullets']
            ))

        return parsed_items

    @classmethod
    def _parse_startups(cls, startup_lines: List[str]) -> List[StartupItem]:
        # Unwrap bullets continuation
        unwrapped = []
        for l in startup_lines:
            if unwrapped and not l.startswith(('•', '-', '*')) and (l[0].islower() and not unwrapped[-1].endswith('.')):
                unwrapped[-1] += ' ' + l
            else:
                unwrapped.append(l)

        items: List[StartupItem] = []
        curr = None

        for l in unwrapped:
            if l.startswith(('•', '-', '*')):
                bullet = re.sub(r'^[•\-\*]\s*', '', l)
                if curr:
                    curr.description.append(bullet)
            else:
                if curr:
                    items.append(curr)
                curr = StartupItem(name=l.strip())

        if curr:
            items.append(curr)

        return items

    @classmethod
    def _parse_education(cls, edu_lines: List[str]) -> List[EducationItem]:
        # Unwrap broken dates
        unwrapped_dates = []
        i = 0
        while i < len(edu_lines):
            l = edu_lines[i]
            if i + 1 < len(edu_lines) and re.search(r'\d{2}\.\d{4}\s*[-–]$', l):
                l = l + ' ' + edu_lines[i+1]
                i += 1
            unwrapped_dates.append(l)
            i += 1

        unwrapped = []
        for l in unwrapped_dates:
            if unwrapped and not l.startswith(('•', '-', '*')) and (l[0].islower() and not unwrapped[-1].endswith('.')):
                unwrapped[-1] += ' ' + l
            else:
                unwrapped.append(l)

        raw_items = []
        curr = None

        for l in unwrapped:
            m = DATE_RANGE_RE.search(l)
            if m:
                if curr:
                    raw_items.append(curr)
                curr = {'period': m.group(0), 'lines': []}
            elif curr:
                curr['lines'].append(l)

        if curr:
            raw_items.append(curr)

        edu_items: List[EducationItem] = []
        for it in raw_items:
            lines = it['lines']
            degree = ""
            institution = ""
            location = ""
            if len(lines) == 1:
                degree = lines[0]
            elif len(lines) >= 2:
                degree = lines[0]
                inst_line = lines[-1]
                if '-' in inst_line:
                    parts = inst_line.split('-', 1)
                    institution = parts[0].strip()
                    location = parts[1].strip()
                else:
                    institution = inst_line

            edu_items.append(EducationItem(
                degree=degree,
                institution=institution,
                location=location,
                period=it['period']
            ))

        return edu_items

    @classmethod
    def _parse_projects(cls, proj_lines: List[str]) -> List[ProjectItem]:
        projects: List[ProjectItem] = []
        curr_proj: Optional[ProjectItem] = None

        for l in proj_lines:
            if l.startswith('•') or l.startswith('■'):
                if curr_proj:
                    projects.append(curr_proj)
                header = re.sub(r'^[•■\-\*]\s*', '', l)
                parts = [p.strip() for p in header.split(',') if p.strip()]
                name = parts[0]
                url = parts[1] if len(parts) > 1 else ""
                curr_proj = ProjectItem(name=name, url=url)
            elif curr_proj:
                # Check if line looks like a tech stack (comma separated short words)
                if not curr_proj.tech_stack and (',' in l and len(l.split()) < 12 and not l.endswith('.')):
                    curr_proj.tech_stack = [t.strip() for t in l.split(',') if t.strip()]
                else:
                    if curr_proj.description:
                        curr_proj.description += " " + l
                    else:
                        curr_proj.description = l

        if curr_proj:
            projects.append(curr_proj)

        return projects

    @classmethod
    def _parse_certifications(cls, cert_lines: List[str]) -> List[str]:
        return [re.sub(r'^[•■\-\*]\s*', '', l) for l in cert_lines if l.strip()]

    @classmethod
    def _parse_clause(cls, clause_lines: List[str]) -> str:
        if not clause_lines:
            return (
                "Wyrażam zgodę na przetwarzanie moich danych osobowych dla potrzeb niezbędnych do "
                "realizacji procesu rekrutacji (zgodnie z ustawą z dnia 10 maja 2018 roku o ochronie "
                "danych osobowych (Dz. Ustaw z 2018, poz. 1000) oraz zgodnie z Rozporządzeniem Parlamentu "
                "Europejskiego i Rady (UE) 2016/679 z dnia 27 kwietnia 2016 r. w sprawie ochrony osób fizycznych "
                "w związku z przetwarzaniem danych osobowych i w sprawie swobodnego przepływu takich danych "
                "oraz uchylenia dyrektywy 95/46/WE (RODO))."
            )
        return " ".join(clause_lines)
