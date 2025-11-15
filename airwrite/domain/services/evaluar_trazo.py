import cv2
import numpy as np

BAND_DILATE = 6  # Reducido para mejor rendimiento
STROKE_DILATE = 3  # Reducido para mejor rendimiento

def evaluar_trazo_por_contorno(imAux, base_canvas, modelo_gray,
                               band_dilate=BAND_DILATE, stroke_dilate=STROKE_DILATE):

    # ============================================================
    # 1) EXTRAER EL TRAZO (stroke_mask)
    # ============================================================
    diff = cv2.absdiff(imAux, base_canvas)
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, stroke_mask = cv2.threshold(diff_gray, 30, 255, cv2.THRESH_BINARY)

    if stroke_dilate > 0:
        stroke_mask = cv2.dilate(
            stroke_mask,
            np.ones((stroke_dilate, stroke_dilate), np.uint8),
            iterations=1
        )

    # Si no hay trazo, retornamos 0%
    if cv2.countNonZero(stroke_mask) == 0:
        return 0.0, imAux.copy()

    # ============================================================
    # 2) CONTORNO DEL MODELO (bordes reales de la letra)
    # ============================================================
    model_edges = cv2.Canny(modelo_gray, 50, 150)
    total_edge_pixels = cv2.countNonZero(model_edges)

    if total_edge_pixels == 0:
        return 0.0, imAux.copy()

    # ============================================================
    # 3) COBERTURA SOBRE BANDA (parte positiva del score)
    # ============================================================
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

    # ============================================================
    # 4) PENALIZACIÓN INTELIGENTE POR DISTANCIA REAL AL MODELO
    # ============================================================

    # Invertir los bordes para crear el mapa de distancia
    inv_edges = cv2.bitwise_not(model_edges)

    # distanceTransform: cada pixel tiene distancia al borde más cercano
    dist_map = cv2.distanceTransform(inv_edges, cv2.DIST_L2, 5)

    stroke_pixels = np.where(stroke_mask == 255)
    dist_values = dist_map[stroke_pixels]

    if len(dist_values) == 0:
        avg_dist = 100  # trazo fuera de todo
    else:
        avg_dist = float(np.mean(dist_values))

    # LOGICA DE PENALIZACIÓN SUAVE
    # 0–5 px  → sin penalización
    # 5–20 px → penalización progresiva (máx 10%)
    # +20 px  → penalización fuerte pero limitada (máx 20%)
    if avg_dist <= 5:
        distance_penalty = 0
    elif avg_dist <= 20:
        distance_penalty = ((avg_dist - 5) / 15) * 10
    else:
        distance_penalty = 10 + min((avg_dist - 20) * 0.2, 10)  # Máx total = 20%

    # Penalización final controlada
    final_score = base_score - distance_penalty
    final_score = float(np.clip(final_score, 0.0, 100.0))

    # ============================================================
    # 5) GENERAR OVERLAY PARA DEBUG VISUAL
    # ============================================================
    overlay = base_canvas.copy()

    # Bordes del modelo (rojo)
    overlay[model_edges == 255] = (0, 0, 200)

    # Parte del trazo que cubre correctamente (verde)
    overlay[covered_on_edges == 255] = (0, 200, 0)

    # Trazo completo (azul)
    stroke_rgb = np.zeros_like(overlay)
    stroke_rgb[stroke_mask == 255] = (255, 0, 0)

    overlay = cv2.addWeighted(overlay, 0.7, stroke_rgb, 0.7, 0)

    # ============================================================
    # 6) RETORNAR SCORE FINAL + OVERLAY
    # ============================================================
    return round(final_score, 2), overlay