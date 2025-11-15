import cv2
import numpy as np

# Tus valores originales, no se tocan
BAND_DILATE = 6
STROKE_DILATE = 3

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

    # 4) PENALIZACIÓN (DISTANCIA + TRAZO FUERA)

    # -------- DISTANCIA --------
    inv_edges = cv2.bitwise_not(model_edges)
    dist_map = cv2.distanceTransform(inv_edges, cv2.DIST_L2, 5)

    stroke_pixels = np.where(stroke_mask == 255)
    dist_values = dist_map[stroke_pixels]

    if len(dist_values) == 0:
        avg_dist = 999
    else:
        avg_dist = float(np.mean(dist_values))

    # 4.1 Penalización suavizada por distancia
    if avg_dist <= 10:                 # ← Se aumentó la tolerancia a 10 px
        dist_penalty = 0
    elif avg_dist <= 25:
        dist_penalty = ((avg_dist - 10) / 15) * 10   # max 10%
    else:
        dist_penalty = min(10 + (avg_dist - 25), 30)  # crece suave

    # -------- TRAZO FUERA --------
    allowed_zone = (model_band == 255).astype(np.uint8)
    stroke_bin = (stroke_mask == 255).astype(np.uint8)

    total_stroke = np.count_nonzero(stroke_bin)

    if total_stroke == 0:
        outside_ratio = 1.0
    else:
        inside_stroke = np.count_nonzero(stroke_bin * allowed_zone)
        outside_stroke = total_stroke - inside_stroke
        outside_ratio = outside_stroke / total_stroke

    # 4.2 Penalización por trazo fuera (ahora MUCHO más tolerante)
    if outside_ratio < 0.30:                # ← antes era 0.20
        out_penalty = 0
    elif outside_ratio < 0.50:
        out_penalty = (outside_ratio - 0.30) * 30    # max ~6%
    else:
        out_penalty = min(6 + (outside_ratio - 0.50) * 60, 40)

    # -------- TOTAL PENALTY --------
    total_penalty = dist_penalty + out_penalty
    total_penalty = min(total_penalty, 80)  # límite más bajo

    final_score = base_score - total_penalty
    final_score = float(np.clip(final_score, 0.0, 100.0))

    # 5) OVERLAY
    overlay = base_canvas.copy()
    overlay[model_edges == 255] = (0, 0, 200)
    overlay[covered_on_edges == 255] = (0, 200, 0)

    stroke_rgb = np.zeros_like(overlay)
    stroke_rgb[stroke_mask == 255] = (255, 0, 0)
    overlay = cv2.addWeighted(overlay, 0.7, stroke_rgb, 0.7, 0)

    # 6) RETORNAR
    return round(final_score, 2), overlay