"""
FastAPI Server for CV Studio Web UI.
Handles web interface, live preview, editing, and document generation.
"""
import os
import sys
import webbrowser
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Add workspace root to sys.path so 'core' can be imported easily
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.models import CVData
from core.reader import DocumentReader
from core.parser import CVParser
from core.merger import CVMerger
from core.docx_builder import DocxCVBuilder
from core.html_builder import HtmlCVBuilder

app = FastAPI(title="CV Studio")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
SOURCE_DIR = os.path.join(ROOT_DIR, "source_cvs")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
YAML_FILE = os.path.join(ROOT_DIR, "cv_profile.yaml")
JSON_FILE = os.path.join(ROOT_DIR, "cv_data.json")
DOCX_FILE = os.path.join(OUTPUT_DIR, "nowe_cv.docx")
HTML_FILE = os.path.join(OUTPUT_DIR, "nowe_cv.html")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(SOURCE_DIR, exist_ok=True)

# Mount static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/favicon.ico", include_in_schema=False)
@app.get("/favoicon.ico", include_in_schema=False)
@app.get("/favicon.svg", include_in_schema=False)
async def get_favicon_ico():
    for name in ("favoicon.ico", "favicon.ico"):
        ico_path = os.path.join(STATIC_DIR, name)
        if os.path.isfile(ico_path):
            return FileResponse(ico_path, media_type="image/x-icon")
    raise HTTPException(status_code=404, detail="Brak pliku favoicon.ico")

def get_current_cv() -> CVData:
    """Loads CV from YAML (preferred), JSON, or extracts from source files if needed."""
    if os.path.isfile(YAML_FILE):
        try:
            with open(YAML_FILE, "r", encoding="utf-8") as f:
                return CVData.from_yaml(f.read())
        except Exception as e:
            print(f"Błąd czytania {YAML_FILE}: {e}")

    if os.path.isfile(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                return CVData.from_json(f.read())
        except Exception as e:
            print(f"Błąd czytania {JSON_FILE}: {e}")

    # Fallback: scan files in source_cvs (or root)
    files = DocumentReader.discover_files(SOURCE_DIR)
    if files:
        cv_list = [CVParser.parse(DocumentReader.read_file(f)) for f in files]
        merged = CVMerger.merge(cv_list)
        save_cv_to_disk(merged)
        return merged

    return CVData()

def save_cv_to_disk(cv: CVData):
    """Saves to YAML & JSON in root, and generates DOCX & HTML in output/."""
    # 1. YAML
    with open(YAML_FILE, "w", encoding="utf-8") as f:
        f.write(cv.to_yaml())

    # 2. JSON
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        f.write(cv.to_json(indent=2))

    # 3. DOCX in output/
    docx_builder = DocxCVBuilder(cv)
    docx_builder.build(DOCX_FILE)

    # 4. HTML in output/
    html_builder = HtmlCVBuilder(cv)
    html_builder.build(HTML_FILE)

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if not os.path.isfile(template_path):
        raise HTTPException(status_code=404, detail="Brak pliku index.html w katalogu templates")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/cv")
async def api_get_cv():
    cv = get_current_cv()
    return {
        "cv": cv.to_dict(),
        "yaml": cv.to_yaml()
    }

@app.post("/api/save")
async def api_save_cv(request: Request):
    try:
        data = await request.json()
        cv = CVData.from_dict(data)
        save_cv_to_disk(cv)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.post("/api/preview-html", response_class=HTMLResponse)
async def api_preview_html(request: Request):
    try:
        data = await request.json()
        cv = CVData.from_dict(data)
        builder = HtmlCVBuilder(cv)
        temp_html_path = os.path.join(OUTPUT_DIR, "temp_preview.html")
        builder.build(temp_html_path)
        with open(temp_html_path, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content)
    except Exception as e:
        return HTMLResponse(f"<html><body><h3>Błąd renderowania podglądu: {e}</h3></body></html>")

@app.post("/api/to-yaml")
async def api_to_yaml(request: Request):
    try:
        data = await request.json()
        cv = CVData.from_dict(data)
        return {"yaml": cv.to_yaml()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/from-yaml")
async def api_from_yaml(request: Request):
    try:
        payload = await request.json()
        yaml_content = payload.get("yaml", "")
        cv = CVData.from_yaml(yaml_content)
        return {"ok": True, "cv": cv.to_dict()}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.post("/api/reload-files")
async def api_reload_files():
    try:
        files = DocumentReader.discover_files(SOURCE_DIR)
        if not files:
            return {"ok": False, "error": f"Nie znaleziono plików PDF/DOCX w katalogu {SOURCE_DIR}"}
        cv_list = [CVParser.parse(DocumentReader.read_file(f)) for f in files]
        merged = CVMerger.merge(cv_list)
        save_cv_to_disk(merged)
        return {"ok": True, "cv": merged.to_dict()}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.get("/api/export-docx")
async def api_export_docx():
    if not os.path.isfile(DOCX_FILE):
        cv = get_current_cv()
        save_cv_to_disk(cv)
    return FileResponse(
        DOCX_FILE,
        filename="nowe_cv.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

def run_server(host: str = "127.0.0.1", port: int = 8000, open_browser: bool = True):
    url = f"http://{host}:{port}"
    print(f"\n🚀 Uruchamianie CV Studio pod adresem: {url}")
    print("   Naciśnij Ctrl+C, aby zatrzymać serwer.\n")
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    uvicorn.run(app, host=host, port=port, log_level="info")

if __name__ == "__main__":
    run_server()
