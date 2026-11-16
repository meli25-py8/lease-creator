#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
trap 'echo; echo "Press Enter to close."; read -r' EXIT
if ! command -v python3 >/dev/null; then
  echo "Install Python 3.12 or newer from https://www.python.org/downloads/macos/ and run this file again."
  exit 1
fi
python3 -m venv .venv-mac
.venv-mac/bin/python -m pip install -r requirements-build.txt
.venv-mac/bin/python build_desktop.py
echo "Application created: dist/LeaseCreator.app"
echo "OCR requires Tesseract: brew install tesseract tesseract-lang"
open dist
