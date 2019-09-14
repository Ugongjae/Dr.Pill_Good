
import cv2
import numpy as np
import pytesseract

from  PIL import Image, ImageEnhance

path="./white/"
for p in range(2345,2346):
    Number=path+str(p)+'.jpg'
    img=cv2.imread(Number,cv2.IMREAD_COLOR)
    #img =cv2.resize(img, dsize=(561, 352), interpolation=cv2.INTER_AREA)
    final=img.copy()
    
    final = Image.fromarray(final)
    final = ImageEnhance.Color(final).enhance(0.0)
    final = ImageEnhance.Contrast(final).enhance(11.0)
    final = np.array(final)
    '''
    final=cv2.cvtColor(final,cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    ff = clahe.apply(final)

    final = cv2.resize(final,(561,352))
    ff = cv2.resize(ff,(561,352))

    final = np.hstack((final, ff))
    '''
    #ret2,th1 = cv2.threshold(img2 ,0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img2,(7,7),0)
    #trunc = cv2.threshold(img2,255,255, cv2.THRESH_TRUNC)[1]
    #cv2.imwrite('1_trunc.jpg',trunc)
    thresh_mean=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,6)
    #thresh_mean=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,17,7)

    canny=cv2.Canny(thresh_mean,100,200)
    #otsu=cv2.threshold(blur,0,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)[1]
    otsu=cv2.threshold(blur,255,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)[1]

    dilate = cv2.dilate(otsu, None, iterations=1)

    kernel = np.ones((9,9),np.uint8)
    closing=cv2.morphologyEx(dilate,cv2.MORPH_CLOSE,kernel)

    contours, hierachy= cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours,key=lambda x:cv2.boundingRect(x)[2]*cv2.boundingRect(x)[3],reverse=True)
    j=0
    for i in contours:
        area=cv2.contourArea(i)
        x,y,w,h=cv2.boundingRect(i)
        rect_area=w*h
        aspect_ratio=float(w)/h

        #if rect_area>=400 and h>=w:
        cv2.rectangle(img,(x-5,y-5),(x+w+10,y+h+10),(0,255,0),1)
        cv2.imwrite('bbb.jpg',img)
        final=final[y-5:y+h+5,x-5:x+w+5]
        #cv2.imwrite(path+str(p)+'_.jpg',final)
        break
        
    #final =cv2.resize(final, dsize=(300, 300), interpolation=cv2.INTER_AREA)

    fimg2=cv2.cvtColor(final,cv2.COLOR_BGR2GRAY)
    fblur = cv2.GaussianBlur(fimg2,(7,7),0)
    fthresh_mean=cv2.adaptiveThreshold(fblur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,21,6)
    cv2.imwrite(path+str(p)+'___.jpg',fthresh_mean)
    fcanny=cv2.Canny(fthresh_mean,100,200)
    cv2.imwrite(path+str(p)+'_.jpg',fcanny)

    contours, hierachy= cv2.findContours(fcanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours,key=lambda x:cv2.boundingRect(x)[2]*cv2.boundingRect(x)[3],reverse=True)
    for i in contours:
        area=cv2.contourArea(i)
        x,y,w,h=cv2.boundingRect(i)
        rect_area=w*h
        aspect_ratio=float(w)/h
        if rect_area<=1100 and rect_area>100 and x>10 and x<=90 and y>10 and y<=90:
            cv2.rectangle(final,(x-5,y-5),(x+w+10,y+h+10),(0,255,0),1)
        #final=final[y-5:y+h+10,x-5:x+w+10]
        #cv2.imwrite(path+str(p)+'__.jpg',final)
        

    #cv2.imshow('mm',cv2.resize(img,(561,352)))

    fdilate = cv2.dilate(fcanny, None, iterations=1)
    cv2.imwrite('f_dilate.jpg',fdilate)

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


    cv2.imwrite('closing.jpg',closing)

    '''
    mask = np.ones(img.shape[:2], dtype="uint8") * 255
    newimage = cv2.bitwise_and(dilate.copy(), dilate.copy(), mask=mask)
    newimage = cv2.dilate(newimage, None, iterations=1)
    cv2.imwrite('1_bitwise.jpg',newimage)
    newimage = cv2.threshold(newimage ,0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    '''

    print('-----------------------'+str(p)+'---------------------------')
    print(pytesseract.image_to_string(Image.open(path+str(p)+'_.jpg'), lang='eng'))
