import cv2
import numpy as np

def dilhor(img,perc,ks):
    ini = int(ks/2)
    initi = ini + 1
    row,col = img.shape
    inited = False
    rowinit = 0
    coords = np.empty((0,2))
    imout = np.copy(img)

    for i in range(initi,row-ini):
        mean = (np.sum(img[(i-ini):(i+ini),:])/col)*100/255
        if mean <= perc:
            imout[i,:].fill(255)
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
    import sys
    from matplotlib import pyplot as plt

    args = sys.argv

    img = cv2.imread("in/" + args[1] +".jpg")
    cv2.imshow("Orig",img)
    img = bin.binar(img, 200)
    img, c = dilhor(img,5,3)
    print(c)
    plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()
    #cv2.imshow("dilHor", img)
    cv2.waitKey(0)
