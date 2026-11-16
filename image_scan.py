import re
import os
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path

import pytesseract
from PIL import Image, ImageOps, ImageFilter


def _find_tesseract():
    configured = os.environ.get("TESSERACT_CMD")
    if configured and Path(configured).exists():
        return configured
    bundled = Path(__file__).with_name("tesseract")
    candidates = [
        bundled / "tesseract.exe", bundled / "tesseract",
        Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
        Path("/opt/homebrew/bin/tesseract"), Path("/usr/local/bin/tesseract"),
        Path("/usr/bin/tesseract"),
    ]
    return str(next((candidate for candidate in candidates if candidate.exists()), None) or shutil.which("tesseract") or "tesseract")


pytesseract.pytesseract.tesseract_cmd = _find_tesseract()
_bundled_tessdata = Path(__file__).with_name("tesseract") / "tessdata"
if _bundled_tessdata.is_dir():
    os.environ["TESSDATA_PREFIX"] = str(_bundled_tessdata)


def read_text(image_path):
    image = Image.open(image_path).convert("RGB")
    full = _ocr_text(image, "--psm 11")
    card = _rectify_id_card(image)
    if card is None:
        return full
    return _ocr_text(card, "--psm 6") + "\n" + full


def _ocr_text(image, config):
    image = ImageOps.autocontrast(image.convert("L"))
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)
    image = image.filter(ImageFilter.SHARPEN)
    return pytesseract.image_to_string(image, lang="rus+eng+kaz", config=config)


def _rectify_id_card(image):
    """Find and perspective-correct a photographed landscape ID card."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return None

    rgb = np.asarray(image.convert("RGB"))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 35, 110)
    edges = cv2.dilate(edges, np.ones((3, 3), dtype=np.uint8), iterations=1)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    image_area = image.width * image.height
    candidates = []
    for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:80]:
        area = cv2.contourArea(contour)
        if area < image_area * 0.06:
            break
        perimeter = cv2.arcLength(contour, True)
        polygon = cv2.approxPolyDP(contour, 0.025 * perimeter, True)
        if len(polygon) != 4 or not cv2.isContourConvex(polygon):
            continue
        points = polygon.reshape(4, 2).astype("float32")
        ordered = _order_corners(points)
        top_left, top_right, bottom_right, bottom_left = ordered
        card_width = max(np.linalg.norm(bottom_right - bottom_left), np.linalg.norm(top_right - top_left))
        card_height = max(np.linalg.norm(top_right - bottom_right), np.linalg.norm(top_left - bottom_left))
        ratio = card_width / max(card_height, 1)
        if 1.25 <= ratio <= 2.0:
            candidates.append((area, ordered, card_width, card_height))

    if candidates:
        _area, corners, card_width, card_height = max(candidates, key=lambda item: item[0])
        target_width = 1200
        target_height = int(target_width * card_height / max(card_width, 1))
        destination = np.array([
            [0, 0], [target_width - 1, 0],
            [target_width - 1, target_height - 1], [0, target_height - 1],
        ], dtype="float32")
        transform = cv2.getPerspectiveTransform(corners, destination)
        corrected = cv2.warpPerspective(rgb, transform, (target_width, target_height))
        return Image.fromarray(corrected)

    # Fingers can hide one or more card corners in a phone photo. In that
    # case use a rotated rectangle around the largest card-sized contour.
    rectangles = []
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        rect_width, rect_height = rect[1]
        if not rect_width or not rect_height:
            continue
        aspect = max(rect_width, rect_height) / min(rect_width, rect_height)
        box_area = rect_width * rect_height
        width_share = max(rect_width, rect_height) / max(image.width, image.height)
        height_share = min(rect_width, rect_height) / min(image.width, image.height)
        if 1.30 <= aspect <= 1.95 and image_area * 0.08 <= box_area <= image_area * 0.72 and width_share >= 0.30 and height_share >= 0.12:
            rectangles.append((box_area, rect))
    if not rectangles:
        return None

    _area, rect = max(rectangles, key=lambda item: item[0])
    corners = cv2.boxPoints(rect).astype("float32")
    corners = _order_corners(corners)
    top_left, top_right, bottom_right, bottom_left = corners
    card_width = max(np.linalg.norm(bottom_right - bottom_left), np.linalg.norm(top_right - top_left))
    card_height = max(np.linalg.norm(top_right - bottom_right), np.linalg.norm(top_left - bottom_left))
    target_width = 1200
    target_height = int(target_width * card_height / max(card_width, 1))
    target_height = max(600, min(target_height, 900))
    destination = np.array([
        [0, 0], [target_width - 1, 0],
        [target_width - 1, target_height - 1], [0, target_height - 1],
    ], dtype="float32")
    transform = cv2.getPerspectiveTransform(corners, destination)
    corrected = cv2.warpPerspective(rgb, transform, (target_width, target_height))
    return Image.fromarray(corrected)


def _order_corners(points):
    import numpy as np
    result = np.zeros((4, 2), dtype="float32")
    sums = points.sum(axis=1)
    differences = np.diff(points, axis=1).reshape(-1)
    result[0] = points[np.argmin(sums)]
    result[2] = points[np.argmax(sums)]
    result[1] = points[np.argmin(differences)]
    result[3] = points[np.argmax(differences)]
    return result


def select_iin(candidates, birth_date=""):
    digit_confusions = str.maketrans({"O": "0", "o": "0", "О": "0", "о": "0", "I": "1", "l": "1", "|": "1"})
    digits_only = [re.sub(r"\D", "", item.translate(digit_confusions)) for item in candidates]
    digits_only = [item for item in digits_only if len(item) in (11, 12, 13, 14)]
    try:
        expected_prefix = datetime.strptime(birth_date, "%d.%m.%Y").strftime("%y%m%d")
    except (ValueError, TypeError):
        expected_prefix = ""

    exact = [item for item in digits_only if len(item) == 12]
    if expected_prefix:
        matched = [item for item in exact if item.startswith(expected_prefix)]
        if matched:
            return matched[0]
    if len(exact) == 1:
        return exact[0]

    # Accept an OCR window from a longer or shorter run only when it matches
    # the recognized birth date encoded at the start of the IIN.
    if expected_prefix:
        for item in digits_only:
            for start in range(max(1, len(item) - 11)):
                candidate = item[start:start + 12]
                if candidate.startswith(expected_prefix):
                    return candidate
    return ""


def read_front_iin(image_path, birth_date=""):
    """Find IIN in both common card layouts, preferably after card rectification."""
    image = Image.open(image_path).convert("RGB")
    card = _rectify_id_card(image)
    sources = [card] if card is not None else []
    sources.append(image)
    recognized = Counter()
    for source in sources:
        width, height = source.size
        if source is card:
            # Newer Kazakh IDs place the IIN on the lower left; older cards
            # place it on the lower right.
            boxes = [
                (0.05, 0.75, 0.62, 0.92),
                (0.04, 0.68, 0.66, 0.96),
                (0.65, 0.76, 0.94, 0.87),
                (0.62, 0.70, 0.98, 0.94),
            ]
        else:
            # Photos often include the desk/background. Search the lower half
            # of the image rather than assuming the card fills the frame.
            boxes = [
                (0.65, 0.76, 0.94, 0.87),
                (0.04, 0.52, 0.72, 0.72),
                (0.02, 0.35, 0.72, 0.78),
                (0.18, 0.40, 0.92, 0.80),
                (0.38, 0.40, 0.98, 0.82),
            ]
        for x1, y1, x2, y2 in boxes:
            crop = source.crop((int(width * x1), int(height * y1), int(width * x2), int(height * y2)))
            crop = ImageOps.autocontrast(crop.convert("L"), cutoff=2)
            crop = crop.filter(ImageFilter.UnsharpMask(radius=1, percent=160, threshold=2))
            enlarged = crop.resize((crop.width * 3, crop.height * 3), Image.Resampling.LANCZOS)
            for psm in (6, 11):
                raw = pytesseract.image_to_string(
                    enlarged,
                    lang="eng",
                    config=f"--psm {psm} -c tessedit_char_whitelist=0123456789",
                )
                candidates = re.findall(r"(?:\d[ \t]*){11,14}", raw)
                candidate = select_iin(candidates, birth_date)
                if candidate:
                    recognized[candidate] += 1
    return recognized.most_common(1)[0][0] if recognized else ""


def read_back_dates(image_path):
    image = Image.open(image_path).convert("L")
    width, height = image.size
    date_area = image.crop((
        int(width * 0.25), int(height * 0.45),
        int(width * 0.90), int(height * 0.65),
    ))
    date_area = ImageOps.autocontrast(date_area)
    date_area = date_area.resize(
        (date_area.width * 4, date_area.height * 4),
        Image.Resampling.LANCZOS,
    )
    return pytesseract.image_to_string(
        date_area,
        lang="eng",
        config="--psm 11 -c tessedit_char_whitelist=0123456789.",
    )
