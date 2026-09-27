import cv2


def aproximar_contorno(contorno, precision=0.02):
    perimetro = cv2.arcLength(contorno, True)

    aproximado = cv2.approxPolyDP(
        contorno,
        precision * perimetro,
        True
    )

    return aproximado


def cantidad_vertices(contorno):
    aproximado = aproximar_contorno(contorno)
    return len(aproximado)
