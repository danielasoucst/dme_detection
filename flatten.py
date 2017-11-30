# coding: utf-8
import numpy as np
from scipy.ndimage.interpolation import shift


def find_polynomial(lst_x,lst_y,largura):

    # print('x,y',len(lst_x),len(lst_y))
    z = np.polyfit(lst_x, lst_y, 2)
    f = np.poly1d(z)

    x_new = np.linspace(lst_x[0], lst_x[-1], largura)
    y_new = f(x_new)
    return y_new.tolist()

def calculate_diff(lstSup,lstInf):
    result = [0 for x in range(0,len(lstSup))]
    # print('diff',len(lstSup),len(lstInf))
    for i in range(0,len(lstSup)):
        result[i] = round(lstInf[i]-lstSup[i],0)

    # print ('ajuste: ',result)
    return result

def shift_image(image,lst_x,diff):
    index = 0
    imageCopy = np.copy(image)
    for x in lst_x:
        column = image[0:imageCopy.shape[0], x]
        imageCopy[0:image.shape[0], x] = shift(column, diff[index], cval=255.0)
        index +=1
    return imageCopy

def flat_image(image):
    # print image.shape
    pilot_rpe = []
    list_x = []

    for c in range(0,image.shape[1]):
        column = image[0:image.shape[0],c]
        column_list = column.tolist()

        for i in range(len(column_list)-2,0,-1):
           if( column_list[i] > 100 and column_list[i] != 255):
                list_x.append(c)
                pilot_rpe.append(i)
                break
    # print ('c:',image.shape,c,len(pilot_rpe))
    '''definimos a linha horizontal q representará o limite inferior'''
    limit = []
    if (len(pilot_rpe) > 0):
        # ele = abs(max(pilot_rpe)-min(pilot_rpe))/2
        ele = max(pilot_rpe)
        limit = [ele for x in xrange(0, len(pilot_rpe))]

    poly = find_polynomial(list_x, pilot_rpe,len(list_x))

    diff = calculate_diff(poly, limit)
    image_flatten = shift_image(image, list_x, diff)
    # return pilot_rpe,limit,poly
    # from matplotlib import pyplot as plt
    #
    # plt.figure()
    # plt.subplot(121)
    # plt.imshow(image_flatten, 'gray')
    # plt.subplot(122)
    # plt.imshow(image, 'gray')
    # plt.plot(pilot_rpe, '.', lw=1)
    # plt.plot(limit, '-', lw=1)
    # plt.show()

    return limit[0], image_flatten

