# coding: utf-8
import os
import cv2
import medpy_ani_diff as diffusionFilter
import heapq
import numpy as np
from scipy import ndimage as ndi


def load_image(dir):
    lstImages = []
    for file in os.listdir(dir):
        if file.endswith(".png"):
            volumeName = os.path.join(dir, file)
           # print (volumeName)
            img = cv2.imread(volumeName,0)
            lstImages.append(img)

    return lstImages

# def load_image(suj):
#     import pickle
#     print("Carregando volume...")
#     fileObject = open('./base_temp/'+suj, 'rb')
#     features1 = pickle.load(fileObject)
#
#     return features1





def getVolume(dir):
    lstImages = []
    for file in os.listdir(dir):
        if file.endswith(".tif"):
            volumeName = os.path.join(dir, file)
            # print (volumeName)
            img = cv2.imread(volumeName, 0)
            lstImages.append(img)

    vol = np.asarray(lstImages)
    aumento = 97.0/vol.shape[0] #qtde de frames
    if(aumento!=1):
        # print "aumento", aumento
        vol = ndi.interpolation.zoom(vol,[aumento,1,1])
        # print i.shape
        # print ("VOLUME",type(vol),vol.shape,type(lstImages[0]),lstImages[0].shape)
    # import
    #
    #
    # Image.register_save(vol[0],'./Publication_Dataset/')
    print ('salvando volume ',vol.shape[0])
    return vol.tolist()


def apply_filter(image,metodo):
    out = np.copy(image)
    if(metodo=='gauss'):
        out = cv2.GaussianBlur(image, (1, 3), 0)
    if(metodo=='anisotropic'):
        out = diffusionFilter.anisotropic_diffusion(image)
    return out

