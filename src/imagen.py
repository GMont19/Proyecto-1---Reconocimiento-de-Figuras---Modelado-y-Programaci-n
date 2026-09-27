
import cv2
import numpy as np

def cargar(ruta):
    imagen = cv2.imread(ruta)
    return imagen


def a_gris(imagen):
       return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)


def binarizar(gris, umbral=127, invertir=True):
    
    tipo = cv2.THRESH_BINARY_INV if invertir else cv2.THRESH_BINARY
    _, binaria = cv2.threshold(gris, umbral, 255, tipo)
    return binaria


def limpiar(binaria, kernel_size=3):
    
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (kernel_size, kernel_size)
    )
    return cv2.morphologyEx(binaria, cv2.MORPH_OPEN, kernel)

def encontrar_contornos(binaria, area_minima=300, area_maxima=None):
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
    
    cv2.imshow(nombre_ventana, imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def segmentar(imagen, tolerancia=80):

    pixeles = imagen.reshape(-1, 3)

    # Color más frecuente (el fondo ocupa más píxeles que cualquier figura)
    colores, cuentas = np.unique(pixeles, axis=0, return_counts=True)
    fondo = colores[np.argmax(cuentas)].astype(np.int32)

    diff = imagen.astype(np.int32) - fondo
    distancia = np.sqrt((diff ** 2).sum(axis=2))

    mascara = np.where(distancia > tolerancia, 255, 0).astype(np.uint8)
    return mascara
