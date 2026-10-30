"""
Skrót do uruchomienia interaktywnego panelu graficznego CV Studio (Web UI).

Uruchomienie:
    python app.py
"""
from server import run_server

if __name__ == "__main__":
    run_server(host="127.0.0.1", port=8000, open_browser=True)

