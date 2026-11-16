import flet as ft

from document_step import show_document_step
from preview_step import show_preview_step
from rental_terms_step import show_rental_terms_step
from translations import tr


LANGUAGES = {"ru": "Русский", "en": "English", "kk": "Qazaqşa"}
STEPS = ["person_data", "rental_terms", "preview"]


def main(page: ft.Page):
    data = {}
    state = {"language": "ru", "step": STEPS[0]}
    picker = ft.FilePicker()
    page.services.append(picker)
    page.title = tr("ru", "app_title")
    page.window.width = 1000
    page.window.height = 780
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="#315b73")


    def go_to(step):
        state["step"] = step
        render()

    def set_language(e):
        state["language"] = e.control.value
        page.title = tr(state["language"], "app_title")
        render()

    def render():
        lang = state["language"]
        current = state["step"]
        page.title = tr(lang, "app_title")
        nav = ft.Row(
            controls=[
                ft.Button(
                    content=tr(lang, step),
                    on_click=lambda _e, target=step: go_to(target),
                    disabled=step == current,
                )
                for step in STEPS
            ]
            + [
                ft.Text(tr(lang, "language")),
                ft.Dropdown(
                    width=150,
                    value=lang,
                    options=[ft.DropdownOption(key=key, text=name) for key, name in LANGUAGES.items()],
                    on_select=set_language,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            wrap=True,
        )
        if current == "person_data":
            content = show_document_step(
                lang, data, picker, page,
                on_next=lambda: go_to("rental_terms"),
            )
        elif current == "rental_terms":
            content = show_rental_terms_step(
                lang, data,
                on_back=lambda: go_to("person_data"),
                on_next=lambda: go_to("preview"),
            )
        else:
            content = show_preview_step(
                lang, data, picker, page,
                on_back=lambda: go_to("rental_terms"),
            )
        page.controls.clear()
        page.add(nav, content)
        page.update()

    render()


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 3 and sys.argv[1] == "--self-test":
        from smoke_check import run_checks

        run_checks(sys.argv[2])
    else:
        ft.run(main)
