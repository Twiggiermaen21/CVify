"""
Skrót do uruchomienia interaktywnego panelu Web UI (CV Studio).

Uruchomienie:
    python app.py
"""
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from web.server import run_server

if __name__ == "__main__":
    run_server(host="127.0.0.1", port=8000, open_browser=True)
