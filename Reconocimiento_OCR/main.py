import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

placa = []
image = cv2.imread('imagen.png')

text = pytesseract.image_to_string(image, lang='spa')
print(text)

cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()