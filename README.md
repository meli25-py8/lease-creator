# Создание договора аренды

Настольное приложение на Python и Flet: загрузка фотографий удостоверения,
распознавание данных, заполнение условий аренды, редактирование текста
и сохранение договора в DOCX/PDF. Интерфейс на русском, английском и казахском.

## Запуск из исходников

Используйте Python 3.14. В Windows запустите `setup.bat`, затем `run.bat`.
Для ручной установки:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS: source .venv/bin/activate
python -m pip install -r requirements-build.txt
python app.py
```

Для распознавания нужен Tesseract OCR с языками `eng`, `rus`, `kaz`.
На Windows ожидается `C:\Program Files\Tesseract-OCR\tesseract.exe`;
другой путь задаётся через `TESSERACT_CMD`. На Mac с установленным Homebrew:

```bash
brew install tesseract tesseract-lang
```

Без Tesseract можно заполнить данные вручную и сохранить договор.
Данные текущего заполнения не сохраняются между запусками.

## Сборка приложения

- **Windows:** запустите `build_windows.bat`. Результат:
  `dist/LeaseCreator/LeaseCreator.exe`. Переносите всю папку `LeaseCreator`.
  Сборщик включает локально установленный Tesseract и три языковых пакета.
- **macOS:** запустите `build_mac.command` на Mac. Результат:
  `dist/LeaseCreator.app`. Подробности в `ДЛЯ_MAC.txt`.
  Tesseract на Mac устанавливается отдельно.

Windows-сборка проверена: запуск окна, создание экранов на трёх языках,
формирование DOCX/PDF, распознавание синтетического изображения.
Сборка на macOS пока не проверена; подпись Apple и нотарификация не настроены.

## Содержимое репозитория

- `app.py` — запуск и навигация.
- `document_step.py`, `image_scan.py` — загрузка и распознавание удостоверения.
- `rental_terms_step.py` — условия аренды.
- `preview_step.py` — просмотр, редактирование и экспорт.
- `contract_templates.py`, `contract_source.docx` — подготовка текста и шаблон.
- `translations.py` — переводы интерфейса.
- `build_desktop.py` — упаковка приложения.
- `smoke_check.py` — интеграционная проверка, включая OCR.

Среды Python, скачанные библиотеки и готовые сборки исключены через `.gitignore`.
Готовые архивы приложений можно размещать отдельно в GitHub Releases.
