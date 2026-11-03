import sys

for fname in ['classic.py', 'modern.py', 'elegant.py']:
    fpath = f'core/templates/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    norm_content = content.replace('\r\n', '\n')
    target = """        {projects_html}
        {skills_html}
        {education_html}
        {languages_html}"""

    replacement = """        {projects_html}
        {education_html}
        {languages_html}
        {skills_html}"""

    if target in norm_content:
        norm_content = norm_content.replace(target, replacement)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(norm_content)
        print(f"Updated {fname}")
    else:
        print(f"Target not found in {fname}")
