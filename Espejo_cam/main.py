import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
	ret, frame = cap.read()
	if ret == False: break
	#print('frame.shape=', frame.shape)
	anchoMitad = frame.shape[1] // 2 		# Dividir el ancho de la imagen en 2 (con abs)
	# Voltear imagen y unir al otro trozo
	frame[:,:anchoMitad] = cv2.flip(frame[:, anchoMitad:], 1) 
	cv2.imshow('Frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()