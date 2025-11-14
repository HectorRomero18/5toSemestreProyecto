import cv2
import numpy as np

BAND_DILATE = 6  # Reducido para mejor rendimiento
STROKE_DILATE = 3  # Reducido para mejor rendimiento

def evaluar_trazo_por_contorno(imAux, base_canvas, modelo_gray,
                               band_dilate=BAND_DILATE, stroke_dilate=STROKE_DILATE):
    diff = cv2.absdiff(imAux, base_canvas)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, stroke_mask = cv2.threshold(diff_gray, 30, 255, cv2.THRESH_BINARY)
    if stroke_dilate > 0:
        stroke_mask = cv2.dilate(stroke_mask, np.ones((stroke_dilate, stroke_dilate), np.uint8), iterations=1)

    model_edges = cv2.Canny(modelo_gray, 50, 150)
    total_edge_pixels = cv2.countNonZero(model_edges)
    if total_edge_pixels == 0:
        return 0.0, base_canvas

    if band_dilate > 0:
        model_band = cv2.dilate(model_edges, np.ones((band_dilate, band_dilate), np.uint8), iterations=1)
    else:
        model_band = model_edges.copy()

    covered_band = cv2.bitwise_and(stroke_mask, model_band)
    covered_on_edges = cv2.bitwise_and(covered_band, model_edges)
    covered_pixels = cv2.countNonZero(covered_on_edges)

    score = (covered_pixels / total_edge_pixels) * 100.0
    score = float(np.clip(score, 0.0, 100.0))

    overlay = base_canvas.copy()
    overlay[model_edges == 255] = (0, 0, 200)
    overlay[covered_on_edges == 255] = (0, 200, 0)
    stroke_rgb = np.zeros_like(overlay)
    stroke_rgb[stroke_mask == 255] = (255, 0, 0)
    overlay = cv2.addWeighted(overlay, 0.7, stroke_rgb, 0.7, 0)

    return round(score, 2), overlay
