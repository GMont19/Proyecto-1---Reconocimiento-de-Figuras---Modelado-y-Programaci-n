#BLIBLIOTECAS
import cv2
import numpy as np
#CLASES
import imagen
import figuras

"""
    Se eligió este minímo de vértices con base a los resultados obtenidos con el banco de imagenes: Exactamente en los casos donde habia 
    presencia de círculos resultaba detectar 8 vértices, pero gracias al caso de las estrellas (donde se generó un caso límite)
    se puede observar que las dimensiones de la figura juegan gran papel en su detección de vertices. Además que la dimensión del 
    circulo juega papel con su valor de circulridad. Es preferible dejar el mínimo un número abajo, no menos por si llegara haber 
    presencia de poligonos de 6 vertices
"""
# CONFIGURACIÓN DE UMBRALES PARA CLASIFICACIÓN
VERTICES_MIN_CIRC = 7
APROX_CIRCULARIDAD = 0.80
AREA_MINIMA = 10  # Filtro de ruido
"""
    Al igual que el mínimo de vertices el valor aproximado de circularidad
    se deja en este valor porque es a partir del cual el valor entraba a la 
    categoria de circulo  en el banco dieron entre 0.85 y 0.91 y no menos 
    porque habia poligonos que se acercaban (pero no alcanzaban) el valor de 0.80.
"""
APROX_CIRCULARIDAD = 0.80

def clasificar_forma(caracteristicas):
    vertices = caracteristicas["vertices"]
    circularidad = caracteristicas["circularidad"] #se hace uso de figuras.caracteristicas()
    if vertices == 3:
        return "T"
    if vertices == 4:
        return "C"
    if vertices >= VERTICES_MIN_CIRC and circularidad >= APROX_CIRCULARIDAD:
        return "O"
    return "X" #Bloque de casos donde ya se clasifican las figuras gracias a los valores calculados que devuelve figuras.caracteristicas()

"""
    Se hace una imagen de mascara completamente negra de mismas dimensiones
    con las figuras en blanco, la mascara analiza solo un valor por pixel (blanco/negro)
    Se usá .drawContour. Se le pide a cv2 que promedie el color solo donde la mascara es blanca (en las figuras)
"""
def color_promedio(imagen_bgr, contorno):
    #Calcula el color promedio en bgr (como recibe cv2) de los pixeles que estan dentro del contorno
    mascara = np.zeros(imagen_bgr.shape[:2], dtype=np.uint8)
    cv2.drawContours(mascara, [contorno], -1, color=255, thickness=cv2.FILLED)
    b, g, r, _ = cv2.mean(imagen_bgr, mask=mascara) #cv2.mean promedio de los pixeles en numeros decimales
    return (int(b), int(g), int(r)) #Se redondea haciendo uso de enteros


"""
    Va a convertir las tuplas de color BGR en cadena hexadecimal y en orden RGB (el estandar)
    {:02X} es la plantilla de formateo usada en python
    X expresa  el numero en hex en mayusculas y 02 si el resultado es menor a dos digitos
    rellena con 0 a la izquierda
"""
def color_hex(bgr):
    b, g, r = bgr
    return "#{:02X}{:02X}{:02X}".format(r, g,b) 

"""
    Función principal: Va a procesar una imagen .bmp y regresar una lista
    con el resultado por cada figura encontrada: categoria, color,
    vertices y circularidad
 
    ValueError si la ruta no corresponde a una imagen válida.
"""
def clasf_imagen(ruta):
    img = imagen.cargar(ruta)
    if img is None:
    # Verifica que la ruta sea de una imagen que pueda ser cargada al programa y si no la puede cargar, da error y marca la entrada (ruta)
        raise ValueError(f"La ruta no pertenece a una imagen valida: {ruta}")
    mascara = imagen.limpiar(imagen.segmentar(img))
    contornos = imagen.encontrar_contornos(mascara) # Se obtienen los contornos de las figuras en la mascara

    resultados = []
    for contorno in contornos:
        caracteristicas = figuras.caracteristicas(contorno)
        categoria = clasificar_forma(caracteristicas)  # Se clasifica la figura usando los valores de vertices y circularidad
        color = color_promedio(img, contorno) #obtiene el color promedio del contorno de la figura

        resultados.append({
            "categoria":categoria,
            "color": color_hex(color),
            "vertices": caracteristicas["vertices"],
            "circularidad": caracteristicas["circularidad"]
        }) #Va a guardar la información de cada figura, el color se convierte a hex usando el método color_hex

    #Se regresa la lista con la información de todas las figuraws encontradas
    return resultados
