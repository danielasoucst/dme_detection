
# coding: utf-8
import Geostatistics as geo
import input
import numpy as np
import flatten
import cropping
import pickle
import arffGenerator
from PIL import Image
from matplotlib import pyplot as plt

def getClass(pasta):
    inicio = pasta[:3]
    if(inicio=='AMD'):
        return inicio
    if(inicio=='DME'):
        return  inicio
    if(inicio=='NOR'):
        return 'NORMAL'
    return None

def extractFeatures(sujeito):
    lstImagens = input.load_image('./base_interpol/' + sujeito)

    lstGeoFeatures = []
    frame = 0
    for imagem in lstImagens:
        imagem = np.asarray(imagem)
        frame_denoise = input.apply_filter(imagem, 'anisotropic')
        bdValue, new = flatten.flat_image(frame_denoise)
        crop = cropping.croppy_mona(new, bdValue)
        print('FRAME ',frame)
        if(frame==3):
            img = Image.fromarray(crop)
            print crop[76][1]
            img.show()
        lstGeoFeatures.append(geo.run((crop),[crop.shape[0],crop.shape[1]]))
        frame+=1
    print('geo',len(lstGeoFeatures),len(lstGeoFeatures[0]))
    # dictionary = features_extraction.apply_BOW(lstSIFTFeatures)
    fileObject = open('./geo_features/'+sujeito, 'wb')
    if (fileObject != None):
        print('salvando...')
        pickle.dump(lstGeoFeatures, fileObject)
        fileObject.close

def getBaseFeatures():
    volumes = []
    volumes += ['DME1','DME2','DME3','DME4','DME5','DME6','DME7','DME8','DME9','DME10','DME11','DME12','DME13','DME14','DME15']
    volumes += ['NORMAL1','NORMAL2','NORMAL3','NORMAL4','NORMAL5','NORMAL6','NORMAL7','NORMAL8','NORMAL9','NORMAL10','NORMAL11','NORMAL12','NORMAL13','NORMAL14','NORMAL15']

    # for vol in volumes:
    #     print('Extraindo gabor features for: ',vol)
    #     geraGABORFeatures(vol)
    # for vol in volumes:
    #     print('Extraindo glcm features for: ',vol)
    #     geraGLCMFeatures(vol)
    for vol in volumes:
        print('Extraindo geo features for: ',vol)
        extractFeatures(vol)
    print ("Fim...")

def loadFeatures():
    volumes = []
    volumes += ['DME1', 'DME2', 'DME3', 'DME4', 'DME5', 'DME6', 'DME7', 'DME8', 'DME9', 'DME10', 'DME11', 'DME12',
                'DME13', 'DME14', 'DME15']
    volumes += ['NORMAL1', 'NORMAL2', 'NORMAL3', 'NORMAL4', 'NORMAL5', 'NORMAL6', 'NORMAL7', 'NORMAL8', 'NORMAL9',
                'NORMAL10', 'NORMAL11', 'NORMAL12', 'NORMAL13', 'NORMAL14', 'NORMAL15']

    featuresGeo = []
    vetLabelsGeo = []

    for vol in volumes:
        print('Extraindo glcm features for: ', vol)
        fileObject = open('./geo_features/' + vol, 'rb')
        featuresVolume = pickle.load(fileObject)

        volumeInLine = []
        for i in featuresVolume:
            volumeInLine += i

        print ('tam:',len(volumeInLine))
        featuresGeo.append(volumeInLine)
        vetLabelsGeo.append(getClass(vol))

    print ('Gerando arff file for glcm',len(vetLabelsGeo),len(featuresGeo))
    arffGenerator.createArffFile('./geo_features/GEODATASET', featuresGeo, vetLabelsGeo, 'DME,NORMAL',
                                 len(featuresGeo[0]))


# getBaseFeatures()
# extractFeatures("DME7")
# loadFeatures()
# import math



















