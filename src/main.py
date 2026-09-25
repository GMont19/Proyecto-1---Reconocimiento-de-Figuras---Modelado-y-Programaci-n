import cv2

imagen = cv2.imread("../bancoDeImg/captura_01.bmp")

if imagen is None:
    print("Error: no se pudo abrir la imagen")
else:
    print("Imagen cargada correctamente")
    print("Tamaño:", imagen.shape)
