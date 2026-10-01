"""Módulo de interfaz de usuario para la clasificación de figuras geométricas.

Este main sirve como punto de entrada de la aplicación. En primer lugar, solicita
la ruta de una imagen. En caso de que no cumpla con alguna especificación, ya sea
de formato o que no se encuentre el archivo, envía un mensaje de que algo no anda
bien y pide nuevamente la ruta cuantas veces sea necesario. Cuando se tenga por 
fin una ruta válida, verifica que haya figuras y utiliza el módulo 'clasificador'
para mostrar en consola el color y la categoría de cada figura.
"""

import os
import clasificador

def main():
    """Ejecuta el bucle principal de interacción con el usuario en consola."""
    
    # Le pide al usuario la ruta de la imagen; ocupamos el strip() y el replace() 
    # para evitar pequeños detalles del formato de entrada.
    ruta = input("Ingresar la ruta de la imagen: ").strip().replace("'", "").replace('"', "")

    # Marca error y pide la ruta, hasta que se ingrese una ruta válida.
    while not ruta or not os.path.exists(ruta):
        print("\n[ERROR] Entrada no válida o archivo no encontrado.")
        print("Formato esperado: Ruta a una imagen (.bmp)")
        ruta = input("Ingresar la ruta de la imagen: ").strip().replace("'", "").replace('"', "")

    try:
        resultados = clasificador.clasf_imagen(ruta)
        # Llama al módulo principal para clasificar todas las figuras de la imagen.

        if not resultados:
            print("No se encontraron figuras en la imagen.")
        else:
            # Muestra en consola de forma entendible cada figura procesada y sus 
            # características.
            for i, fig in enumerate(resultados):
                print(f"  Figura {i}: Color {fig['color']} | Categoría = {fig['categoria']}")

    except Exception:
        print("\n[ERROR] La imagen no cumple con el formato o especificaciones requeridas.")

if __name__ == "__main__":
    main()