"""
Reader module to extract raw text from PDF and Word (.docx) files.
Handles both standard paragraphs and multi-column table layouts.
"""
import os
import re
from typing import List, Dict, Optional, Tuple
import pypdf
import docx

class DocumentReader:
    @staticmethod
    def read_pdf(file_path: str) -> List[str]:
        """
        Extracts lines of text from a PDF document.
        Handles page-by-page extraction and basic formatting cleanup.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Nie znaleziono pliku: {file_path}")

        extracted_lines: List[str] = []
        reader = pypdf.PdfReader(file_path)

        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            raw_lines = text.split("\n")
            for line in raw_lines:
                clean_l = line.strip()
                if clean_l:
                    extracted_lines.append(clean_l)

        return extracted_lines

    @staticmethod
    def read_docx(file_path: str) -> List[str]:
        """
        Extracts lines of text from a Word (.docx) document.
        Accurately reads normal paragraphs and handles table-based multi-column CVs.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Nie znaleziono pliku: {file_path}")

        extracted_lines: List[str] = []
        doc = docx.Document(file_path)

        # 1. Read document-level paragraphs
        for p in doc.paragraphs:
            text = p.text.strip()
            if text:
                extracted_lines.append(text)

        # 2. Read tables (preserving multi-column structure)
        for table in doc.tables:
            num_rows = len(table.rows)
            num_cols = len(table.columns)

            if num_rows == 1 and num_cols > 1:
                for cell in table.rows[0].cells:
                    for p in cell.paragraphs:
                        text = p.text.strip()
                        if text:
                            extracted_lines.append(text)
            else:
                visited_cells = set()
                for row in table.rows:
                    for cell in row.cells:
                        cell_id = id(cell._tc)
                        if cell_id in visited_cells:
                            continue
                        visited_cells.add(cell_id)

                        for p in cell.paragraphs:
                            text = p.text.strip()
                            if text:
                                extracted_lines.append(text)

        return extracted_lines

    @classmethod
    def read_file(cls, file_path: str) -> List[str]:
        """
        Reads any supported file (.pdf or .docx) and returns its lines.
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            return cls.read_pdf(file_path)
        elif ext in (".docx", ".doc"):
            if ext == ".doc":
                raise ValueError("Format .doc (stary format Word) nie jest bezpośrednio wspierany. Zapisz plik jako .docx.")
            return cls.read_docx(file_path)
        else:
            raise ValueError(f"Nieobsługiwany format pliku: {ext}. Obsługiwane to: .pdf, .docx")

    @classmethod
    def discover_files(cls, directory: str = "source_cvs") -> List[str]:
        """
        Finds all .pdf and .docx CV files in the given directory (default: source_cvs),
        or falls back to root '.' if source_cvs is empty or doesn't exist.
        Ignores temporary files (like ~$temp.docx) and already generated CV files.
        """
        search_dirs = [directory]
        if directory != ".":
            search_dirs.append(".")

        for d in search_dirs:
            if not os.path.isdir(d):
                continue
            discovered = []
            for filename in os.listdir(d):
                if filename.startswith("~$") or filename.startswith("."):
                    continue
                lower = filename.lower()
                if lower.endswith((".pdf", ".docx")):
                    if "nowe_cv" in lower or "wygenerowane_cv" in lower or "generated_cv" in lower:
                        continue
                    full_path = os.path.join(d, filename)
                    if os.path.isfile(full_path):
                        discovered.append(full_path)
            if discovered:
                return sorted(discovered)
        return []
