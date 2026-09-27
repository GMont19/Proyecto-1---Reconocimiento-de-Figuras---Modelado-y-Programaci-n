#BLIBLIOTECAS
import cv2
import numpy as np
#CLASES
import imagen
import figuras

VERTICES_MIN_CIRC = 7
"""
Se eligió este minímo de vértices con base a los resultados obtenidos con el banco de imagenes: Exactamente en los casos donde habia 
presencia de círculos resultaba detectar 8 vértices, pero gracias al caso de las estrellas (donde se generó un caso límite)
se puede observar que las dimensiones de la figura juegan gran papel en su detección de vertices. Además que la dimensión del 
circulo juega papel con su valor de circulridad. Es preferible dejar el mínimo un número abajo, no menos por si llegara haber 
presencia de poligonos de 6 vertices
"""
UMBRAL_CIRCULARIDAD = 0.80
"""
Al igual qye el mínimo de vertices el umbral se deja en este valor 
porque es a partir del cual el valor entraba a la categoria de circulo 
en el banco dieron entre 0.85 y 0.91 y no menos porque habia 
poligonos que se acercaban (pero no alcanzaban) el valor de 0.80.
"""

def clasificar_forma(caracteristicas):
    vertices = caracteristicas["vertices"]
    circularidad = caracteristicas["circularidad"]
    #se hace uso de figuras.caracteristicas()
    if vertices == 3:
        return "T"
    if vertices == 4:
        return "C"
    if vertices >= VERTICES_MIN_CIRC and circularidad >= UMBRAL_CIRCULARIDAD:
        return "O"
    return "X"
    #Aquí ya se clasifican las figuras gracias a los valores calculados que devuelve figuras.caracteristicas()

def color_promedio(imagen_bgr, contorno):
    #Calcula el color promedio en bgr (como recibe cv2)
    #de los pixeles que estan dentro del contorno
    mascara = np.zeros(imagen_bgr.shape[:2], dtype=np.uint8)
    """
    Se hace una imagen de mascara completamente negra de mismas dimensiones
    con las figuras en blanco, la mascara analiza solo un valor por pixel (blanco/negro)
    Se usá .drawContour. Se le pide a cv2 que promedie el color solo donde la mascara es blanca (en las figuras)
    """
    cv2.drawContours(mascara, [contorno], -1, color=255, thickness=cv2.FILLED)
    b, g, r, _ = cv2.mean(imagen_bgr, mask=mascara) #cv2.mean promedio de los pixeles en numeros decimales
    return (int(b), int(g), int(r)) #Se redondea haciendo uso de enteros

#Va a convertir las tuplas de color BGR en cadena hexadecimal y en orden RGB (el estandar)
"""
"{:02X} es la plantilla de formateo usada en python"
X expresa  el numero en hex en mayusculas y 02 si el resultado es menor a dos digitos
rellena con 0 a la izquierda
"""
def color_hex(bgr):
    b, g, r = bgr
    return "#{:02X}{:02X}{:02X}".format(r, g,b) 
