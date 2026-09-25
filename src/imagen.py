
import cv2


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


def encontrar_contornos(binaria, area_minima=100):
    
    contornos, _ = cv2.findContours(
        binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contornos = [c for c in contornos if cv2.contourArea(c) >= area_minima]
    return contornos


def mostrar(nombre_ventana, imagen):
    
    cv2.imshow(nombre_ventana, imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
