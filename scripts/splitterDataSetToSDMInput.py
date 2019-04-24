'''
Este script permite recibir un archivo csv con la informacion de la mutacion y lo transforma a archivo txt para ingresarlo o ejecutar SDM
1. Recibe CSV
2. Codifica la data
3. Genera un directorio
4. Almacena los archivos
'''

import pandas as pd
import sys
import os

#funcion que permite crear un txt
def createFileExport(rowData, nameDoc):

    fileWrite = open(nameDoc, 'w')
    for element in rowData:
        fileWrite.write(element+"\n")
    fileWrite.close()

#lista de PDBS en el directorio
ListPDB = ['1A22','1CHO','1DKT','1FKJ','1FTG','1PPF','1RX4','1WQ5','2AFG','3SGB','5AZU']

#recibimos el directorio de salida y el archivo csv
pathOutput = sys.argv[1]

for codePDB in ListPDB:

    nameFileInput = pathOutput+codePDB+"/dataSet_"+codePDB+".csv"
    pathOutputPDB = pathOutput+codePDB+"/filesSDM/"

    dataSet = pd.read_csv(nameFileInput)
    matrixNew = []

    for i in range(len(dataSet)):

        mutation = "%s%d%s" % (dataSet['AAWT'][i], dataSet['Pos'][i], dataSet['AAMT'][i])
        row = "%s %s" % (dataSet['Chain'][i], mutation)
        matrixNew.append(row)

    #obtenemos la cantidad de documentos a crear
    documents = int(len(matrixNew)/20)
    resto = len(matrixNew) % 20

    print documents
    print resto
    #creamos el directorio de salida
    command = "mkdir -p %s" % pathOutputPDB
    os.system(command)

    indexPosInit = 0
    for i in range(documents):#cantidad inicial de archivos a crear

        partialMatrix = []
        for j in range(indexPosInit, indexPosInit+20):
            partialMatrix.append(matrixNew[j])
        nameDoc = "%ssdmInput_file_%d.txt" % (pathOutputPDB, i)
        print "create file ", nameDoc
        createFileExport(partialMatrix, nameDoc)
        indexPosInit+=20

    #trabajamos con el resto
    rowFinal = []
    for j in range(len(matrixNew)-resto, len(matrixNew)):
        rowFinal.append(matrixNew[j])

    nameDoc = "%ssdmInput_file_%d.txt" % (pathOutputPDB, i+1)
    print "create file ", nameDoc
    createFileExport(rowFinal, nameDoc)
