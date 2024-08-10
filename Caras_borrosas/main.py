import cv2

def nothing(x): pass

image = cv2.imread('oficina.png')
faceClassif = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cv2.namedWindow('Imagen')
cv2.createTrackbar('Blur', 'Imagen', 0, 30, nothing)
cv2.createTrackbar('Gray', 'Imagen', 0, 1, nothing)

while True:
	val = cv2.getTrackbarPos('Blur', 'Imagen')
	grayVal = cv2.getTrackbarPos('Gray', 'Imagen')
	
	if grayVal == 1: imageN = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
	else: imageN = image.copy()
	faces = faceClassif.detectMultiScale(image.copy(), 1.2, 5)
	
	for (x, y, w, h) in faces:
		if val > 0: imageN[y:y+h, x:x+w] = cv2.blur(imageN[y:y+h, x:x+w], (val, val))
	cv2.imshow('imageN', imageN)
	if cv2.waitKey(1) & 0xFF == ord('q'): break

cv2.destroyAllWindows()
