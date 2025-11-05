import matplotlib.pyplot as plt

# Coordenadas de la letra A
""" Estas coordenadas son las del punto de la letra A en /resultado/letraA.json"""
coords = [
    [348, 386], [326, 386], [304, 386], [282, 386], [260, 386], [238, 386], [216, 386], [194, 386], [174, 386], [370, 385], [141, 377], [158, 352], [174, 335], [188, 317], [204, 300], [218, 283], [234, 266], [249, 248], [264, 231], [279, 214], [294, 197], [309, 180], [232, 173], [324, 162], [337, 148], [358, 135], [364, 128], [344, 131], [350, 122], [345, 123], [348, 112], [122, 116], [118, 113], [128, 116], [131, 115], [126, 102], [326, 111], [304, 111], [282, 111], [260, 111], [172, 111], [238, 111], [216, 110], [194, 111], [140, 108], [152, 110], [369, 111]
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
