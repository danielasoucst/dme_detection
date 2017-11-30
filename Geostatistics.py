# coding: utf-8
import numpy as np

import math

# Função que calcula as estatisticas semivariograma, semimadograma, correlograma e covariograma
# Recebe: img - imagem original
#         marcacao - imagem com a mascara da segmentação do disco otico
#         windowsize - tamanho da imagem (img. rols, img.cols)[dispensavel]
# 		label - label da imagem (dispensavel tbm)
# retorna: vector com o resultado dos calculos

def run(img, windowSize):
    resultados =[]
    # for r in range(0,len(resultados)):
    #    resultados[r]=-1000

    # resultados.resize(1000);
    car = 0


    xCenterOffset = windowSize[0] / 2
    yCenterOffset = windowSize[1] / 2


    xStart = xCenterOffset
    yStart = yCenterOffset


    xEnd = img.shape[1] - 1 - xCenterOffset
    yEnd = img.shape[0] - 1 - yCenterOffset

    for distance in range(1, 6):
        for direction in range(0,136,45):

            # // / gera as estatisticas geoespaciais
            parcial = computeAll(img, xStart, yStart, direction, distance, windowSize)

            resultados.append(parcial[0])
            resultados.append(parcial[1])
            resultados.append(parcial[2])
            resultados.append(parcial[3])

            car = car + 4


    return resultados

#
# Função que calcula as estatisticas semivariograma, semimadograma, correlograma e covariograma
# Recebe: img - imagem original
#         marcacao - imagem com a mascara da segmentação do disco otico
#         inicio e fim da altura e largura da janela
#         distance - a distancia entre os pares de pixels
#         direction - direção dos pares de pixels
#         windowsize - janela
# retorna: vector com o resultado dos calculos

def computeAll(img, xStart, yStart,direction,  distance,  windowSize):
    resultados = [0]*5

    smV = 0.0
    smM = 0.0
    coV = 0.0
    coR = 0.0
    roD = 0.0
    N = 0


    '''list of float'''
    meanV = computeMeans(img,xStart, yStart, direction, distance, windowSize)


    janela = computeWindow(xStart, yStart, windowSize, direction, distance)
    # print ('dim janela',janela)
    # // cout << endl << meanV[0] << " " << meanV[1] << " " << meanV[2];


    mean = meanV[0] * meanV[1]


    sdV1 = 0.0
    sdV2 = 0.0

    for y in range(janela[2],janela[3]):
        for x in range(janela[0], janela[1]):

            v1 = img[x][y]
            v2 = img[x + janela[4]][y + janela[5]]

            difference = abs( v1 - v2 )


            if(math.isnan(v1) or math.isnan(v2)):
                print ('janela, ', v1,v2)
            # difference2 = v1 - v2;
            #     variance   = difference2 *
            variance = difference*difference
            mult     = ( v1 * v2 ) - mean
            # print v1,v2
            if(math.isnan(v1) or math.isnan(v2) ):
                print ( 'NAn merma',  x,y,x + janela[4],y + janela[5])
            sdV1 += (v1 - meanV[0]) * (v1 - meanV[0])
            sdV2 += (v2 - meanV[1]) * (v2 - meanV[1])

            smV += variance
            smM += difference
            coV += mult
            N += 1
    # end for


    factor = 1.0/ N

    '''Semivariograma'''
    smV = 0.5 * factor * smV
    '''Semimadograma'''
    smM = 0.5 * factor * smM
    '''Covariograma'''
    coV = factor * coV
    # roD = 0.5 * factor * roD;

    '''Correlograma'''
    sdV1 = np.sqrt(factor * sdV1)
    sdV2 = np.sqrt(factor * sdV2)

    if (sdV1 == 0 or sdV2 == 0):
        coR = 0.0

    else:
        coR = coV / (sdV1 * sdV2)

    resultados[0] = smV;''' semivariograma'''
    resultados[1] = smM; '''semimadograma'''
    resultados[2] = coR; '''correlograma'''
    resultados[3] = coV; '''covariograma'''
    # resultados[4] = roD; '''rodograma'''

    return resultados

def computeMeans(img,xStart, yStart, direction,  distance,  windowSize):


    janela = computeWindow(xStart, yStart, windowSize, direction, distance)


    sumV1 = 0.0
    sumV2 = 0.0
    N = 0

    mean = []


    for y in range(janela[2],janela[3]):
        for x in range(janela[0],janela[1]):

            v1 = img[x][y]
            v2 = img[x + janela[4]][y + janela[5]]

            sumV1 += v1
            sumV2 += v2

            N += 1


    mean.append(sumV1 / N)
    mean.append(sumV2 / N)
    mean.append(N)
    return mean


def computeWindow(centerx,  centery,  windowSize,  direction, distance):

    janela = []

    # width = img.rows
    # height = img.cols

    xCenterOffset = windowSize[0] / 2
    yCenterOffset = windowSize[1] / 2


    xStart = centerx - xCenterOffset
    yStart = centery - yCenterOffset

    xEnd = centerx + xCenterOffset
    yEnd = centery + yCenterOffset


    xDistance = 0
    yDistance = -distance

    if(direction==45):
        xDistance = distance
    else:
        if(direction==90):
            xDistance = 0
        else:
            if(direction==135):
                xDistance = -distance


    if (xDistance < 0):
     xStart -= xDistance
    else:
        xEnd -= xDistance

    if (yDistance < 0 ):
        yStart -= yDistance

    janela.append(xStart)
    janela.append(xEnd)
    janela.append(yStart)
    janela.append(yEnd)
    janela.append(xDistance)
    janela.append(yDistance)
    # print janela,direction,distance
    return janela