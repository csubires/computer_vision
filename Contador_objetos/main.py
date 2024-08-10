import cv2

imagen = cv2.imread('monedas.jpg')
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
_, th = cv2.threshold(grises, 240, 255, cv2.THRESH_BINARY_INV)
cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# cv2.drawContours(imagen, cnts, -1, (255, 0, 0), 1) # Mostrar todos los contornos a la vez
# cv2.imshow('Imagen', imagen)

print('Número de objetos: ', len(cnts))

# Fuente del texto a mostrar
font = cv2.FONT_HERSHEY_SIMPLEX
i = 0
for c in cnts:
	M = cv2.moments(c)
	if (M['m00']==0): M['m00'] = 1 	# Para evitar división 0
	x = int(M['m10']/M['m00'])
	y = int(M['m01']/M['m00'])
	
	mensaje = str(i+1)
	#nuevoContorno = cv2.convexHull(c)
	cv2.putText(imagen, mensaje, (x-40, y), font, 0.75, (0, 255, 0), 2, cv2.LINE_AA)
	cv2.drawContours(imagen, [c], 0, (255, 0, 0), 2)
	cv2.imshow('Imagen', imagen)
	#cv2.waitKey(0)
	i = i + 1

# cv2.imshow('th', th) # Para mostrar la imagen contrastada
cv2.waitKey(0)
cv2.destroyAllWindows()

# TODO Si la imagen no es nítida, el conteo se hará mal, reducir redundancia