# CV Extractor & Generator (PDF & Word -> Nowe CV + Web Studio)

Kompletne narzędzie w Pythonie do:
1. **Ekstrakcji danych ze starych CV** w formatach **PDF** (`.pdf`) oraz **Word** (`.docx`).
2. **Inteligentnego scalania danych** z wielu plików (deduplikacja, uzupełnianie braków).
3. **Zapisu w formacie AI-Friendly (`cv_profile.yaml`)** – czytelnym dla człowieka i idealnym do edycji przez sztuczną inteligencję (np. Antigravity, ChatGPT, Claude).
4. **Interaktywnego panelu Web UI (`http://127.0.0.1:8000`)** – wizualny edytor z podglądem na żywo (Live Preview), zakładką YAML dla AI i natychmiastowym eksportem do Worda i PDF.
5. **Generowania profesjonalnych dokumentów**:
   - **`nowe_cv.docx`** – edytowalny plik Word z nowoczesną typografią Executive Navy.
   - **`nowe_cv.html`** – responsywny podgląd gotowy do druku do PDF (**Ctrl + P**).

---

## 🖥️ 1. Interaktywny Panel Graficzny (Web Studio)

Aby uruchomić edytor z podglądem na żywo w przeglądarce, wpisz:

```bash
python app.py
# lub:
python main.py ui
```

W oknie przeglądarki (`http://127.0.0.1:8000`) zyskujesz:
- **Wizualny formularz**: edycja danych osobowych, podsumowania, doświadczenia, startupów, projektów, umiejętności i wykształcenia.
- **Dodawanie / usuwanie wpisów**: przyciski `+ Dodaj punkt`, `+ Dodaj stanowisko`, `+ Dodaj projekt`.
- **Podgląd na żywo (Live Preview)**: prawa strona odświeża się automatycznie po każdej zmianie.
- **Zakładka "Edytor YAML (Dla AI)"**: możliwość bezpośredniego wklejenia kodu YAML wygenerowanego przez AI.
- **Przycisk "Kopiuj Prompt dla AI"**: kopiuje do schowka gotowy szablon z Twoimi danymi, abyś mógł zapytać dowolne AI o przeróbkę.
- **Pobieranie jednym kliknięciem**: przycisk **"Pobierz DOCX"** oraz **"Drukuj / PDF"**.

---

## 🤖 2. Jak edytować CV za pomocą AI?

Twoje CV jest zapisane w pliku:
👉 **`cv_profile.yaml`**

Format YAML jest stworzony dla modeli językowych (brak uciążliwych nawiasów czy cudzysłowów, naturalny podział wcięciami). 

### Przykłady promptów, które możesz zadać mnie (Antigravity) lub innemu AI:

> *"Oto moje CV w `cv_profile.yaml`. Zmodyfikuj je pod ofertę pracy na stanowisko Senior Python / Backend Developer: [wklej treść oferty]. Uwydatnij projekty Neocal AI i DataExtractAI oraz dodaj technologię Redis."*

> *"Przetłumacz całe `cv_profile.yaml` na profesjonalny język angielski."*

> *"W `cv_profile.yaml` dopisz nowe stanowisko: Full Stack Developer w firmie ABC (od 01.2025 do teraz) i dodaj 3 mocne punkty osiągnięć z liczbami."*

Po otrzymaniu odpowiedzi:
1. Zapisujesz zmiany bezpośrednio w pliku `cv_profile.yaml` (albo wklejasz kod w panelu Web UI w zakładce YAML).
2. Wpisujesz w konsoli:
   ```bash
   python main.py build
   ```
   i nowe pliki `nowe_cv.docx` oraz `nowe_cv.html` generują się natychmiast!

---

## ⚡ 3. Dostępne polecenia w konsoli (CLI)

```bash
# 1. Pełny skan folderu i wygenerowanie nowego CV:
python main.py

# 2. Uruchomienie panelu graficznego w przeglądarce:
python app.py
# lub:
python main.py ui

# 3. Przebudowanie CV po edycji cv_profile.yaml (lub cv_data.json):
python main.py build

# 4. Tylko ekstrakcja ze starych plików do YAML/JSON:
python main.py extract

# 5. Ekstrakcja tylko ze wskazanych plików:
python main.py run moje_stare_cv.pdf inne_cv.docx
```

---

## 📂 Struktura plików

- `app.py` / `server.py` – serwer lokalny FastAPI napędzający panel graficzny.
- `templates/index.html` – interfejs panelu (dwukolumnowy edytor + Live Preview).
- `cv_profile.yaml` – **główny plik profilu dla Ciebie i AI**.
- `cv_data.json` – alternatywny format JSON.
- `nowe_cv.docx` – wygenerowany plik Word.
- `nowe_cv.html` – wygenerowany plik HTML / druk PDF.
- `docx_builder.py` – silnik formatowania Word.
- `html_builder.py` – silnik formatowania HTML / PDF.
- `reader.py` – ekstraktor tekstu z PDF i Word (tabele, kolumny).
- `parser.py` – parser sekcji CV.
- `merger.py` – scalanie danych bez duplikatów.
- `models.py` – definicje klas i serializacja YAML/JSON.
