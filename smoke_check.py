"""Integration checks runnable from the packaged executable, without real ID data."""
import io
import json
from pathlib import Path
import sys
import traceback
from types import SimpleNamespace


def run_checks(report_path):
    report = {"ok": False, "frozen": bool(getattr(sys, "frozen", False))}
    try:
        import flet as ft
        import cv2
        import pytesseract
        from PIL import Image, ImageDraw, ImageFont
        from docx import Document
        from contract_templates import build_contract_text
        from document_step import show_document_step
        from rental_terms_step import show_rental_terms_step
        from preview_step import show_preview_step, _docx_bytes, _pdf_bytes

        # Construct every screen in every supported language using the actual Flet API.
        for language in ("ru", "en", "kk"):
            data = {"surname": "ТЕСТОВАЯ", "first_name": "МИЛЕНА", "contract_number": "TEST-123"}
            page = SimpleNamespace(services=[])
            picker = ft.FilePicker()
            show_document_step(language, data, picker, page)
            show_rental_terms_step(language, data)
            show_preview_step(language, data, picker, page)
            text = build_contract_text(language, data)
            assert "TEST-123" in text, "Contract number was not inserted"
            content = _docx_bytes(text)
            reopened = Document(io.BytesIO(content))
            assert "TEST-123" in "\n".join(p.text for p in reopened.paragraphs)
            pdf = _pdf_bytes(text)
            assert pdf.startswith(b"%PDF-") and len(pdf) > 5000
        report["screens_and_exports"] = ["ru", "en", "kk"]
        report["opencv"] = cv2.__version__
        languages = pytesseract.get_languages(config="")
        assert {"eng", "rus", "kaz"}.issubset(languages), languages
        canvas = Image.new("RGB", (700, 120), "white")
        draw = ImageDraw.Draw(canvas)
        font = ImageFont.load_default(size=48)
        draw.text((20, 25), "1234567890", font=font, fill="black")
        result = pytesseract.image_to_string(canvas, lang="eng", config="--psm 7 -c tessedit_char_whitelist=0123456789")
        assert result.strip() == "1234567890", repr(result)
        report["ocr_languages"] = languages
        report["ocr_executable"] = pytesseract.pytesseract.tesseract_cmd
        report["ok"] = True
    except Exception:
        report["error"] = traceback.format_exc()
    Path(report_path).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if not report["ok"]:
        raise SystemExit(1)
