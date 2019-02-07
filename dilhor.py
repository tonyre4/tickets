import cv2
import numpy as np

def dilhor(img,perc,ks):
    ini = (ks/2)
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
    from matplotlib import pyplot as plt

    img = cv2.imread("in/4.jpg",cv2.IMREAD_GRAYSCALE)
    cv2.imshow("Orig",img)
    img = bin.binar(img, 128)
    img, c = dilhor(img,10,5)
    print(c)
    plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()
    #cv2.imshow("dilHor", img)
    cv2.waitKey(0)
