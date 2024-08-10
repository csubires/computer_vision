import cv2
import numpy as np

# Buscar el target en una imagen
def points_target_matching(image, target):
	points = [] 		# Donde se guardan los puntes de rectangulos finales
	threshold = 0.9 	# Umbral, límite
	res = cv2.matchTemplate(image, target, cv2.TM_CCOEFF_NORMED) # Lo máximo es 1
	
	candidates = np.where(res >= threshold)
	candidates = np.column_stack([candidates[1], candidates[0]]) # x, y
	
	points.append(candidates[0]) # Meter el primer punto como valido
	i=0
	while len(candidates) > 0:
		to_delete = []
		for j in range(0, len(candidates)):
			diff = points[i-1]-candidates[j] 
			# Si la diferncia entre uno y el siguiente es menor de 10, borrarlo
			if abs(diff[0]) < 10 and abs(diff[1]) < 10: to_delete.append(j)

		candidates = np.delete(candidates, to_delete, axis=0)
		if len(candidates) == 0: break
		points.append(candidates[0])
		i+=1
	return points or False

img_rgb = cv2.imread('1.jpg')							# Leer imagen original
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)	# Pasar imagen en escala de grises

target = cv2.imread('template.jpg', 0) 					# Leer objeto a buscar en escala de grises (0)
point_res = points_target_matching(img_gray, target)	# Buscar objeto

target_inv = cv2.flip(target, -1) 						# Invertir objeto a buscar
point_inv = points_target_matching(img_gray, target_inv)

# Si se ha encontrado el objeto y su invertido, unir en un solo resultado
point_res = np.concatenate((point_res, point_inv)) if point_inv else point_res

# Dibujar los rectangulo sobre la imagen original
for point in point_res:
	x1, y1 = point[0], point[1]
	x2, y2 = point[0] + target.shape[1], point[1] + target.shape[0]
	cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.putText(img_rgb, '#: ' + str(len(point_res)), (20, 20), 1, 1.0, (0, 0, 0), 1)
cv2.imshow("Image", img_rgb)	# Mostrar imagen con los recuadros
cv2.waitKey(0)					# Esperar a que se cierre la ventana [X]
#cv2.destroyAllWindow() 			# Cerrar todas las ventanas