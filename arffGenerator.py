
def createArffFile(nameFile,vetFeatures,vetLabels,labels,attLength):

    file = open(nameFile+".arff", 'w')
    file.write("@RELATION eye\n")

    for k in range(0,attLength):
        file.write("@ATTRIBUTE 'att"+str(k)+"' real\n")
    file.write("@ATTRIBUTE 'class' {"+labels+"}\n")
    file.write("@DATA\n")
    for i in range(0,len(vetFeatures)):
        # vetFeatures[i] = normalize(vetFeatures[i])
        for j in range(0,len(vetFeatures[i])):
            file.write(str(vetFeatures[i][j])+", ")
        file.write(str(vetLabels[i]) + "\n")
    file.close()


def createSuperArffFile(nameFile, vetFeatures, vetLabels, labels, attLength):
    file = open(nameFile + ".arff", 'w')
    file.write("@RELATION eye\n")

    for k in range(0, attLength):
        file.write("@ATTRIBUTE 'att" + str(k) + "' real\n")
    file.write("@ATTRIBUTE 'class' {" + labels + "}\n")
    file.write("@DATA\n")
    for inst in range(0,len(vetFeatures)):
        for i in range(0, len(vetFeatures[0])):
            for j in range(0, len(vetFeatures[i])):
                file.write(str(vetFeatures[i][j]) + ", ")
            file.write(str(vetLabels[i]) + "\n")
    file.close()


def read_csv_file(nameFile):
    file = open(nameFile,'r')
    line = file.readline()
    cont = 0
    lstIdFrames = []
    lstValuePixel = []
    while(line!=None):
        line = file.readline()
        if(len(line)<5 ):
            break
        line = line.split(',')
        #print(line, len(line))
        porcentagem = float(line[4])
        if(line[2]=='2:1' or line[2]=='3:2' ):  #if(line[2]=='2:1' and line[3]==''):
            lstIdFrames.append(int(line[0]))
            lstValuePixel.append(porcentagem)
        if(line[1]=='2:1'):
            cont += 1
    return lstIdFrames,cont,lstValuePixel


def normalize(a):

    import numpy as np

    a = np.asarray(a)

    eps = 1e-7

    # normalize the histogram
    hist = a.astype("float")
    hist /= (hist.sum() + eps)
    return hist.tolist()