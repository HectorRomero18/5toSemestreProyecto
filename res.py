import matplotlib.pyplot as plt

# Coordenadas de la letra A
""" Estas coordenadas son las del punto de la letra A en /resultado/letraA.json"""
coords = [
    [261, 387], [238, 386], [283, 383], [215, 382], [389, 386], [305, 376], [194, 374],
    [325, 365], [174, 364], [390, 364], [343, 352], [156, 349], [389, 340], [359, 335],
    [140, 332], [389, 318], [128, 313], [371, 316], [389, 294], [119, 292], [390, 272],
    [114, 270], [389, 249], [113, 247], [389, 225], [115, 224], [389, 202], [120, 202],
    [375, 190], [361, 187], [374, 175], [368, 173], [130, 181], [389, 179], [142, 162],
    [358, 161], [389, 157], [346, 148], [159, 146], [328, 133], [389, 137], [177, 132],
    [399, 112], [380, 111], [308, 123], [197, 121], [390, 121], [379, 110], [287, 115],
    [219, 114], [264, 110], [241, 110], [389, 111]
]

# Separar en listas de x e y
x_vals = [pt[0] for pt in coords]
y_vals = [pt[1] for pt in coords]

# Graficar
plt.figure(figsize=(6, 8))
plt.scatter(x_vals, y_vals, color="green")
plt.gca().invert_yaxis()  # Invertir eje Y para que coincida con coordenadas de imagen
plt.title("Puntos detectados en la letra A")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.tight_layout()
plt.show()
