import re
import asyncio
import base64
from datetime import datetime
from pathlib import Path

import flet as ft
from PIL import Image
from image_scan import read_text, read_back_dates, read_front_iin, select_iin
from translations import tr


def find_value_after_label(text, labels):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    known_labels = [
        "ФАМИЛИЯ",
        "ТЕГІ",
        "ИМЯ",
        "АТЫ",
        "ОТЧЕСТВО",
        "ӘКЕСІНІҢ АТЫ",
        "ДАТА РОЖДЕНИЯ",
        "ТУҒАН КҮНІ",
        "ИИН",
        "ЖСН",
    ]

    for index, line in enumerate(lines):
        upper_line = line.upper()

        if any(label.upper() in upper_line for label in labels):
            for candidate in lines[index + 1:]:
                upper_candidate = candidate.upper()

                if any(label in upper_candidate for label in known_labels):
                    break

                return candidate

    return ""


def find_valid_dates(text):
    found_dates = re.findall(r"\b\d{2}\.\d{2}\.\d{4}\b", text)
    valid_dates = []

    for date_text in found_dates:
        try:
            datetime.strptime(date_text, "%d.%m.%Y")
            valid_dates.append(date_text)
        except ValueError:
            continue

    return valid_dates


def clean_person_value(value):
    """Remove OCR label fragments, stray digits and symbols around a name."""
    value = str(value or "").strip()
    label_words = {
        "ФАМИЛИЯ", "ТЕГІ", "ТЕГИ", "ИМЯ", "АТЫ", "ОТЧЕСТВО",
        "ӘКЕСІНІҢ", "АТЫ", "NAME", "SURNAME", "GIVEN", "MIDDLE",
    }
    words = re.findall(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", value.upper(), flags=re.UNICODE)
    words = [word for word in words if len(word) > 2 and word not in label_words]
    if not words:
        return ""

    has_ocr_noise = bool(re.search(r"[^\w\s'-]|\d", value, flags=re.UNICODE))
    if has_ocr_noise:
        chunks = re.split(r"[\d|<>_]+", value)
        clean_chunks = []
        for chunk in chunks:
            chunk_words = re.findall(r"[^\W\d_]+(?:[-'][^\W\d_]+)*", chunk.upper(), flags=re.UNICODE)
            chunk_words = [word for word in chunk_words if len(word) > 2 and word not in label_words]
            if chunk_words and any(len(word) > 3 for word in chunk_words):
                clean_chunks.extend(chunk_words)
        if clean_chunks:
            return " ".join(clean_chunks)
    return " ".join(words)


def extract_front_values(text):
    values = {
        "surname": clean_person_value(find_value_after_label(text, ["ФАМИЛИЯ", "ТЕГІ"])),
        "first_name": clean_person_value(find_value_after_label(text, ["ИМЯ", "АТЫ"])),
        "patronymic": clean_person_value(find_value_after_label(
            text,
            ["ОТЧЕСТВО", "ӘКЕСІНІҢ АТЫ"],
        )),
    }

    dates = list(dict.fromkeys(find_valid_dates(text)))
    birth_date = dates[0] if len(dates) == 1 else ""
    number_pattern = r"(?:[0-9OoОоIl|][\s.,:;\-–—]*){11,14}"
    labeled_runs = re.findall(
        rf"(?:ИИН|ЖСН|IIN)\s*[:№\-]?\s*({number_pattern})",
        text,
        flags=re.IGNORECASE,
    )
    number_runs = labeled_runs + re.findall(
        rf"(?<![A-Za-z0-9]){number_pattern}(?![A-Za-z0-9])",
        text,
        flags=re.IGNORECASE,
    )
    iin = select_iin(number_runs, birth_date)
    if iin:
        values["iin"] = iin

    if len(dates) == 1:
        values["birth_date"] = dates[0]

    return values


def extract_back_values(text):
    values = {}

    numbers = re.findall(r"(?m)^\s*(\d{8,12})\s*$", text)

    if len(numbers) == 1:
        values["document_number"] = numbers[0]

    dates = find_valid_dates(text)

    if len(dates) == 2:
        values["issue_date"] = dates[0]

    return values


def show_document_step(language="ru", data=None, picker=None, page=None, on_next=None):
    data = data if data is not None else {}
    fields = ["surname", "first_name", "patronymic", "birth_date", "iin", "document_number", "issue_date"]
    entries = {}
    saved_previews = data.setdefault("_document_preview_images", {})
    previews = {}
    for side in ("front", "back"):
        saved_src = saved_previews.get(side)
        image_control = (
            ft.Image(src=saved_src, width=300, height=180, fit=ft.BoxFit.CONTAIN)
            if saved_src else None
        )
        previews[side] = ft.Container(content=image_control, width=300, height=180)
    status = ft.Text(color=ft.Colors.BLUE_GREY_700)
    file_pickers = data.setdefault("_document_file_pickers", {})
    for side in ("front", "back"):
        if side not in file_pickers:
            file_pickers[side] = ft.FilePicker()
        if page is not None and file_pickers[side] not in page.services:
            page.services.append(file_pickers[side])

    def set_status(message, error=False):
        status.value = message
        status.color = ft.Colors.RED_700 if error else ft.Colors.BLUE_GREY_700
        status.update()

    def changed(e):
        data[e.control.data] = e.control.value

    def next_clicked(_e):
        on_next()

    for field_name in fields:
        entries[field_name] = ft.TextField(
            label=tr(language, field_name), value=data.get(field_name, ""),
            on_change=changed, data=field_name, expand=True,
        )

    field_names_by_side = {
        "front": ["surname", "first_name", "patronymic", "birth_date", "iin"],
        "back": ["document_number", "issue_date"],
    }

    async def load_side(side, files):
        if not files:
            return
        image_path = files[0].path
        if not image_path:
            set_status(tr(language, "ocr_desktop_only"), error=True)
            return
        for name in field_names_by_side[side]:
            entries[name].value = ""
            data[name] = ""
        try:
            with Image.open(image_path) as image:
                image.thumbnail((600, 360))
                buffer = __import__("io").BytesIO()
                image.convert("RGB").save(buffer, format="JPEG", quality=82)
                preview_src = "data:image/jpeg;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")
                saved_previews[side] = preview_src
                previews[side].content = ft.Image(
                    src=preview_src, width=300, height=180, fit=ft.BoxFit.CONTAIN
                )
            previews[side].update()
            set_status(tr(language, "ocr_running"))
            recognized_text = await asyncio.to_thread(read_text, image_path)
            if not recognized_text.strip():
                set_status(tr(language, "no_text"), error=True)
                return
            if side == "front":
                values = extract_front_values(recognized_text)
                focused_iin = await asyncio.to_thread(read_front_iin, image_path, values.get("birth_date", ""))
                if focused_iin:
                    values["iin"] = focused_iin
            else:
                values = extract_back_values(recognized_text)
                try:
                    date_text = await asyncio.to_thread(read_back_dates, image_path)
                    dates = find_valid_dates(date_text)
                    if len(dates) == 2:
                        values["issue_date"] = dates[0]
                except Exception:
                    pass
            for field_name, value in values.items():
                if value and field_name in entries:
                    entries[field_name].value = value
                    data[field_name] = value
            for entry in entries.values():
                entry.update()
            if side == "front" and not values.get("iin"):
                set_status(tr(language, "iin_manual"), error=True)
            else:
                set_status(tr(language, "check_values"))
        except Exception as error:
            set_status(f"{tr(language, 'manual_entry')}\n{error}", error=True)

    def make_file_handler(side):
        async def handle_file_result(event):
            await load_side(side, event.files)
        return handle_file_result

    for side in ("front", "back"):
        file_pickers[side].on_result = make_file_handler(side)


    def field_card(side, title, upload_key):
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=16, weight=ft.FontWeight.BOLD),
                ft.Container(content=previews[side], alignment=ft.Alignment.CENTER,
                             bgcolor=ft.Colors.GREY_100, border_radius=8, height=190),
                ft.Button(
                    content=tr(language, upload_key),
                    icon=ft.Icons.UPLOAD_FILE,
                    action=ft.PickFiles(
                        file_picker=file_pickers[side],
                        dialog_title=tr(language, "select_image"),
                        file_type=ft.FilePickerFileType.IMAGE,
                        allow_multiple=False,
                    ),
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            padding=14, border=ft.Border.all(1, ft.Colors.GREY_300), border_radius=12,
            expand=True,
        )

    return ft.Column(
        controls=[
            ft.Text(tr(language, "upload_both"), size=21, weight=ft.FontWeight.BOLD),
            ft.ResponsiveRow([
                ft.Container(content=field_card("front", tr(language, "front_side"), "upload_front"), col={"sm": 12, "md": 6}),
                ft.Container(content=field_card("back", tr(language, "back_side"), "upload_back"), col={"sm": 12, "md": 6}),
            ], spacing=12),
            ft.ResponsiveRow([
                ft.Container(
                    content=ft.Column(
                        controls=[entries[name] for name in ("surname", "first_name", "patronymic", "birth_date", "iin")],
                        spacing=8,
                    ),
                    col={"sm": 12, "md": 6},
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[entries[name] for name in ("document_number", "issue_date")],
                        spacing=8,
                    ),
                    col={"sm": 12, "md": 6},
                ),
            ], spacing=12, run_spacing=2),
            status,
            ft.Row([ft.Container(expand=True), ft.Button(content=tr(language, "next"), icon=ft.Icons.ARROW_FORWARD,
                                                        on_click=next_clicked)]),
        ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=12,
    )
