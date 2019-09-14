import cv2
import numpy as np
import pytesseract

from  PIL import Image, ImageEnhance

name="test1.jpg"
img=cv2.imread(name,cv2.IMREAD_COLOR)#사진 읽어오기

img =cv2.resize(img, dsize=(500, 500), interpolation=cv2.INTER_AREA)

#------------------------명암비 올리기---------------------------
img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
ff = clahe.apply(img)
ff = cv2.resize(img,(500,500))
#---------------------------------------------------------------

blur=cv2.GaussianBlur(ff,(5,5),0)#블러처리

thresh_mean=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,4)#스레드
#thresh_mean = cv2.threshold(blur,175,255, cv2.THRESH_BINARY)[1]
#thresh_mean =cv2.resize(thresh_mean, dsize=(300, 200), interpolation=cv2.INTER_AREA)
cv2.imwrite('thresh.jpg',thresh_mean)

v=np.median(img)
sigma=0.33
lower=int(max(0,(1.0-sigma)*v))
upper=int(min(255,(1.0+sigma)*v))

canny=cv2.Canny(img,lower,upper)#캐니
cv2.imwrite('canny.jpg',canny)

otsu=cv2.threshold(canny,255,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)[1]
cv2.imwrite('otsu.jpg',otsu)



kernel=np.ones((3,3),np.uint8)

closing=cv2.morphologyEx(canny,cv2.MORPH_CLOSE,kernel)
dilate = cv2.dilate(canny, kernel, iterations=2)
dilate =cv2.resize(dilate, dsize=(120, 120), interpolation=cv2.INTER_AREA)
cv2.imwrite('dilate.jpg',dilate)

closing =cv2.resize(closing, dsize=(300, 300), interpolation=cv2.INTER_AREA)
cv2.imwrite('opening.jpg',closing)

median=cv2.medianBlur(thresh_mean,3)
median=cv2.bitwise_not(cv2.bitwise_xor(median,median))
median =cv2.resize(median, dsize=(120, 120), interpolation=cv2.INTER_AREA)
cv2.imwrite('median.jpg',median)

print(pytesseract.image_to_string(Image.open('thresh.jpg'), lang='eng'))