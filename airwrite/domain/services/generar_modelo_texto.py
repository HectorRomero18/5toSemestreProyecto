import cv2
import numpy as np

def generar_modelo_texto(size, texto):
    h, w = size
    img = np.zeros((h, w), dtype=np.uint8)
    length = len(texto)
    base_scale = max(5.0, h / 60.0)
    scale = base_scale * (1.0 if length <= 2 else 0.8)
    thickness = int(max(12, h // 30))
    (tw, th), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, scale, thickness)
    x = max(10, (w - tw) // 2)
    y = int(h * 0.75)
    cv2.putText(img, texto, (x, y), cv2.FONT_HERSHEY_SIMPLEX, scale, 255, thickness, cv2.LINE_AA)
    return img
