"""
Główny program CLI do ekstrakcji danych z CV (PDF / Word DOCX)
oraz generowania nowego, nowoczesnego CV na podstawie starych plików.

Użycie:
    python main.py                     - Automatyczne skanowanie katalogu, scalenie i wygenerowanie nowego CV (.docx i .html)
    python main.py extract             - Tylko ekstrakcja i zapis do cv_data.json
    python main.py build               - Wygenerowanie nowego CV z pliku cv_data.json
    python main.py plik1.pdf plik2.docx - Ekstrakcja ze wskazanych plików
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

from models import CVData
from reader import DocumentReader
from parser import CVParser
from merger import CVMerger
from docx_builder import DocxCVBuilder
from html_builder import HtmlCVBuilder

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

def save_json(cv: CVData, path: str = "cv_data.json"):
    with open(path, "w", encoding="utf-8") as f:
        f.write(cv.to_json(indent=2))
    print(f"💾 Zapisano ustrukturyzowane dane do: {path}")

def load_json(path: str = "cv_data.json") -> CVData:
    if not os.path.isfile(path):
        print(f"❌ Plik {path} nie istnieje!")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return CVData.from_dict(data)

def generate_documents(cv: CVData, docx_path: str = "nowe_cv.docx", html_path: str = "nowe_cv.html"):
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
                        choices=["run", "extract", "build"], 
                        help="Akcja do wykonania: run (domyślnie: ekstrakt + budowa), extract (tylko json), build (budowa z json)")
    parser.add_argument("files", nargs="*", help="Opcjonalna lista plików CV do przetworzenia (.pdf, .docx)")
    parser.add_argument("--json", default="cv_data.json", help="Ścieżka do pliku JSON (domyślnie: cv_data.json)")
    parser.add_argument("--docx-out", default="nowe_cv.docx", help="Nazwa wyjściowego pliku Word (domyślnie: nowe_cv.docx)")
    parser.add_argument("--html-out", default="nowe_cv.html", help="Nazwa wyjściowego pliku HTML (domyślnie: nowe_cv.html)")

    args = parser.parse_args()

    print_banner()

    cmd = args.command

    # If user provided file paths directly as arguments
    target_files = args.files
    if not target_files and cmd != "build":
        target_files = DocumentReader.discover_files(".")
        if not target_files:
            print("❌ Nie znaleziono żadnych plików .pdf ani .docx w bieżącym katalogu.")
            print("   Umieść stare pliki CV w tym katalogu lub podaj ich ścieżki.")
            sys.exit(1)

    if cmd == "build":
        print(f"\n📖 Wczytywanie danych z pliku: {args.json} ...")
        cv = load_json(args.json)
        print_summary(cv)
        generate_documents(cv, args.docx_out, args.html_out)
        print("\n🎉 Sukces! Nowe CV zostało wygenerowane.")

    elif cmd == "extract":
        cv = extract_and_merge(target_files)
        print_summary(cv)
        save_json(cv, args.json)
        print(f"\n💡 Możesz teraz przejrzeć i dostosować dane w pliku {args.json},")
        print("   a następnie uruchomić: python main.py build")

    elif cmd == "run":
        # Full end-to-end pipeline
        cv = extract_and_merge(target_files)
        print_summary(cv)
        save_json(cv, args.json)
        generate_documents(cv, args.docx_out, args.html_out)
        print("\n" + "=" * 65)
        print("🎉 GOTOWE! Nowe CV zostało wygenerowane na podstawie starych plików!")
        print(f"   1. Plik Word (.docx):   {args.docx_out}  (gotowy do edycji i wysyłki)")
        print(f"   2. Plik HTML / PDF:     {args.html_out}  (otwórz w przeglądarce i naciśnij Ctrl+P)")
        print(f"   3. Baza danych JSON:    {args.json}      (Twoje dane w czystym formacie)")
        print("=" * 65)

if __name__ == "__main__":
    main()

