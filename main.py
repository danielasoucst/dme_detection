
# coding: utf-8
import cv2
import os
import Geostatistics as geo

def load_image(dir):
    lstImages = []
    for file in os.listdir(dir):
        if file.endswith(".tif"):
            volumeName = os.path.join(dir, file)
           # print (volumeName)
            img = cv2.imread(volumeName,0)
            lstImages.append(img)

    return lstImages


# dir = './Publication_Dataset/DME1/TIFFs/8bitTIFFs/'
dir = './retina.jpg'
img = cv2.imread(dir, 0)

# frames = load_image(dir)
# print ("total de frames",len(frames),type(frames[0]))


windowSize = [img.shape[0],img.shape[1]]
resultado = geo.run(img,windowSize)
print (type(resultado),len(resultado))
print resultado
