# coding: utf-8
import numpy as np


# Função que calcula as estatisticas semivariograma, semimadograma, correlograma e covariograma
# Recebe: img - imagem original
#         marcacao - imagem com a mascara da segmentação do disco otico
#         windowsize - tamanho da imagem (img. rols, img.cols)[dispensavel]
# 		label - label da imagem (dispensavel tbm)
# retorna: vector com o resultado dos calculos

def run(img, marcacao, windowSize, label):
    resultados =[300]
    for r in resultados:
       r =-1000;

    # resultados.resize(1000);
    parcial=[];
    car = 0;


    xCenterOffset = windowSize[0] / 2
    yCenterOffset = windowSize[1] / 2


    xStart = xCenterOffset
    yStart = yCenterOffset


    xEnd = img.cols - 1 - xCenterOffset
    yEnd = img.rows - 1 - yCenterOffset

    for distance in range(1, 6):
        for direction in range(0,136,45):

            smV = smM = coV = coR = 0.0


            # // / gera as estatisticas geoespaciais
            parcial = computeAll(img, marcacao, xStart, xEnd, yStart, yEnd, direction, distance, windowSize);

            resultados[car] = parcial[0]

            resultados[car + 1] = parcial[1]
            resultados[car + 2] = parcial[2]
            resultados[car + 3] = parcial[3]

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
def computeAll(img, marcacao, xStart, xEnd, yStart, yEnd, direction,  distance,  windowSize):
    resultados = [300]

    smV = 0.0
    smM = 0.0
    coV = 0.0
    roD = 0.0
    N = 0
    coR = 0.0

    '''list of float'''
    meanV = []
    meanV = computeMeans(img, marcacao, xStart, xEnd, yStart, yEnd, direction, distance, windowSize);

    janela = []
    janela = computeWindow(img, xStart, yStart, windowSize, direction, distance);

    # // cout << endl << meanV[0] << " " << meanV[1] << " " << meanV[2];


    mean = meanV[0] * meanV[1];


    sdV1 = 0.0
    sdV2 = 0.0

    for y in range(janela[2],janela[3]):
        for x in range(janela[0], janela[1]):


            v1 = img[x][y]
            v2 = img[x + janela[4]][y + janela[5]];


            v1m = marcacao[x, y]
            v2m = marcacao[x + janela[4]][ y + janela[5]]

            if (v1m > 0 and v2m > 0):
            # // para calcular somente nos pixels do disco ótico
                difference = abs( v1 - v2 );
                difference2 = v1 - v2;
                variance   = difference2 * difference2;
                mult       = ( v1 * v2 ) - mean;

                sdV1 += ( v1 - meanV[0] ) * ( v1 - meanV[0] );
                sdV2 += ( v2 - meanV[1] ) * ( v2 - meanV[1] );

                smV += variance;

                raiz = np.sqrt(difference);
                roD += raiz;

                # // cout << v1 << " " << v2 << " variance:" << variance << " smV:" << smV << endl;
                smM += difference;
                coV += mult;
                N += 1





    factor = 1.0/ N

    # // smV = factor * smV;
    smV = 0.5 * factor * smV
    # // roD = sqrt(smM);

    # // cout << endl << "smV:" << smV << "  factor:" << factor << "  N:" << meanV[2];
    smM = 0.5 * factor * smM
    coV = factor * coV
    roD = 0.5 * factor * roD;

    sdV1 = np.sqrt(factor * sdV1);
    sdV2 = np.sqrt(factor * sdV2);

    if (sdV1 == 0 or sdV2 == 0):
        coR = 0.0

    else:
        coR = coV / (sdV1 * sdV2)

    resultados[0] = smV;''' semivariograma'''
    resultados[1] = smM; '''semimadograma'''
    resultados[2] = coR; '''correlograma'''
    resultados[3] = coV; '''covariograma'''
    resultados[4] = roD; '''rodograma'''

    return resultados

def computeMeans(img,  marcacao,  xStart,  xEnd,  yStart,  yEnd,  direction,  distance,  windowSize):
    mean = [10]
    janela = []
    janela = computeWindow(img, xStart, yStart, windowSize, direction, distance);


    sumV1 = 0.0
    sumV2 = 0.0

    N = 0

    # if (nomeimg == "Drishti//drishtiGS_004.png")
    # {
    #     cout << "parou" << endl;
    # getchar();
    # }
# // cout << janela[0] << " " << janela[1] << " " << janela[2] << " " << janela[3] << " " << janela[4] << " " << janela[
#     5];

    for y in range(janela[2],janela[3]):
        for x in range(janela[0],janela[1]):

            v1 = img[x][y]

            v2 = img[x + janela[4]][y + janela[5]]

            v1m = marcacao[x][y]

            v2m = marcacao[x + janela[4]][ y + janela[5]]

            if (v1m > 0 and v2m > 0):
            # // para contar somente os pixels dentro do disco ótico
                sumV1 += v1;
                sumV2 += v2;

                N += 1



# // cout << " " << sumV1 << " " << sumV2 << " " << N << endl;

    mean[0] = sumV1 / N
    mean[1] = sumV2 / N
    mean[2] = N
    # // cout << endl << mean[0] << " " << mean[1] << " " << mean[2];
    return mean


def computeWindow( img,  centerx,  centery,  windowSize,  direction, distance):

    janela = [10]

    width = img.rows

    height = img.cols


    xCenterOffset = windowSize[0] / 2

    yCenterOffset = windowSize[1] / 2


    xStart = 0

    yStart= 0


    xEnd = 0

    yEnd = 0

    # // / para o modo disco

    rest = windowSize[0] % 2;

# // cout << endl << rest;
    if (rest == 0):
        xEnd = (centerx + xCenterOffset)-distance
        yEnd = (centery + yCenterOffset)-distance

    else:
        xEnd = centerx + xCenterOffset
        yEnd = centery + yCenterOffset

    xStart = centerx - xCenterOffset;
    yStart = centery - yCenterOffset;


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

    if ( yDistance < 0 ):
        yStart -= yDistance

    janela[0] = xStart
    janela[1] = xEnd
    janela[2] = yStart
    janela[3] = yEnd
    janela[4] = xDistance
    janela[5] = yDistance

    return janela