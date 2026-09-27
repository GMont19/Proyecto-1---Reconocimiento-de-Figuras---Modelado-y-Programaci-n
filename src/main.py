import imagenes
import figuras


imagenes = imagen.cargar("../bancoDeImg/captura_01.bmp")

gris = imagen.a_gris(imagenes)
binaria = imagen.binarizar(gris)
limpia = imagen.limpiar(binaria)

contornos = imagen.encontrar_contornos(limpia)

print("Contornos encontrados:", len(contornos))

for contorno in contornos:
    vertices = figuras.cantidad_vertices(contorno)
    print("Vértices:", vertices)

