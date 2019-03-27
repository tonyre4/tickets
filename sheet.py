#!/usr/bin/python3
# 2017.12.20 10:47:28 CST
# 2017.12.20 11:29:30 CST

import cv2
import numpy as np
import matplotlib.pyplot as plt
import subprocess as bash
import time

#Retorna el poligono donde cabe la hoja y la deteccion
def getsheet(img):
    ##(2) convert to hsv-space, then split the channels
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)

    ##(3) threshold the S channel using adaptive method(`THRESH_OTSU`) or fixed thresh
    th, threshed = cv2.threshold(s, 50, 255,
                                 cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    #cv2.imshow("th",threshed)

    ##(4) find all the external contours on the threshed S
    cnts = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    canvas  = img.copy()
    #cv2.drawContours(canvas, cnts, -1, (0,255,0), 1)

    ## sort and choose the largest contour
    cnts = sorted(cnts, key = cv2.contourArea)
    cnt = cnts[-1]

    ## approx the contour, so the get the corner points
    arclen = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02* arclen, True)
    cv2.drawContours(canvas, [cnt], -1, (255,0,0), 1, cv2.LINE_AA)
    #cv2.imshow("c1",canvas)
    cv2.drawContours(canvas, [approx], -1, (0, 0, 255), 1, cv2.LINE_AA)
    approx = approx.reshape(approx.shape[0],2)

    return approx,canvas

#Retorna el ticket recortado y rotado
def cropSkew(img):
    #Se obtiene el poligono y el resultado de hoja detectada
    poly, z = getsheet(img)
    #Se calcula el angulo
    angle = np.arctan((poly[1,1]-poly[0,1])/(poly[1,0]-poly[0,0]))
    angle = np.rad2deg(angle)
    angle += 90
    rows = img.shape[0]
    cols = img.shape[1]
    #Se rota la imagen original
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    rows = dst.shape[0]
    cols = dst.shape[1]
    #De la imagen rotada se obtiene de nuevo la hoja
    poly, z = getsheet(dst)
    #Se obtiene un recortado provisional
    crop = dst[np.min(poly[:,1]):np.max(poly[:,1]),np.min(poly[:,0]):np.max(poly[:,0])]
    if crop.shape[0]<crop.shape[1]:
        crop = np.rot90(crop)
        crop = np.rot90(crop)
        crop = np.rot90(crop)

    #Para obtener solamente area con hoja
    #Quitar porcentaje de la respuesta (no es muy bueno)
    #r,c,x = crop.shape
    #r,c = int(r*.05) , int(c*.05)
    #crop = crop[r:-r,c:-c]


    #Para quitar pixeles negros de las orillas
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    th, threshed = cv2.threshold(s, 50, 255,
                                 cv2.THRESH_BINARY_INV)

    #Se hace una media de todas las orillas, y se borra la que tenga mas
    #negros, se realiza el bucle hasta que ya no haya pixeles negros en las
    #orillas
    means = [0,0,0,0]
    #while not np.all([np.all(threshed[0,:]),np.all(threshed[:,0]), np.all(threshed[:,-1]), np.all(threshed[-1,:])]):
    while means != [255,255,255,255]:
        means = [np.mean(threshed[0,:]), #top
                 np.mean(threshed[:,0]), #left
                 np.mean(threshed[:,-1]), #right
                 np.mean(threshed[-1,:])] #bottom
        op = np.argmin(means)

        #Croping top
        if op == 0:
            crop = crop[1:,:]
            threshed = threshed[1:,:]
        #Cropping left side
        if op == 1:
            crop = crop[:,1:]
            threshed = threshed[:,1:]
        #Cropping right
        if op == 2:
            crop = crop[:,:-1]
            threshed = threshed[:,:-1]
        #Cropping bottom
        if op == 3:
            crop = crop[:-1,:]
            threshed = threshed[:-1,:]
    return crop


if __name__ == "__main__":
    img = cv2.imread("x1.jpg")
    
    crop = cropSkew(img) 


    YCrCb = cv2.cvtColor(crop, cv2.COLOR_BGR2YCrCb)
    gray,_,_ = cv2.split(YCrCb)
    th, threshed = cv2.threshold(gray, 200, 255,
                                cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    #gray = cv2.blur(gray,(5,5))
    th3 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                cv2.THRESH_BINARY_INV,11,2)

    anded = cv2.bitwise_and(th3,threshed)
   
    #anded = cv2.morphologyEx(anded, cv2.MORPH_CLOSE, np.ones((3,3), dtype=np.uint8))


    #cv2.imshow("h",gray)
    #cv2.imshow("w",th3)
    #cv2.imshow("x",threshed) 
    #cv2.imshow("and", anded)

    

    ## Ok, you can see the result as tag(6)
    #cv2.imshow("c2",crop)
    #cv2.waitKey(0)

    #Redimensionando x4
    x4 = cv2.resize(anded, None, fx=4,fy=4)
    x4 = cv2.erode(anded,np.ones((3,3),dtype=np.uint8))
    cv2.imwrite("out.png",x4)
    print ("out.png guardado en raiz\nPasando por tesseract...")
    time.sleep(0.2)
    bash.check_output("tesseract -l spa out.png out", shell=True)
    time.sleep(0.2)
    
    with open("out.txt", "r") as f:
        print("/////\nTexto detectado\n/////")
        for l in f:
            lprint = l.replace("\n","")
            if lprint != "" or lprint.replace(" ","") != "":
                print (lprint)
    print("/////\n///////////////\n/////")

