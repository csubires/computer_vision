import cv2
import numpy as np

video = cv2.VideoCapture(0)
i = 0
while True:
	ret, frame = video.read()
	if ret == False: break
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 	# Transformar a escala de grises
	
	if i == 20:		# Dejar 20 frames para estabilizar la capturar en el fondo
		bgGray = gray
	if i > 20: 
		# Diferencia entre la imagen actual y la de 20 frames atrás
		dif = cv2.absdiff(gray, bgGray) 
		# Pasar la diferencia a blanco y negro
		_, th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY) 
		# Encontrar los contornos
		cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cv2.imshow('th', th)
		# Dibujar un rectangulo con el contorno
		for c in cnts:
			area = cv2.contourArea(c)
			if area > 9000: # Para movimientos muy grandes
				x, y , w, h = cv2.boundingRect(c)
				cv2.rectangle(frame, (x-10, y-10), (x+w, y+h), (0, 255, 0), 2)
				
	cv2.imshow('Frame', frame)
	i = i + 1
	if cv2.waitKey(1) & 0xFF == ord('q'): break
video.release()
cv2.destroyAllWindows()