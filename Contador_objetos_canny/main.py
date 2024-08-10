import cv2

imagen = cv2.imread('objetos.png')
grises = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
bordes = cv2.Canny(grises, 100, 200)
cnts, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(imagen, cnts, -1, (255, 0, 0), 2) # Mostrar todos los contornos a la vez

print('Número de objetos: ', len(cnts))

cv2.imshow('imagen', imagen) # Para mostrar la imagen contrastada
cv2.imshow('bordes', bordes) # Para mostrar la imagen contrastada
cv2.waitKey(0)
cv2.destroyAllWindows()
