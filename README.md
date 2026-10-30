# CV Studio & Generator (PDF & Word -> Nowe CV + Web Studio)

Kompletne, modułowe narzędzie w Pythonie do:
1. **Ekstrakcji danych ze starych CV** (PDF / Word DOCX).
2. **Scalania i deduplikacji danych** w jeden spójny profil.
3. **Wygodnej edycji** przez człowieka lub AI w formacie **`cv_profile.yaml`**.
4. **Interaktywnego panelu Web UI** (`http://127.0.0.1:8000`) z edytorem i podglądem na żywo.
5. **Generowania nowoczesnego CV** w formatach **DOCX** i **HTML / PDF**.

---

## 📁 Przejrzysta struktura folderów

```
d:\visualstudio\!cv\
├── source_cvs/             # 📂 TUTAJ WRZUCAJ SWOJE STARE CV (pliki .pdf i .docx)
│   ├── cv_KacperPudelko.pdf
│   └── cv_kacper_pudelko_v2.docx
│
├── output/                 # 📄 TUTAJ ZAPISUJĄ SIĘ WYGENEROWANE NOWE CV
│   ├── nowe_cv.docx        # Gotowy dokument Word (Executive Navy)
│   └── nowe_cv.html        # Gotowy dokument do druku do PDF (Ctrl + P)
│
├── core/                   # ⚙️ LOGIKA BIZNESOWA (Ekstrakcja, Parsowanie, Budowanie)
│   ├── reader.py           # Odczyt plików PDF i Word (tabele, kolumny)
│   ├── parser.py           # Inteligentne rozpoznawanie sekcji
│   ├── merger.py           # Scalanie wielu CV bez duplikatów
│   ├── docx_builder.py     # Generator plików Word .docx
│   ├── html_builder.py     # Generator HTML pod druk PDF (@media print)
│   └── models.py           # Modele danych i serializacja YAML/JSON
│
├── web/                    # 🌐 WSZYSTKO ZWIĄZANE ZE STRONĄ (Panel Web UI)
│   ├── server.py           # Serwer FastAPI i API REST
│   └── templates/          # Szablony HTML
│       └── index.html      # Edytor wizualny + Live Preview
│
├── .venv/                  # 🐍 Środowisko wirtualne Pythona z bibliotekami
├── cv_profile.yaml         # 🤖 GŁÓWNY PLIK TWOJEGO PROFILU (czytelny dla Ciebie i AI)
├── cv_data.json            # 💾 Kopia bazy danych w formacie JSON
├── app.py                  # 🚀 Skrót do uruchomienia panelu graficznego (python app.py)
├── main.py                 # 💻 Główny skrypt CLI (skanowanie, generowanie)
└── requirements.txt        # Zależności projektu
```

---

## 🚀 Jak korzystać z programu?

### 1. Panel graficzny w przeglądarce (Web UI)
Uruchomienie panelu z edytorem formularzy i podglądem na żywo:
```bash
python app.py
```
*(lub w aktywnym venv: `python main.py ui`)*

- Panel otworzy się pod adresem: `http://127.0.0.1:8000`.
- Z lewej strony masz edytor (dane osobowe, doświadczenie, projekty, umiejętności).
- Z prawej strony widzisz podgląd na żywo, który aktualizuje się przy każdej zmianie.
- W nagłówku masz przyciski: **"Zapisz zmiany"**, **"Pobierz DOCX"**, **"Drukuj / PDF"** oraz **"Kopiuj Prompt dla AI"**.

---

### 2. Edycja przez AI (np. ze mną na czacie)
Głównym źródłem prawdy o Twoim CV jest plik:
👉 **`cv_profile.yaml`**

Napisz do mnie (lub dowolnego AI):
> *"Oto moje `cv_profile.yaml`. Dostosuj je pod ofertę na stanowisko Python / Backend Developer: [treść oferty]. Dodaj projekt X i wyeksponuj znajomość Dockera i FastAPI."*

Gdy zaktualizujesz ten plik, wystarczy wpisać w konsoli:
```bash
python main.py build
```
i zaktualizowane CV pojawi się natychmiast w folderze `output/`!

---

### 3. Konsola (CLI)

```bash
# Automatyczny skan folderu source_cvs/ i generowanie nowego CV:
python main.py

# Przebudowanie plików w output/ po modyfikacji cv_profile.yaml:
python main.py build

# Tylko ekstrakcja ze starych CV do cv_profile.yaml i cv_data.json:
python main.py extract
```
