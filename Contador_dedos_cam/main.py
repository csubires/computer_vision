import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
bg = None

# Colores para la visualización
color_start = (204, 204, 0)
color_end = (204, 0, 204)
color_far = (255, 0, 0)

color_start_far = (204, 204, 0)
color_far_end = (204, 0, 204)
color_start_end = (0, 255, 255)

color_contorno = (0, 255, 0)
color_ymin = (0, 130, 255)
color_angulo = (0, 255, 255)
color_d = (0, 255, 255)
color_fingers = (0, 255, 255)

while True:
	ret, frame = cap.read()
	if ret == False: break
	
	#frame = imutils.resize(frame, width=640)
	frame = cv2.flip(frame, 1)
	frameAux = frame.copy()
	
	if bg is not None:
		ROI = frame[50:300, 380:600]
		cv2.rectangle(frame, (380-2, 50-2), (600+2, 300+2), color_fingers, 1)
		grayROI = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
		
		bgROI = bg[50:300, 380:600]
		#cv2.imshow('grayROI', grayROI)
		
		dif = cv2.absdiff(grayROI, bgROI)
		_, th = cv2.threshold(dif, 30, 255, cv2.THRESH_BINARY)
		th = cv2.medianBlur(th, 7)
		cv2.imshow('th', th)
		
		cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]
		
		for cnt in cnts:
			M = cv2.moments(cnt)
			if M['m00']==0: M['m00'] = 1
			x = int(M['m10']/M['m00'])
			y = int(M['m01']/M['m00'])
			cv2.circle(ROI, (x, y), 5, (0, 255, 0), -1)
			
			ymin = cnt.min(axis=1)
			cv2.circle(ROI, tuple(ymin[0]), 5, color_ymin, -1)
			
			hull1 = cv2.convexHull(cnt)
			cv2.drawContours(ROI, [hull1], 0, color_contorno, 2)
			
			hull2 = cv2.convexHull(cnt, returnPoints=False)
			defects = cv2.convexityDefects(cnt, hull2)
			
			if defects is not None:
				inicio = []
				fin = []
				fingers = 0
				
				for i in range(defects.shape[0]):
					s, e, f, d = defects[i, 0]
					start = cnt[s][0]
					end = cnt[e][0]
					far = cnt[f][0]
					
					a = np.linalg.norm(far-end)
					b = np.linalg.norm(far-start)
					c = np.linalg.norm(start-end)
					
					angulo = np.arccos((np.power(a, 2)+np.power(b, 2)-np.power(c, 2))/(2*a*b))
					angulo = np.degrees(angulo)
					angulo = int(angulo)
					
					if np.linalg.norm(start-end) > 20 and d > 12000:
						#cv2.putText(ROI, '{}'.format(d), tuple(far), 1, 1, color_d, 1, cv2.LINE_AA)
						cv2.circle(ROI, tuple(start), 5, color_start, 2)
						cv2.circle(ROI, tuple(end), 5, color_end, 2)
						cv2.circle(ROI, tuple(far), 7, color_far, -1)
						
					if len(inicio) == 0:
						minY = np.linalg.norm(ymin[0]-x,y)
						if minY >= 110:
							fingers = fingers + 1
							cv2.putText(ROI, '{}'.format(fingers), tuple(ymin[0]), 1, 1, color_fingers, 1, cv2.LINE_AA)
					
					for i in range(len(inicio)):
						fingers = fingers +1
						cv2.putText(ROI, '{}'.format(fingers), tuple(inicio[i]), 1, 1, color_fingers, 1, cv2.LINE_AA)
						if i == len(inicio)-1:
							fingers = fingers + 1
							cv2.putText(ROI, '{}'.format(fingers), tuple(fin[i]), 1, 1, color_fingers, 1, cv2.LINE_AA)
					
					cv2.putText(frame, '{}'.format(fingers), (390, 45), 1, 4, color_fingers, 2, cv2.LINE_AA)
	
	cv2.imshow('Frame', frame)
	
	k = cv2.waitKey(20)
	if k == ord('i'):  bg = cv2.cvtColor(frameAux, cv2.COLOR_BGR2GRAY)
	if k == ord('q'): break

cap.release()
cv2.destroyAllWindows()
	