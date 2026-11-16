"""Build a native desktop bundle on Windows or macOS."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parent


def main():
    os.chdir(ROOT)
    windows = sys.platform == "win32"
    if not windows and sys.platform != "darwin":
        raise SystemExit("Run this builder on Windows or macOS.")
    icon = ROOT / "assets" / ("icon.ico" if windows else "icon.icns")
    with Image.open(ROOT / "assets" / "icon.png") as source:
        source.save(icon)
    command = [
        str(Path(sys.executable).with_name("flet.exe" if windows else "flet")),
        "pack", "app.py", "--name", "LeaseCreator", "--onedir",
        "--icon", str(icon), "--product-name", "Создание договора",
        "--product-version", "1.0.0", "--file-version", "1.0.0.0",
        "--add-data", "contract_source.docx:.", "--add-data", "assets:assets",
        "--hidden-import", "cv2", "--hidden-import", "PIL.ImageDraw",
        "--hidden-import", "PIL.ImageFont", "--yes", "-v",
    ]
    if windows:
        source = Path(os.environ.get("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")).parent
        bundle = ROOT / "packaging" / "tesseract"
        (bundle / "tessdata").mkdir(parents=True, exist_ok=True)
        for file in [source / "tesseract.exe", *source.glob("*.dll")]:
            shutil.copy2(file, bundle / file.name)
        for language in ("eng", "rus", "kaz"):
            shutil.copy2(source / "tessdata" / f"{language}.traineddata", bundle / "tessdata")
        shutil.copytree(source / "doc", bundle / "doc", dirs_exist_ok=True)
        command.extend(["--add-data", f"{bundle}:tesseract"])
    else:
        command.extend(["--bundle-id", "com.milena.leasecreator"])
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
