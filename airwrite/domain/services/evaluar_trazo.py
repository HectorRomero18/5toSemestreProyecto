import cv2
import numpy as np

# Tus valores originales, no se tocan
BAND_DILATE = 10
STROKE_DILATE = 8

def evaluar_trazo_por_contorno(imAux, base_canvas, modelo_gray,
                               band_dilate=BAND_DILATE, stroke_dilate=STROKE_DILATE):

    # 1) EXTRAER EL TRAZO (stroke_mask)
    diff = cv2.absdiff(imAux, base_canvas)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, stroke_mask = cv2.threshold(diff_gray, 30, 255, cv2.THRESH_BINARY)

    if stroke_dilate > 0:
        stroke_mask = cv2.dilate(
            stroke_mask,
            np.ones((stroke_dilate, stroke_dilate), np.uint8),
            iterations=1
        )

    if cv2.countNonZero(stroke_mask) == 0:
        return 0.0, imAux.copy()

    # 2) CONTORNO DEL MODELO
    model_edges = cv2.Canny(modelo_gray, 50, 150)
    total_edge_pixels = cv2.countNonZero(model_edges)

    if total_edge_pixels == 0:
        return 0.0, imAux.copy()

    # 3) COBERTURA SOBRE BANDA
    if band_dilate > 0:
        model_band = cv2.dilate(
            model_edges,
            np.ones((band_dilate, band_dilate), np.uint8),
            iterations=1
        )
    else:
        model_band = model_edges.copy()

    covered_band = cv2.bitwise_and(stroke_mask, model_band)
    covered_on_edges = cv2.bitwise_and(covered_band, model_edges)

    covered_pixels = cv2.countNonZero(covered_on_edges)

    base_score = (covered_pixels / total_edge_pixels) * 100.0
    base_score = float(np.clip(base_score, 0.0, 100.0))

      # 4) PENALIZACIÓN ÚNICA: TRAZO FUERA (GRADUAL)
    allowed_zone = (model_band == 255).astype(np.uint8)
    stroke_bin   = (stroke_mask == 255).astype(np.uint8)

    total_stroke = np.count_nonzero(stroke_bin)

    if total_stroke == 0:
        outside_ratio = 1.0
    else:
        inside_stroke  = np.count_nonzero(stroke_bin * allowed_zone)
        outside_stroke = total_stroke - inside_stroke
        outside_ratio  = outside_stroke / total_stroke

    # Modo estándar: gradual, equilibrado
    if outside_ratio < 0.35:
        out_penalty = 0
    elif outside_ratio < 0.60:
        out_penalty = (outside_ratio - 0.35) * (25 / 0.25)
    else:
        out_penalty = 25 + (outside_ratio - 0.60) * (75 / 0.40)  # máx 45%

    # 5) PUNTUACIÓN FINAL
    final_score = base_score - out_penalty
    final_score = float(np.clip(final_score, 0.0, 100.0))

    # 6) OVERLAY
    overlay = base_canvas.copy()
    overlay[model_edges == 255] = (0, 0, 200)
    overlay[covered_on_edges == 255] = (0, 200, 0)

    stroke_rgb = np.zeros_like(overlay)
    stroke_rgb[stroke_mask == 255] = (255, 0, 0)
    overlay = cv2.addWeighted(overlay, 0.7, stroke_rgb, 0.7, 0)

    # 6) RETORNAR
    return round(final_score, 2), overlay