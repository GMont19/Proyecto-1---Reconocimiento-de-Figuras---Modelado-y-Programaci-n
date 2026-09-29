
import glob
import os
import imagen
import figuras
import clasificador

#Le pide al usuario la ruta de la imagen ocupamos el strip y el replace para evitar pequeños detalles del formato de entrada.
ruta = input("Ingresar la ruta de la imagen: ").strip().replace("'", "").replace('"', "")

# Marca error y pide la ruta, hasta que se ingrese una ruta válida.
while not ruta or not os.path.exists(ruta):
    print("\n[ERROR] Entrada no válida o archivo no encontrado.")
    print("Formato esperado: Ruta a una imagen (.bmp)")
    ruta = input("Ingresar la ruta de la imagen: ").strip().replace("'", "").replace('"', "")

try:
    resultados = clasificador.clasf_imagen(ruta)

    if not resultados:
        print("No se encontraron figuras en la imagen.")
    else:
        for i, fig in enumerate(resultados):
            print(f"  Figura {i}: Color {fig['color']} | Categoría = {fig['categoria']}")

except Exception:
    print("\n[ERROR] La imagen no cumple con el formato o especificaciones requeridas.")
            
