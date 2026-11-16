import io
import os
from pathlib import Path

import flet as ft

from contract_templates import SOURCE_DOCX, build_contract_text
from translations import tr


def _docx_bytes(text):
    from docx import Document

    document = Document(str(SOURCE_DOCX))
    lines = text.splitlines()
    while len(document.paragraphs) < len(lines):
        document.add_paragraph()
    for index, line in enumerate(lines):
        document.paragraphs[index].text = line
    for paragraph in document.paragraphs[len(lines):]:
        paragraph.text = ""
    result = io.BytesIO()
    document.save(result)
    return result.getvalue()


def _pdf_bytes(text):
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    font_candidates = [
        Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts" / "arial.ttf",
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/Library/Fonts/Arial.ttf"),
        Path(__import__("reportlab").__file__).parent / "fonts" / "Vera.ttf",
    ]
    font_path = next((path for path in font_candidates if path.exists()), None)
    font_name = "Helvetica"
    if font_path:
        font_name = "LeaseFont"
        pdfmetrics.registerFont(TTFont(font_name, str(font_path)))

    output = io.BytesIO()
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "LeaseBody", parent=styles["Normal"], fontName=font_name, fontSize=9,
        leading=12, alignment=TA_LEFT, spaceAfter=5,
    )
    document = SimpleDocTemplate(output, pagesize=A4, rightMargin=52, leftMargin=52,
                                 topMargin=48, bottomMargin=48)
    story = []
    for line in text.splitlines():
        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") or "&nbsp;"
        story.extend([Paragraph(safe, body), Spacer(1, 2)])
    document.build(story)
    return output.getvalue()


def show_preview_step(language, data, picker, page, on_back=None):
    previews = data.setdefault("contract_preview_by_language", {})
    preview_sources = data.setdefault("contract_preview_source_by_language", {})
    generated_text = build_contract_text(language, data)
    if preview_sources.get(language) == generated_text and previews.get(language):
        initial_text = previews[language]
    else:
        initial_text = generated_text
    preview_sources[language] = generated_text
    editor = ft.TextField(
        value=initial_text,
        multiline=True, min_lines=12, expand=True,
        text_size=14, color=ft.Colors.BLUE_GREY_900,
        bgcolor=ft.Colors.WHITE,
        border=ft.OutlineInputBorder(border_radius=10),
    )
    document_text = ft.Text(
        value=initial_text, size=14, color=ft.Colors.BLUE_GREY_900,
        selectable=True,
    )
    paper = ft.Container(
        content=ft.Column([document_text], scroll=ft.ScrollMode.AUTO, expand=True),
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        border_radius=10,
        padding=24,
        expand=True,
    )
    preview_area = ft.Container(content=paper, expand=True)
    editing = {"active": False}
    status = ft.Text(color=ft.Colors.BLUE_GREY_700)

    def persist(_e=None):
        previews[language] = editor.value or ""

    def rebuild(_e):
        editor.value = build_contract_text(language, data)
        preview_sources[language] = editor.value
        document_text.value = editor.value
        persist()
        if editing["active"]:
            editor.update()
        else:
            document_text.update()
        status.value = ""
        status.update()

    def toggle_edit(_e):
        if editing["active"]:
            persist()
            document_text.value = editor.value or ""
            preview_area.content = paper
            editing["active"] = False
            edit_button.content = tr(language, "edit_text")
        else:
            preview_area.content = editor
            editing["active"] = True
            edit_button.content = tr(language, "show_preview")
        preview_area.update()
        edit_button.update()

    async def export(extension, content):
        persist()
        try:
            result = await picker.save_file(
                dialog_title=tr(language, "save_contract"),
                file_name=f"lease_agreement.{extension}",
                file_type=ft.FilePickerFileType.CUSTOM,
                allowed_extensions=[extension],
                src_bytes=content,
            )
            if result:
                status.value = f"{tr(language, 'export_done')}: {result}"
                status.color = ft.Colors.GREEN_700
            else:
                status.value = ""
        except Exception as error:
            status.value = f"{tr(language, 'export_error')}\n{error}"
            status.color = ft.Colors.RED_700
        status.update()

    async def export_docx(_e):
        try:
            content = await __import__("asyncio").to_thread(_docx_bytes, editor.value or "")
            await export("docx", content)
        except Exception as error:
            status.value = f"{tr(language, 'export_error')}\n{error}"
            status.color = ft.Colors.RED_700
            status.update()

    async def export_pdf(_e):
        try:
            content = await __import__("asyncio").to_thread(_pdf_bytes, editor.value or "")
            await export("pdf", content)
        except Exception as error:
            status.value = f"{tr(language, 'export_error')}\n{error}"
            status.color = ft.Colors.RED_700
            status.update()

    editor.on_change = persist
    edit_button = ft.Button(content=tr(language, "edit_text"), icon=ft.Icons.EDIT,
                             on_click=toggle_edit)
    return ft.Column([
        ft.Text(tr(language, "preview"), size=21, weight=ft.FontWeight.BOLD),
        ft.Text(tr(language, "preview_help"), color=ft.Colors.BLUE_GREY_700),
        ft.Row([
            ft.Button(content=tr(language, "back"), icon=ft.Icons.ARROW_BACK,
                      on_click=lambda _e: on_back()),
            ft.Button(content=tr(language, "rebuild_preview"), icon=ft.Icons.REFRESH,
                      on_click=rebuild),
            edit_button,
            ft.Button(content="DOCX", icon=ft.Icons.DESCRIPTION, on_click=export_docx),
            ft.Button(content="PDF", icon=ft.Icons.PICTURE_AS_PDF, on_click=export_pdf),
        ], wrap=True),
        preview_area,
        status,
    ], expand=True, spacing=10)
