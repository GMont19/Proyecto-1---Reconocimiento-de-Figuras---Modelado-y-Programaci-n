"""Módulo de procesamiento digital de imágenes.

Da funciones para la carga, conversión de color, binarización, 
limpieza de ruido, extracción de contornos y segmentación 
mediante el uso de OpenCV y NumPy.
"""
import cv2
import numpy as np

def cargar(ruta):
    """Carga una imagen dada por el usuario usando OpenCV.

    Argumentos:
        ruta (str): Ruta relativa o absoluta del archivo.
    
    Returns:
        numpy.ndarray o None: Matriz de la imagen en especio BGR, 
        o None si no se pudo leer el archivo.
    """
    imagen = cv2.imread(ruta)
    return imagen


def a_gris(imagen):
    """Convierte una imagen BGR a escala de grises.
    
    Argumentos:
        imagen (numpy.ndarray): Imagen de entrada en formato BGR.
    
    Returns:
        numpy.ndarray: Imagen en escala de grises.
    """
    return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)


def binarizar(gris, umbral=127, invertir=True):
    """Aplica una umbralización binaria sobre una imagen en escala de grises.
    
    Argumentos:
        gris (numpy.ndarray): Imagen en escala de grises.
        umbral (int, optional): Valor de intensidad de corte (0 a 255), que por defecto es 127.
        invertir (bool, optional): Si se cumple, usa cv2.THRESH_BINARY_INV para convertir la imagen a binaria
            pero invirtiendo el resultado predeterminado.

    Returns:
        numpy.ndarray: Imagen binaria resultante.
    """
    tipo = cv2.THRESH_BINARY_INV if invertir else cv2.THRESH_BINARY
    _, binaria = cv2.threshold(gris, umbral, 255, tipo)
    return binaria


def limpiar(binaria, kernel_size=3):
    """Elimina el ruido de fondo mediante Opening.

    Argumentos:
        binaria (numpy.ndarray): Imagen binaria.
        kernel_size (int, optional): Tamaño de la ventana del elemento estructurante, por defecto 3.
    
    Returns:
        numpy.ndarray: Imagen binaria sin ruido pequeño.
    """
    # Genera un elemento estructurante de forma elíptica
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (kernel_size, kernel_size)
    )
    return cv2.morphologyEx(binaria, cv2.MORPH_OPEN, kernel)

def encontrar_contornos(binaria, area_minima=300, area_maxima=None):
    """Encuentra y filtra contornos en una imagen binaria según lpimites del área.
    
    Argumentos:
        binaria (numpy.ndarray): Imagen binaria.
        area_minima (int, optional): Área mínima para ignorar ruido, en píxeles; por defecto 300.
        area_maxima (float, optional): Área máxima para ignorar el fondo. Si esNone, considera el 90% de la imagen.
    
    Returns:
        list [numpy.ndarray]: Lista de contornos válidos que cumplen los criterios de área.
    """
    contornos, _ = cv2.findContours(
        binaria, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )
    alto, ancho = binaria.shape[:2]
    if area_maxima is None:
        area_maxima = alto * ancho * 0.9

    resultado = []
    for c in contornos:
        a = cv2.contourArea(c)
        if a < area_minima:
            continue
        if a > area_maxima:
            continue
        resultado.append(c)
    return resultado


def mostrar(nombre_ventana, imagen):
    """Muestra una imagen en una ventana emergente para pruebas.
    
    Argumentos:
        nombre_ventana (str): Título de la ventana.
        imagen (numpy.ndarray): Imagen a mostrar.
    """
    cv2.imshow(nombre_ventana, imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def segmentar(imagen, tolerancia=80):
    """Aisla las figuras del fondo.

    Calcula la moda del color BGR en la imagen para determinar el color de fondo.
    Luego, calcula la distancia euclidiana de color de cada píxel respecto al fondo
    y genera una máscara binaria basada en una tolerancia.

    Argumentos:
        imagen (numpy.ndarray): Imagen original.
        tolerancia (int, optional): Distancia euclidiana mínima para considerar un 
            píxel como parte de alguna figura, por defecto es 80.

    Returns:
        numpy.ndarray: Máscara binaria donde las figuras son blancas y el fondo negro.
    """
    # Simplifica la matriz a una lista de píxeles (N, 3)
    pixeles = imagen.reshape(-1, 3)

    # Color más frecuente (el fondo ocupa más píxeles que cualquier figura)
    colores, cuentas = np.unique(pixeles, axis=0, return_counts=True)
    fondo = colores[np.argmax(cuentas)].astype(np.int32)

    # Calcula la diferencia euclidiana entre el color en espacio BGR y el fondo
    diff = imagen.astype(np.int32) - fondo
    distancia = np.sqrt((diff ** 2).sum(axis=2))

    # Crea la máscara binaria: si la distancia supera la tolerancia, asigna 255, sino 0
    mascara = np.where(distancia > tolerancia, 255, 0).astype(np.uint8)
    return mascara
