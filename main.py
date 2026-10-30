"""
Główny program CLI i punkt wejścia do ekstrakcji oraz generowania CV.

Dostępne polecenia:
    python main.py          - Ekstrakcja z folderu source_cvs/ i wygenerowanie nowego CV
    python main.py ui       - Uruchomienie panelu Web UI (http://127.0.0.1:8000)
    python main.py extract  - Tylko ekstrakcja ze starych plików do cv_profile.yaml i cv_data.json
    python main.py build    - Przebudowanie plików w output/ na podstawie cv_profile.yaml
"""
import sys
import os
import json
import argparse
from typing import List

# Fix Windows console encoding for Polish characters & emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.models import CVData
from core.reader import DocumentReader
from core.parser import CVParser
from core.merger import CVMerger
from core.docx_builder import DocxCVBuilder
from core.html_builder import HtmlCVBuilder

SOURCE_DIR_DEFAULT = "source_cvs"
OUTPUT_DIR_DEFAULT = "output"
YAML_DEFAULT = "cv_profile.yaml"
JSON_DEFAULT = "cv_data.json"
DOCX_DEFAULT = os.path.join(OUTPUT_DIR_DEFAULT, "nowe_cv.docx")
HTML_DEFAULT = os.path.join(OUTPUT_DIR_DEFAULT, "nowe_cv.html")

def print_banner():
    print("=" * 65)
    print("      🚀 CV EXTRACTOR & GENERATOR (PDF & Word -> Nowe CV)      ")
    print("=" * 65)

def extract_and_merge(files: List[str]) -> CVData:
    print(f"\n📂 Znaleziono pliki do analizy ({len(files)}):")
    cv_list = []
    for f in files:
        print(f"  🔍 Ekstrakcja danych z: {os.path.basename(f)} ...", end=" ", flush=True)
        try:
            lines = DocumentReader.read_file(f)
            cv = CVParser.parse(lines)
            cv_list.append(cv)
            print(f"✅ OK ({len(lines)} linii tekstu)")
        except Exception as e:
            print(f"❌ Błąd: {e}")

    if not cv_list:
        print("❌ Nie udało się przetworzyć żadnego pliku.")
        sys.exit(1)

    print("\n🔄 Scalanie i deduplikacja danych ze wszystkich plików...", end=" ", flush=True)
    merged = CVMerger.merge(cv_list)
    print("✅ Gotowe!")
    return merged

def print_summary(cv: CVData):
    info = cv.personal_info
    print("\n" + "-" * 65)
    print("📋 PODSUMOWANIE ZEBRANYCH DANYCH:")
    print(f"  • Imię i nazwisko:   {info.name or '(brak)'}")
    print(f"  • Tytuł zawodowy:    {info.title or '(brak)'}")
    print(f"  • Kontakt:           {info.email or '-'} | {info.phone or '-'} | {info.location or '-'}")
    print(f"  • LinkedIn:          {info.linkedin or '(brak)'}")
    print(f"  • GitHub:            {info.github or '(brak)'}")
    print(f"  • Prawo jazdy:       {info.driver_license or '(brak)'}")
    print(f"  • Doświadczenie:     {len(cv.experience)} pozycji")
    for exp in cv.experience:
        print(f"      - {exp.period}: {exp.role} ({exp.company})")
    print(f"  • Start-up / Inicj.: {len(cv.startups)} pozycji")
    for st in cv.startups:
        print(f"      - {st.name} ({len(st.description)} punktów opisu)")
    print(f"  • Wykształcenie:     {len(cv.education)} wpisów")
    for edu in cv.education:
        print(f"      - {edu.period}: {edu.degree} ({edu.institution})")
    print(f"  • Projekty własne:   {len(cv.projects)} projektów")
    for pr in cv.projects:
        print(f"      - {pr.name} [{', '.join(pr.tech_stack[:4])}...]")
    print(f"  • Umiejętności:      {len(cv.skills_technical)} tech, {len(cv.skills_soft)} miękkich")
    print(f"  • Języki obce:       {', '.join(f'{l.language} ({l.level})' for l in cv.languages)}")
    print("-" * 65)

def save_profile_files(cv: CVData, yaml_path: str = YAML_DEFAULT, json_path: str = JSON_DEFAULT):
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(cv.to_yaml())
    print(f"💾 Zapisano profil AI-friendly (YAML): {yaml_path}")

    with open(json_path, "w", encoding="utf-8") as f:
        f.write(cv.to_json(indent=2))
    print(f"💾 Zapisano bazę danych (JSON):         {json_path}")

def load_profile_file(yaml_path: str = YAML_DEFAULT, json_path: str = JSON_DEFAULT) -> CVData:
    if os.path.isfile(yaml_path):
        print(f"\n📖 Wczytywanie profilu z pliku YAML: {yaml_path} ...")
        with open(yaml_path, "r", encoding="utf-8") as f:
            return CVData.from_yaml(f.read())
    elif os.path.isfile(json_path):
        print(f"\n📖 Wczytywanie profilu z pliku JSON: {json_path} ...")
        with open(json_path, "r", encoding="utf-8") as f:
            return CVData.from_json(f.read())
    else:
        print(f"❌ Nie znaleziono ani pliku {yaml_path}, ani {json_path}!")
        sys.exit(1)

def generate_documents(cv: CVData, docx_path: str = DOCX_DEFAULT, html_path: str = HTML_DEFAULT):
    os.makedirs(os.path.dirname(os.path.abspath(docx_path)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(html_path)), exist_ok=True)

    print("\n📄 Generowanie nowoczesnego CV w formatach DOCX i HTML...")
    
    # 1. DOCX
    docx_builder = DocxCVBuilder(cv)
    docx_out = docx_builder.build(docx_path)
    print(f"  ✨ Wygenerowano plik Word: {docx_out}")

    # 2. HTML (z możliwością druku do PDF)
    html_builder = HtmlCVBuilder(cv)
    html_out = html_builder.build(html_path)
    print(f"  ✨ Wygenerowano plik HTML (Druk do PDF): {html_out}")

def main():
    parser = argparse.ArgumentParser(
        description="Program do ekstrakcji danych z PDF/Word i tworzenia nowego CV na ich podstawie."
    )
    parser.add_argument("command", nargs="?", default="run", 
                        choices=["run", "extract", "build", "ui", "web"], 
                        help="Akcja: run (ekstrakt + generowanie), ui (panel graficzny w przeglądarce), extract (tylko yaml/json), build (generowanie z yaml/json)")
    parser.add_argument("files", nargs="*", help="Opcjonalna lista plików CV do przetworzenia (.pdf, .docx)")
    parser.add_argument("--source-dir", default=SOURCE_DIR_DEFAULT, help="Katalog ze starymi plikami CV (domyślnie: source_cvs)")
    parser.add_argument("--yaml", default=YAML_DEFAULT, help="Ścieżka do pliku YAML (domyślnie: cv_profile.yaml)")
    parser.add_argument("--json", default=JSON_DEFAULT, help="Ścieżka do pliku JSON (domyślnie: cv_data.json)")
    parser.add_argument("--docx-out", default=DOCX_DEFAULT, help="Nazwa wyjściowego pliku Word (domyślnie: output/nowe_cv.docx)")
    parser.add_argument("--html-out", default=HTML_DEFAULT, help="Nazwa wyjściowego pliku HTML (domyślnie: output/nowe_cv.html)")

    args = parser.parse_args()

    cmd = args.command

    # UI Command
    if cmd in ("ui", "web"):
        from web.server import run_server
        print_banner()
        run_server(host="127.0.0.1", port=8000, open_browser=True)
        return

    print_banner()

    target_files = args.files
    if not target_files and cmd != "build":
        target_files = DocumentReader.discover_files(args.source_dir)
        if not target_files:
            print(f"❌ Nie znaleziono żadnych plików .pdf ani .docx w katalogu '{args.source_dir}' ani w katalogu głównym.")
            print(f"   Umieść stare pliki CV w folderze '{args.source_dir}' lub podaj ich ścieżki.")
            sys.exit(1)

    if cmd == "build":
        cv = load_profile_file(args.yaml, args.json)
        print_summary(cv)
        generate_documents(cv, args.docx_out, args.html_out)
        print("\n🎉 Sukces! Nowe CV zostało wygenerowane na podstawie pliku profilu.")

    elif cmd == "extract":
        cv = extract_and_merge(target_files)
        print_summary(cv)
        save_profile_files(cv, args.yaml, args.json)
        print(f"\n💡 Możesz teraz przejrzeć i dostosować dane w pliku {args.yaml} (lub poprosić AI o edycję),")
        print("   a następnie uruchomić: python main.py build")
        print("   lub uruchomić panel graficzny: python app.py")

    elif cmd == "run":
        cv = extract_and_merge(target_files)
        print_summary(cv)
        save_profile_files(cv, args.yaml, args.json)
        generate_documents(cv, args.docx_out, args.html_out)
        print("\n" + "=" * 65)
        print("🎉 GOTOWE! Nowe CV zostało wygenerowane na podstawie starych plików!")
        print(f"   1. Folder źródłowy:          {args.source_dir}/  (Twoje stare pliki CV)")
        print(f"   2. Format dla AI / Edycji:   {args.yaml}  (czytelny YAML do edycji przez Ciebie lub prompt AI)")
        print(f"   3. Pliki wyjściowe:          {args.docx_out}")
        print(f"                                {args.html_out}  (otwórz w przeglądarce i naciśnij Ctrl+P)")
        print("   4. Panel graficzny (UI):      uruchom wpisując: python app.py")
        print("=" * 65)

if __name__ == "__main__":
    main()
