import cv2
import numpy as np

def cort(img,path,coords):
    row,col = img.shape
    fil,x = coords.shape
    #print(row,col)
    for i in range(fil):
        z = coords[i,:]
        print (z)
        f = img[int(z[0]):int(z[1]), :]
        cv2.imwrite(path + "reng_" + str(i) + ".jpg", f)

#test
if __name__ == '__main__':
    import bin
    import dilhor
    import subprocess

    subprocess.Popen("rm ./renglones/*.jpg", shell=True)
    img = cv2.imread("in/2.jpg",cv2.IMREAD_GRAYSCALE)
    img2 = bin.binar(np.copy(img), 128)
    img2, c = dilhor.dilhor(img2,10,5)
    cort(img,"renglones/",c)
