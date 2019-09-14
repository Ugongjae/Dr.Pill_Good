#!/usr/bin/etc python

import cv2
import numpy as np
import pytesseract
from  PIL import Image

class Recognition:
     def ExtractNumber(self):
          Number='1423.jpg'
          img=cv2.imread(Number,cv2.IMREAD_COLOR)
          img =cv2.resize(img, dsize=(557, 348), interpolation=cv2.INTER_AREA)
          copy_img=img.copy()
          
          img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
          blur = cv2.GaussianBlur(img2,(3,3),0)
          thresh_mean=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,17,9)
          cv2.imwrite('thresh_mean.jpg',thresh_mean)
          canny=cv2.Canny(blur,100,200)
          cv2.imwrite('canny.jpg',canny)
          otsu=cv2.threshold(blur,0,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)[1]
          otsu=cv2.Canny(otsu,100,200)
          cv2.imwrite('otsu.jpg',otsu)

          """
          abab=cv2.adaptiveThreshold(img2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,17,6)
          
          abac=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,17,9)
          otsu=cv2.threshold(abab,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
          canny=cv2.Canny(abab,100,200)
          abad=cv2.adaptiveThreshold(canny,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,17,9)
          """

          cnts,contours,hierarchy  = cv2.findContours(thresh_mean, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
          result = pytesseract.image_to_string(Image.open('thresh_mean.jpg'), lang='eng')
          return(result.replace(" ",""))

          box1=[]
          f_count=0
          select=0
          plate_width=0

          for i in range(len(contours)):
               cnt=contours[i]
               area = cv2.contourArea(cnt)
               x,y,w,h = cv2.boundingRect(cnt)      #좌상단 꼭지점 좌표, width, height
               rect_area=w*h  #area size
               aspect_ratio = float(w)/h # ratio = width/height
               print(w,h)
               print(rect_area)
               print(aspect_ratio)
               print('^^^^^^^')
               #1300일때 숫자는 나옴
               if (aspect_ratio>=0.2)and(aspect_ratio<=1.5)and(rect_area>=1000)and(rect_area<=1300):
               #if  (aspect_ratio>=0.2)and(aspect_ratio<=1.0)and(rect_area>=100)and(rect_area<=700):

                   cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),1)       #원본이미지위에 사각형그리기 (이미지, 사각형왼쪽 상단점, 사각형오른쪽하단점,선색,선두께)
                   box1.append(cv2.boundingRect(cnt))

          for i in range(len(box1)): ##Buble Sort on python
               for j in range(len(box1)-(i+1)):
                    if box1[j][0]>box1[j+1][0]:
                         temp=box1[j]
                         box1[j]=box1[j+1]
                         box1[j+1]=temp

         #to find number plate measureing length between rectangles
          for m in range(len(box1)):
               count=0
               for n in range(m+1,(len(box1)-1)):
                    delta_x=abs(box1[n+1][0]-box1[m][0])
                    if delta_x > 150:
                         break
                    delta_y =abs(box1[n+1][1]-box1[m][1])
                    if delta_x ==0:
                         delta_x=1
                    if delta_y ==0:
                         delta_y=1
                    gradient =float(delta_y) /float(delta_x)
                    if gradient<0.25:
                        count=count+1
               #measure number plate size
               if count > f_count:
                    select = m
                    f_count = count
                    plate_width=delta_x
          cv2.imwrite('snake.jpg',img)


          number_plate=copy_img[box1[select][1]-10:box1[select][3]+box1[select][1]+20,box1[select][0]-10:140+box1[select][0]]
          resize_plate=cv2.resize(number_plate,None,fx=1.8,fy=1.8,interpolation=cv2.INTER_CUBIC+cv2.INTER_LINEAR)
          plate_gray=cv2.cvtColor(resize_plate,cv2.COLOR_BGR2GRAY)
          ret,th_plate = cv2.threshold(plate_gray,150,255,cv2.THRESH_BINARY)

          cv2.imwrite('plate_th.jpg',th_plate)
          kernel = np.ones((3,3),np.uint8)
          er_plate = cv2.erode(th_plate,kernel,iterations=1)
          er_invplate = er_plate
          cv2.imwrite('er_plate.jpg',er_invplate)
          result = pytesseract.image_to_string(Image.open('er_plate.jpg'), lang='eng')
          return(result.replace(" ",""))


recogtest=Recognition()
result=recogtest.ExtractNumber()
print(result)
print(pytesseract.image_to_string(Image.open('1423.jpg'), lang='eng'))
