import cv2
import glob
import os
import imagen
import figuras

for ruta in sorted(glob.glob("../bancoDeImg/*.bmp")):
    img = imagen.cargar(ruta)
    if img is None:
        print(ruta, "ERROR")
        continue

    limpia = imagen.limpiar(imagen.segmentar(img))
    contornos = imagen.encontrar_contornos(limpia)

    print(os.path.basename(ruta), "-", len(contornos), "figura(s)")
    for i, c in enumerate(contornos):
        print(f"   Figura {i}:", figuras.resumen(c))
