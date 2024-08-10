import cv2
import numpy as np

cap = cv2.VideoCapture(0)
bg = None

# Rango de tonalidades para amarillo
amarilloBajo = np.array([15, 100, 20], np.uint8)
amarilloAlto = np.array([45, 255, 255], np.uint8)

while True:
	ret, frame = cap.read()
	if ret == False: break

	if bg is None: bg = frame

	frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	maskAmarillo = cv2.inRange(frameHSV, amarilloBajo, amarilloAlto)
	
	mask = cv2.medianBlur(maskAmarillo, 13)			# Aplicar un desenfoque
	kernel = np.ones((5, 5), np.uint8)
	mask = cv2.dilate(mask, kernel, iterations=2)	# Entender los bordes
	areaColor = cv2.bitwise_and(bg, bg, mask=mask) 	# Diferencia entre imagen y mascara de color
	maskInv = cv2.bitwise_not(mask) 				# Invertir lo anterior
	sinAreaColor = cv2.bitwise_and(frame, frame, mask=maskInv) 	# Obtener el resto del area
	finalFrame = cv2.addWeighted(areaColor, 1, sinAreaColor, 1, 0)	# 
	cv2.imshow('Frame', frame)
	#cv2.imshow('mask', mask)
	#cv2.imshow('areaColor', areaColor)
	#cv2.imshow('maskInv',maskInv)
	#cv2.imshow('sinAreaColor',sinAreaColor)
	cv2.imshow('finalFrame', finalFrame)
	if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()