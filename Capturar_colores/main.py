import cv2
import numpy as np

# Colorear el perfil de un color
def dibujar(mask, color):
	contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	for c in contornos:
		area = cv2.contourArea(c)
		if area > 3000:			# Eliminar contornos ruido
			x, y, w, h = cv2.boundingRect(c)
			
			if color == (255, 0, 0):
				cv2.rectangle(frame, (x, y), (x+w, y+h), color, 3)
				cv2.line(frame, (x,y), (x+w, y+h), color, 3)
				cv2.line(frame, (x+w, y), (x, y+h), color, 3)
				cv2.putText(frame, 'Azul', (x-10, y-10), font, 0.75, color, 2, cv2.LINE_AA)
			
			if color != (255, 0, 0):
				# Obtener las coordenadas del centro del objeto
				M = cv2.moments(c)
				if (M['m00']==0): M['m00']=1 	# Para evitar división 0
				xcentro = int(M['m10']/M['m00'])
				ycentro = int(M['m01']/M['m00'])
				radio = xcentro-x
				
				cv2.circle(frame, (xcentro, ycentro), radio, color, 3) # Radio 7
				cv2.putText(frame, '{},{}'.format(xcentro, ycentro), (xcentro+10, ycentro), font, 0.75, (0, 255, 0))
				# Suavizar contornos
				#nuevoContorno = cv2.convexHull(c)
				# Dibujar el contorno del color apropiado
				#cv2.drawContours(frame, [nuevoContorno], 0, color, 2)

# Capturar la imagen de la webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Rango de tonalidades para azul
azulBajo = np.array([100, 100, 20], np.uint8)
azulAlto = np.array([125, 255, 255], np.uint8)

# Rango de tonalidades para amarillo
amarilloBajo = np.array([15, 100, 20], np.uint8)
amarilloAlto = np.array([45, 255, 255], np.uint8)

# Rango de tonalidades para rojo
redBajo1 = np.array([0, 100, 20], np.uint8)
redAlto1 = np.array([5, 255, 255], np.uint8)
redBajo2 = np.array([175, 100, 20], np.uint8)
redAlto2 = np.array([179, 255, 255], np.uint8)

# Fuente del texto a mostrar
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
	ret, frame = cap.read()
	
	if ret == True:
		# Convertir de BGR(nativo cv2) a HSV
		frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		# Crear las mascaras de colores
		maskAzul = cv2.inRange(frameHSV, azulBajo, azulAlto)
		maskAmarillo = cv2.inRange(frameHSV, amarilloBajo, amarilloAlto)
		maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)
		maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)
		maskRed = cv2.add(maskRed1, maskRed2)
		# Detectar y dibujar los contornos
		dibujar(maskAzul, (255, 0, 0))
		dibujar(maskAmarillo, (0, 255, 255))
		dibujar(maskRed, (0, 0, 255))
		# Mostrar imagen
		cv2.imshow('frame', frame)
		# Condición de salida
		if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()