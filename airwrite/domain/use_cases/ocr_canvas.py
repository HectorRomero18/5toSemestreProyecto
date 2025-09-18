from __future__ import annotations

from typing import List, Tuple

import cv2
import numpy as np

try:
    import easyocr  # type: ignore
except Exception:  # pragma: no cover - handled at call site
    easyocr = None  # lazy requirement


def _get_or_create_reader(langs: List[str]):
    """Cache a singleton EasyOCR reader per language set to avoid cold start cost."""
    global _EASY_OCR_READERS
    key = tuple(langs)
    if '_EASY_OCR_READERS' not in globals():
        _EASY_OCR_READERS = {}
    if key not in _EASY_OCR_READERS:
        if easyocr is None:
            raise ImportError("easyocr no está instalado")
        _EASY_OCR_READERS[key] = easyocr.Reader(langs, gpu=False)
    return _EASY_OCR_READERS[key]


def _preprocess_canvas(img_bgr: np.ndarray) -> Tuple[np.ndarray, bool]:
    """
    - Toma el canvas BGR (fondo negro con trazos de color)
    - Convierte a escala de grises y binariza
    - Encuentra bounding box de píxeles no negros para recortar
    - Retorna imagen RGB recortada y si estaba vacía
    """
    if img_bgr is None:
        return img_bgr, True

    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # Umbral adaptativo para destacar trazos (que suelen ser >0 en canvas negro)
    _, bw = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

    # Si está vacío (pocos píxeles blancos)
    if int(cv2.countNonZero(bw)) < 50:
        return img_bgr, True

    # Morfología para engrosar un poco los trazos
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    bw = cv2.dilate(bw, kernel, iterations=1)

    # Bounding box
    ys, xs = np.where(bw > 0)
    y1, y2 = int(np.min(ys)), int(np.max(ys))
    x1, x2 = int(np.min(xs)), int(np.max(xs))

    # Padding
    pad = 10
    y1 = max(y1 - pad, 0)
    x1 = max(x1 - pad, 0)
    y2 = min(y2 + pad, img_bgr.shape[0] - 1)
    x2 = min(x2 + pad, img_bgr.shape[1] - 1)

    crop = img_bgr[y1:y2 + 1, x1:x2 + 1]

    # Convertir a RGB para EasyOCR y reescalar a altura razonable
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    h, w = rgb.shape[:2]
    target_h = 256
    scale = target_h / max(h, 1)
    rgb = cv2.resize(rgb, (max(int(w * scale), 1), target_h), interpolation=cv2.INTER_CUBIC)

    return rgb, False


def recognize_text_from_canvas(canvas_port, languages: List[str] | None = None) -> Tuple[str, bool]:
    """
    Reconoce texto del canvas actual.

    Retorna (texto, empty), donde empty=True indica que no hay trazos suficientes.
    """
    langs = languages or ['es', 'en']

    # Obtener canvas actual
    img = canvas_port.get()
    if img is None:
        return "", True

    pre, empty = _preprocess_canvas(img)
    if empty:
        return "", True

    reader = _get_or_create_reader(langs)
    # detail=0 devuelve solo textos reconocidos
    result: List[str] = reader.readtext(pre, detail=0, paragraph=True)

    # Unir líneas en una sola frase/palabra
    text = " ".join([s.strip() for s in result if s and s.strip()])
    return text, False