import cv2
import numpy as np

def dibujar_contorno(contorno, color):
	for (i, c) in enumerate(contorno):
		M = cv2.moments(c)				# Obtener las coordenadas del centro
		if (M['m00']==0): M['m00'] = 1 	# Para evitar división 0
		x = int(M['m10']/M['m00'])
		y = int(M['m01']/M['m00'])
		cv2.drawContours(imagen, [c], 0, color, 2)
		cv2.putText(imagen, str(i+1), (x-10, y-10), font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

# Rango de tonalidades para amarillo
amarilloBajo = np.array([15, 100, 20], np.uint8)
amarilloAlto = np.array([45, 255, 255], np.uint8)

# Rango de tonalidades para azul
azulBajo = np.array([100, 100, 20], np.uint8)
azulAlto = np.array([125, 255, 255], np.uint8)

# Rango de tonalidades para verde
verdeBajo = np.array([36, 100, 20], np.uint8)
verdeAlto = np.array([70, 255, 255], np.uint8)

# Rango de tonalidades para rojo
redBajo1 = np.array([0, 100, 20], np.uint8)
redAlto1 = np.array([5, 255, 255], np.uint8)
redBajo2 = np.array([175, 100, 20], np.uint8)
redAlto2 = np.array([179, 255, 255], np.uint8)

imagen = cv2.imread('lunares.png')
imagenHSV = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Fuente del texto a mostrar
font = cv2.FONT_HERSHEY_SIMPLEX

# Crear mascaras por color
maskAmarillo = cv2.inRange(imagenHSV, amarilloBajo, amarilloAlto)
maskAzul = cv2.inRange(imagenHSV, azulBajo, azulAlto)
maskVerde = cv2.inRange(imagenHSV, verdeBajo, verdeAlto)
maskRed1 = cv2.inRange(imagenHSV, redBajo1, redAlto1)
maskRed2 = cv2.inRange(imagenHSV, redBajo2, redAlto2)
maskRojo = cv2.add(maskRed1, maskRed2)

# Obtener los contornos de cada color
contornosAmarillo, _ = cv2.findContours(maskAmarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contornosAzul, _ = cv2.findContours(maskAzul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contornosVerde, _ = cv2.findContours(maskVerde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contornosRojo, _ = cv2.findContours(maskRojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar los contornos de cada color
dibujar_contorno(contornosAmarillo, (0, 255, 255))
dibujar_contorno(contornosAzul, (140, 40, 120))
dibujar_contorno(contornosVerde, (0, 255, 0))
dibujar_contorno(contornosRojo, (0, 0, 255))

# Crear una imagen de resumen de colores
imgResumen = 255 * np.ones((210, 100, 3), dtype=np.uint8)
cv2.circle(imgResumen, (30, 30), 15, (0, 255, 255), -1)
cv2.circle(imgResumen, (30, 70), 15, (140, 40, 120), -1)
cv2.circle(imgResumen, (30, 110), 15, (0, 255, 0), -1)
cv2.circle(imgResumen, (30, 150), 15, (0, 0, 255), -1)
cv2.putText(imgResumen, str(len(contornosAmarillo)), (65, 40), 1, 2, (0, 0, 0), 2)
cv2.putText(imgResumen, str(len(contornosAzul)), (65, 80), 1, 2, (0, 0, 0), 2)
cv2.putText(imgResumen, str(len(contornosVerde)), (65, 120), 1, 2, (0, 0, 0), 2)
cv2.putText(imgResumen, str(len(contornosRojo)), (65, 160), 1, 2, (0, 0, 0), 2)
total = len(contornosAmarillo) + len(contornosAzul) + len(contornosVerde) + len(contornosRojo)
cv2.putText(imgResumen, str(total), (55, 200), 1, 2, (0, 0, 0), 2)

cv2.imshow('Resumen', imgResumen)
cv2.imshow('imagen', imagen)
#cv2.imshow('maskAmarillo', maskAmarillo)

cv2.waitKey(0)
cv2.destroyAllWindows()