# CV Extractor & Generator (PDF & Word -> Nowe CV)

Program w Pythonie (CLI bez konieczności uruchamiania frontendu) stworzony do:
1. **Automatycznej ekstrakcji danych ze starych CV** w formatach **PDF** (`.pdf`) oraz **Word** (`.docx`) – w tym tabel i układów wielokolumnowych.
2. **Inteligentnego łączenia i deduplikacji danych** z wielu plików naraz (uzupełnia brakujące pozycje ze starych wersji).
3. **Generowania nowego, profesjonalnego CV** w dwóch nowoczesnych formatach:
   - **`nowe_cv.docx`** – gotowy do edycji w Microsoft Word / LibreOffice plik z nowoczesną typografią, paletą kolorów (Executive Navy), podziałem na sekcje, klikalnymi linkami i klauzulą RODO.
   - **`nowe_cv.html`** – responsywny podgląd CV, który po otwarciu w dowolnej przeglądarce pozwala wydrukować lub zapisać dokument jako idealny **PDF (Ctrl + P)** z gotowymi regułami `@media print`.
   - **`cv_data.json`** – ustrukturyzowana baza Twoich danych w czytelnym formacie JSON, którą możesz w każdej chwili edytować w notatniku/VS Code i błyskawicznie przebudować CV jednym poleceniem.

---

## 🚀 Szybki start (Najprostsze użycie)

Wystarczy umieścić swoje stare pliki CV w katalogu projektu (np. `cv_KacperPudelko.pdf`, `cv_kacper_pudelko_v2.docx`) i uruchomić:

```bash
python main.py
```

Program automatycznie:
- Przeskanuje folder w poszukiwaniu plików `.pdf` i `.docx`,
- Wyciągnie dane kontaktowe, doświadczenie, startupy, wykształcenie, projekty, technologie i języki,
- Połączy je w jeden spójny profil i zapisze do `cv_data.json`,
- Wygeneruje **`nowe_cv.docx`** oraz **`nowe_cv.html`**.

---

## 🛠️ Dostępne polecenia

### 1. Pełny przebieg (domyślny)
```bash
python main.py
# lub:
python main.py run
```

### 2. Tylko ekstrakcja do JSON
Jeśli chcesz najpierw sprawdzić lub zmodyfikować wyciągnięte dane przed wygenerowaniem nowego CV:
```bash
python main.py extract
```
Spowoduje to utworzenie pliku `cv_data.json`.

### 3. Generowanie CV na podstawie zmodyfikowanego `cv_data.json`
Po ręcznej edycji lub dodaniu nowych punktów w `cv_data.json`:
```bash
python main.py build
```

### 4. Ekstrakcja tylko ze wskazanych plików
Możesz wskazać konkretne pliki:
```bash
python main.py run moje_stare_cv.pdf inne_cv.docx
```

---

## 📂 Struktura projektu

- `main.py` – główny punkt wejścia CLI z czytelnym interfejsem w konsoli.
- `reader.py` – moduł odczytu PDF (`pypdf`) i Word (`python-docx`), radzący sobie z wąskimi kolumnami i tabelami CV.
- `parser.py` – inteligentny parser tekstu rozpoznający sekcje (doświadczenie, edukacja, startupy, projekty, technologie, języki, RODO).
- `merger.py` – algorytm scalający dane z wielu dokumentów (zapobiega duplikatom i uzupełnia braki).
- `docx_builder.py` – generator dokumentu Word (`.docx`) z nowoczesnym stylem i formatowaniem.
- `html_builder.py` – generator HTML ze stylami druku PDF (`@media print`).
- `models.py` – modele danych (`CVData`, `ExperienceItem`, `ProjectItem` itd.).
- `cv_data.json` – wyekstrahowana baza danych Twojego profilu.
- `requirements.txt` – zależności (`pypdf`, `python-docx`).

---

## 🖨️ Zapis do PDF
Otwórz plik `nowe_cv.html` w przeglądarce (Chrome, Edge itp.) i:
1. Kliknij przycisk **"Drukuj / Zapisz jako PDF"** (lub naciśnij `Ctrl + P`).
2. Jako cel wybierz: **Zapisz jako PDF** (Save as PDF).
3. Ustawienia: Rozmiar A4, marginesy domyślne.

