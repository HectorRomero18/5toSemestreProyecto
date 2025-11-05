import cv2
import numpy as np
import json
import os

# --- Carpeta con imágenes ---
folder = "media/letras"
output_folder = "resultados"
os.makedirs(output_folder, exist_ok=True)

# --- Configurar detector de blobs ---
params = cv2.SimpleBlobDetector_Params()
params.filterByArea = True
params.minArea = 0.5
params.maxArea = 10000
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = False
params.filterByColor = True
params.blobColor = 0

ver = (cv2.__version__).split('.')
detector = cv2.SimpleBlobDetector_create(params) if int(ver[0]) >= 3 else cv2.SimpleBlobDetector(params)

# --- Procesar cada imagen PNG ---
for filename in os.listdir(folder):
    if filename.lower().endswith(".png"):
        path = os.path.join(folder, filename)
        print(f"Procesando: {filename}")

        # --- Cargar e invertir imagen ---
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        img_inv = cv2.bitwise_not(img)

        # --- Preprocesamiento ---
        img_blur = cv2.GaussianBlur(img_inv, (5, 5), 0)
        _, thresh = cv2.threshold(img_blur, 127, 255, cv2.THRESH_BINARY)

        # --- Detectar blobs ---
        keypoints = detector.detect(thresh)
        print(f"{len(keypoints)} puntos detectados")

        # --- Dibujar resultados ---
        img_result = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        coords = []
        for i, kp in enumerate(keypoints):
            x, y = int(kp.pt[0]), int(kp.pt[1])
            r = int(kp.size / 2)
            coords.append((x, y))
            cv2.circle(img_result, (x, y), r, (0, 255, 0), 2)
            cv2.putText(img_result, str(i+1), (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

        # --- Guardar coordenadas en JSON ---
        json_name = os.path.splitext(filename)[0] + ".json"
        json_path = os.path.join(output_folder, json_name)
        with open(json_path, "w") as f:
            json.dump(coords, f)

        # --- Guardar imagen con puntos dibujados ---
        result_img_name = os.path.splitext(filename)[0] + "_puntos.png"
        result_img_path = os.path.join(output_folder, result_img_name)
        cv2.imwrite(os.path.join(output_folder, f"{filename}_binaria.png"), thresh)
        cv2.imwrite(result_img_path, img_result)

print("Procesamiento completo. Resultados guardados en:", output_folder)
