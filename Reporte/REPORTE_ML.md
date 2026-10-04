# Reporte de Uso del Modelo de Lenguaje (IA)

## Prompts más Importantes

### 1. Detección de fondo arbitrario y limpieza mediante máscara binaria
* **Prompt enviado:**
  > "Tengo una imagen BMP con un fondo de color sólido arbitrario y figuras geométricas de colores sólidos. Necesito una función en Python usando OpenCV que detecte automáticamente el color del fondo, cree una máscara binaria para separar las figuras y limpie el ruido."
* **a. Motivo de uso de este tipo de herramienta:**
  En principio investigamos qué bibliotecas de Python nos servirían más para la resolución del problema y fue así que tomamos la decisión de ocupar OpenCV (`cv2`) para el procesamiento de las imágenes. Debido a esta decisión, ocupamos un modelo de lenguaje para pedirle las funciones que realmente íbamos a ocupar, para qué sirven y cómo usarlas, evitando perder tiempo leyendo la extensa documentación técnica de OpenCV.
* **b. Parte de la respuesta que aceptamos tal cual:**
  De aquí tomamos la idea de calcular la moda de los colores (el color más frecuente) mediante `np.unique` para asumir que la mayoría de los píxeles pertenecen al fondo. Además, tomamos la sugerencia de aplicar `cv2.morphologyEx` con un kernel elíptico para hacer la operación de apertura y eliminar el ruido.
* **c. Parte que corregimos o descartamos, y por qué:**
  Descartamos la idea de convertir primero a escala de grises y aplicar un umbral de Otsu (`cv2.THRESH_OTSU`), debido a que el umbral de Otsu fallaba cuando había varias figuras de distintos colores. En cambio, aplicamos el cálculo de la distancia euclidiana de color en espacio BGR de cada píxel respecto al fondo detectado, aplicando un umbral directo de tolerancia (al cual asignamos un valor de 80).

---

### 2. Clasificación de contornos y fórmula de circularidad
* **Prompt enviado:**
  > "¿Cómo puedo clasificar contornos en OpenCV para diferenciar entre triángulos, cuadriláteros, círculos y otras figuras si los círculos no siempre tienen una forma perfecta al ser procesados por `cv2.approxPolyDP`?"
* **a. Motivo de uso de este tipo de herramienta:**
  Teníamos claro que era necesario saber el número de vértices para identificar cuál tipo de figura era; sin embargo, no sabíamos cómo aplicarlo en OpenCV ni qué fórmula matemática usar para determinar qué tan circular era una figura.
* **b. Parte de la respuesta que aceptamos tal cual:**
  Nos mostró la función `cv2.approxPolyDP` para simplificar la forma y contar los vértices. También nos dio la fórmula de circularidad:
  
  $$\text{Circularidad} = \frac{4\pi \cdot \text{Área}}{\text{Perímetro}^2}$$
  
  (donde un círculo perfecto regresa un valor cercano a 1), ocupando el número $\pi$ de la librería NumPy.
* **c. Parte que corregimos o descartamos, y por qué:**
  La IA nos sugirió que si la figura tenía más de 6 vértices, de alguna manera podía expresarse como un círculo. Fue un error gravísimo que detectamos, ya que, por ejemplo, una estrella tiene 7, 8 o más vértices y no es un círculo. Modificamos esta lógica añadiendo un doble filtro: para ser un círculo los vértices mínimos serían 7 y tendría un coeficiente de circularidad mayor a 0.80.

---

### 3. Limpieza de rutas ingresadas por consola en Linux
* **Prompt enviado:**
  > "Al arrastrar una imagen a la terminal en Linux la ruta se pega con comillas simples o dobles como `'../bancoDeImg/captura_01.bmp'`. Explícame qué métodos de cadenas de Python puedo encadenar a `input()` para limpiar esos caracteres y espacios sobrantes."
* **a. Motivo de uso de este tipo de herramienta:**
  Resolver fallos que se nos presentaron en la ejecución al procesar archivos cuyas rutas contenían uno que otro espacio vacío accidental o comillas simples/dobles insertadas automáticamente.
* **b. Parte de la respuesta que aceptamos tal cual:**
  Utilizamos el encadenamiento de métodos sobre cadenas de texto `.strip().replace("'", "").replace('"', "")`.
* **c. Parte que corregimos o descartamos, y por qué:**
  También nos mencionó que podíamos importar el módulo de expresiones regulares `re` mediante el uso de `re.sub()` para limpiar los caracteres especiales, pero agregar esta nueva librería solo complicaría innecesariamente a una sola línea de código que podía resolverse con métodos estándar de cadenas en Python.

---

### 4. Estructuración y flujo de la función principal `clasf_imagen`
* **Prompt enviado:**
  > "Tengo los módulos `imagen.py` (cargar, limpiar, encontrar contornos) y `figuras.py` (resumen de categoría y color). ¿Cómo estructuro la función principal `clasf_imagen` dada una ruta de manera general para que procese la imagen paso a paso y devuelva los resultados de cada figura?"
* **a. Motivo de uso de este tipo de herramienta:**
  Buscamos un diseño de la estructura general y el flujo de datos de la función principal dentro del módulo `clasificador.py` para integrar las funciones auxiliares de limpieza, detección de contornos y análisis de color/forma desde una sola ruta de archivo.
* **b. Parte de la respuesta que aceptamos tal cual:**
  El flujo secuencial del pipeline: Cargar imagen $\rightarrow$ binarizar/limpiar $\rightarrow$ extraer contornos $\rightarrow$ iterar sobre cada contorno para analizar forma/color $\rightarrow$ retornar lista de resultados. De aquí tomamos la idea de validar inicialmente para retornar una lista vacía o lanzar un error más específico si la imagen no carga correctamente.
* **c. Parte que corregimos o descartamos, y por qué:**
  La IA proponía que la función imprimiera los resultados en pantalla directamente con `print()` dentro del propio módulo `clasificador.py`, pero esto rompía con el principio de separación de responsabilidades. Descartamos la idea y le dimos esa responsabilidad a `main.py`, mientras que `clasificador.py` solo se encargaría de procesar la lógica y regresar los resultados solicitados.

---

### 5. Estrategia de conversión a escala de grises y binarización
* **Prompt enviado:**
  > "Tengo imágenes con figuras geométricas sobre fondos de colores arbitrarios. ¿Por qué se recomienda convertir primero a escala de grises y binarizar la imagen antes de extraer los contornos con OpenCV? ¿Cómo puedo manejar la binarización si el fondo varía de color?"
* **a. Motivo de uso de este tipo de herramienta:**
  Decidimos usar la IA para que determinara la mejor estrategia de conversión y binarización para resolver el aislamiento de los contornos de la figura cuando la imagen puede tener cualquier color como fondo.
* **b. Parte de la respuesta que aceptamos tal cual:**
  Tomamos la recomendación de convertir a escala de grises (ocupando `cv2.COLOR_BGR2GRAY`) para reducir la información de 3 posibles canales a 1 solo canal de intensidad, lo que facilita el cálculo matemático de contornos. Además, tomamos el uso de `cv2.threshold` para transformar la intensidad en una imagen binaria (blanco y negro), permitiendo controlar mediante un parámetro booleano (`invertir`) si el objeto de interés o el fondo se asignan al valor 255 según el contraste relativo de la escena.
* **c. Parte que corregimos o descartamos, y por qué:**
  La IA había sugerido binarizar directamente sobre los 3 canales de color BGR utilizando un rango de color `cv2.inRange()` para cada color posible, pero decidimos que la mejor opción era convertir a escala de grises y permitir la inversión de la binarización para procesar imágenes con distintos tonos de fondo. Esto aportó una solución más generalizable sin necesidad de definir rangos fijos de color para el fondo de cada imagen.

---

### 6. Justificación de la arquitectura modular del proyecto
* **Prompt enviado:**
  > "Tengo la siguiente estructura de archivos en Python: `imagen.py` (preprocesamiento y contornos), `figuras.py` (análisis de forma y color), `clasificador.py` (función principal que une el flujo) y `main.py` (interfaz CLI). ¿Esta organización es adecuada? ¿Cuáles son sus principales ventajas frente a tener todo en un solo script?"
* **a. Motivo de uso de este tipo de herramienta:**
  Validar si la decisión de estructura del proyecto en los 4 módulos antes mencionados cumple con las buenas prácticas de diseño de software y comparar sus ventajas frente a otro tipo de estructuras.
* **b. Parte de la respuesta que aceptamos tal cual:**
  La IA subrayó que esta estructura era óptima porque cada archivo tenía una única tarea clara (preprocesamiento, análisis geométrico, orquestación y presentación). Por otra parte, enlistó algunas ventajas: permite la reutilización de código, aísla errores y facilita el trabajo colaborativo.
* **c. Parte que corregimos o descartamos, y por qué:**
  Se nos sugirió agrupar todos los módulos en un paquete reutilizable con un archivo `__init__.py` y subclases orientadas a objetos. Sin embargo, esto solo añadía una estructura más abstracta que no era necesaria. Mantener módulos planos con funciones nativas nos pareció una solución más directa, legible y fácil de mantener.

---

## Caso en que el modelo de lenguaje se equivocó o dio una solución no funcional

Al solicitar la función para extraer el color promedio de cada figura (`color_promedio`), el modelo sugirió inicialmente recortar el *Bounding Box* (caja delimitadora) de la figura con un *slice* de NumPy `imagen[y:y+h, x:x+w]` y sacarle el promedio con `np.mean()`.

Al realizar pruebas con figuras rotadas o diagonales, la caja delimitadora incluía parte del fondo dentro del área de cálculo, lo cual causaba que el color promedio calculado estuviera contaminado por el color del fondo de la imagen.

Descartamos el código sugerido y reimplementamos la función creando una **máscara binaria del contorno exacto** y calculando la media espacial únicamente en la región delimitada.

---

## Explicación del Algoritmo Implementado

### 1. `imagen.py`
* Detecta el fondo calculando cuál es el color de píxel más frecuente de la imagen.
* Calcula la diferencia euclidiana de color (en espacio BGR) de cada píxel respecto al fondo: si la diferencia supera un umbral de tolerancia $= 80$, se considera parte de una figura y pasa a ser blanco ($255$); si no, se vuelve negro ($0$).
* Usa un elemento estructurante elíptico de $3 \times 3$ para eliminar ruido mediante la operación de apertura morfológica, sin alterar la forma general de la figura.
* Detecta los límites de las formas y filtra contornos extremadamente pequeños (ruido) o extremadamente grandes (fondo).

### 2. `figuras.py`
* Simplifica el contorno y los vértices con `cv2.approxPolyDP`, suavizando bordes rugosos y reduciendo el contorno a sus vértices representativos.
* Calcula el área y el perímetro del contorno.
* Calcula el coeficiente de circularidad con la fórmula:
  $$\text{Circularidad} = \frac{4\pi \cdot \text{Área}}{\text{Perímetro}^2}$$
* Extrae la longitud de cada segmento entre vértices consecutivos y los ángulos internos.
* **Identificación de color promedio:** Genera una máscara binaria del tamaño exacto del contorno, calcula el promedio de los canales B, G y R de los píxeles de interés y convierte los valores promediados BGR al formato hexadecimal (`#RRGGBB`).

### 3. `clasificador.py`
* Clasifica cada figura en un tipo de forma:
  * **`T`**: Si tiene 3 vértices (Triángulo).
  * **`C`**: Si tiene 4 vértices (Cuadrilátero).
  * **`O`**: Si tiene 7 o más vértices y un coeficiente de circularidad mayor o igual a 0.80 (Círculo/Óvalo).
  * **`X`**: En caso de que no cumpla con ninguna de las categorías anteriores (Otra figura).

### 4. `main.py`
* Solicita al usuario la ruta de la imagen interactiva por consola.
* En caso de error o ruta inexistente, pide nuevamente la ruta en un bucle iterativo hasta recibir una válida.
* Imprime la categoría y el color en hexadecimal de cada figura procesada.
