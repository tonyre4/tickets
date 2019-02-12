import cv2
import numpy as np
import time

def dilver(img,perc,ks):
    ini = int(ks/2)
    initi = ini + 1
    row,col = img.shape
    inited = False
    rowinit = 0
    coords = np.empty((0,2))
    imout = np.copy(img)

    for i in range(initi,col-ini):
        subm = img[:,(i-ini):(i+ini)] 
        mean = (np.sum(subm)/np.prod(subm.shape))*100/255
        if mean <= perc:
            imout[:,i].fill(128)
            if inited:
                inited = False
                coords = np.vstack([coords, np.array([rowinit,i-1])])
        else:
            if not inited:
                inited = True
                rowinit = i
    return imout,coords


#test
if __name__ == '__main__':
    import bin
    import dilhor
    import cortar
    import subprocess

    subprocess.Popen("rm -r ./renglones/words_reng*", shell=True) 
    subprocess.Popen("rm ./renglones/*", shell=True)
    img = cv2.imread("in/6.jpg")
    img2 = bin.binar(np.copy(img), 200)
    img2, c = dilhor.dilhor(img2,5,5)
    rengs = cortar.cort(img,"renglones/",c)

    kern = np.ones((5,5),np.uint8)

    #NO MOVER (si no se crean antes los directorios no se guardan las imagenes)
    for i in range(rengs):
        subprocess.Popen("mkdir ./renglones/words_reng"+ str(i), shell=True) 

    #Cliclo de procesado de palabras
    for i in range(rengs):
        #Leer renglon
        im = cv2.imread("renglones/reng_" + str(i) + ".jpg")
        #Binarizarlo
        im2 = bin.binar(np.copy(im), 200)
        #Dilatarlo (para hacer mejor los cortes)
        im2 = cv2.dilate(im2,kern)
        #Separar palabras y obtener coordenadas
        im2,c2 = dilver(im2,5,10)

        #Ciclo para obtener cada imagen de cada palabra
        for j in range(c2.shape[0]):
            z = c2[j,:]
            #print (z)
            f = im[:,int(z[0]):int(z[1])]
            #cv2.imshow("palabra",f)
            #cv2.waitKey(0)
            cv2.imwrite("./renglones/words_reng" + str(i) + "/word" + str(j) + ".jpg", f)



