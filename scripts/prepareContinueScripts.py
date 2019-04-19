import pandas as pd
import sys
import os

#funcion que permite procesar los PDB
def processPDBData(pdbList):

    pdbData = []

    for element in pdbList:
        element = str(element)
        element = element.replace(" ", "")
        element = element.upper()
        pdbData.append(element)
    return pdbData

#funcion que permite procesar la posicion en el PDB
def processPosValue(posList):

    posData = []

    for element in posList:
        posData.append(int(element))
    return posData

#funcion que permite procesar la respuesta asociada a la informacion
def processResponse(posResponse):

    responseData = []

    for element in posResponse:
        element = element.replace(",", ".")
        responseData.append(float(element))
    return responseData

#funcion que permite
listHeader = ['PDB','Chain','AAWT','AAMT','Pos','Response']

pathInput = sys.argv[1]
pathOutput = sys.argv[2]
numberDataSet = int(sys.argv[3])

#creamos listas con todos los elementos existentes en los set de datos
codePDB = []
chain = []
aawt = []
aamt = []
pos = []
response = []

#hacemos la lectura de cada dataset en base a la informacion existente en el path asociado
for i in range(numberDataSet):

    nameDataSet = str(i+1)+".csv"
    print "process dataset: ", nameDataSet
    dataSet = pd.read_csv(pathInput+nameDataSet)

    codePDB = codePDB + processPDBData(dataSet['PDB'])
    chain = chain + processPDBData(dataSet['Chain'])
    aawt = aawt + processPDBData(dataSet['AAWT'])
    aamt = aamt + processPDBData(dataSet['AAMT'])
    pos = pos + processPosValue(dataSet['Pos'])
    response = response + processResponse(dataSet['Response'])

#obtenemos la lista unica de proteinas
listUniqueProtein = list(set(codePDB))

#por cada proteina creamos un set de datos y lo almacenamos creando un directorio asociado a la data de interes
for pdb in listUniqueProtein:

    #obtenemos la matriz para formar los set de datos
    indexPos = []
    for i in range(len(codePDB)):
        if codePDB[i] == pdb:
            indexPos.append(i)

    #en base a este indice y si el numero de ejemplos es mayor a 50 formamos los nuevos set de datos
    if len(indexPos)>100:
        command = "mkdir -p " + pathOutput+pdb
        print command
        os.system(command)#creamos el directorio

        #formamos la nueva matriz de elementos
        matrixResponse = []
        for i in range(len(indexPos)):
            row = [chain[i], aawt[i], pos[i], aamt[i], response[i]]
            matrixResponse.append(row)

        #generamos el csv
        dataFrame = pd.DataFrame(matrixResponse, columns=['Chain', 'AAWT','Pos', 'AAMT', 'Response'])
        nameDoc = pathOutput+pdb+"/dataSet_"+pdb+".csv"
        dataFrame.to_csv(nameDoc, index=False)
