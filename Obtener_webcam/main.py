import cv2

#captura = cv2.VideoCapture(0)						# Capturar desde las webcam
captura = cv2.VideoCapture('video_salida.avi')		# Para mostrar un video
#salida = cv2.VideoWriter('video_salida.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (640, 480))
while captura.isOpened():
	ret, imagen = captura.read()
	if ret: 
		cv2.imshow('Video', imagen)
		#salida.write(imagen)
		if cv2.waitKey(1) & 0xFF == ord('q'): break	# Salida del programa
	else: break

captura.release()
#salida.release()
cv2.destroyAllWindows()