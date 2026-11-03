import sys
sys.stdout.reconfigure(encoding='utf-8')
from main import load_profile_file
from core.templates import get_template, list_templates

data = load_profile_file("cv_profile.yaml", "cv_data.json")

print(f"Loaded data for: {data.personal_info.name}")
print(f"Driver license: '{data.personal_info.driver_license}'")
print(f"Soft skills count: {len(data.skills_soft)}")
print(f"Active template in profile: {data.template}")

all_templates = list_templates()
print(f"\nTesting all {len(all_templates)} templates...")

for t_name in all_templates:
    try:
        cls = get_template(t_name)
        tmpl = cls(data)
        out_path = f"output/test_{t_name}.html"
        tmpl.build(out_path)
        with open(out_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Check order
        idx_lang = -1
        idx_skill = -1
        for kw in ["JĘZYKI", "Języki", "languages", "LANGUAGES"]:
            p = html.find(kw)
            if p != -1 and (idx_lang == -1 or p < idx_lang):
                idx_lang = p
        for kw in ["UMIEJĘTNOŚCI", "Umiejętności", "Technologie i Umiejętności", "skills", "SKILLS"]:
            p = html.find(kw)
            if p != -1 and (idx_skill == -1 or p < idx_skill):
                idx_skill = p

        order_ok = (idx_lang < idx_skill) if (idx_lang != -1 and idx_skill != -1) else True
        status = "[OK] (Języki -> Umiejętności)" if order_ok else "[WARN] Order inverted"
        print(f"  {t_name:12}: BUILD SUCCESS, {status}")
    except Exception as e:
        print(f"  {t_name:12}: FAILED -> {e}")
