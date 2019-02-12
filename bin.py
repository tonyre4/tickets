import cv2
import numpy as np

def binar(img,th):

    ##Mejorar contraste
    img_to_yuv = cv2.cvtColor(img,cv2.COLOR_BGR2YUV)
    img = img_to_yuv[:,:,0] 
    #img = cv2.equalizeHist(img_to_yuv[:,:,0])
    #img = cv2.cvtColor(img_to_yuv, cv2.COLOR_YUV2BGR)
    row,col = img.shape

    img = cv2.blur(img,(3,3))

    print(row,col)
    for i in range(row):
        for j in range(col):
            if img[i,j] < th:
                img[i,j] = 255 
            else:
                img[i,j] = 0

    #para filtrar ruido
    #kernel = np.ones((3,3),np.uint8)
    #img = cv2.dilate(img,kernel,iterations = 1)
    #img = cv2.erode(img,kernel,iterations = 1)
    return img


#test
if __name__ == '__main__':
    img = cv2.imread("in/2.jpg",1)
    cv2.imshow("Orig",img)
    img = binar(img, 200)
    cv2.imshow("Bin", img)
    cv2.waitKey(0)
