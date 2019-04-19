'''
script que permite agregar la cadena al set de datos
Requiere: BioPython
'''

import sys
import pandas as pd
from Bio.PDB.PDBParser import PDBParser

#recibimos el code PDB y el path de entrada
codePDB = sys.argv[1]
pathInput = sys.argv[2]
dataSet = pd.read_csv(pathInput+"dataSet_"+codePDB+".csv")

parser = PDBParser()#creamos un parse de pdb
structure = parser.get_structure(codePDB.lower(), pathInput+codePDB.lower()+".pdb")#trabajamos con la proteina cuyo archivo es 1AQ2.pdb

#obtenemos la cadena y los elementos asociados: residuo-posicion
matrix = []
for model in structure:
    for chain in model:
        for residue in chain:
            row = [chain.id, residue.id[1]]
            matrix.append(row)

chainColumn = []

#buscamos la cadena en la mutacion
for i in range(len(dataSet)):

    exist =1
    for element in matrix:
        if dataSet['Pos'][i] == element[1]:
            chainColumn.append(element[0])
            exist=0
            break
    if exist == 1:
        chainColumn.append('NA')
        
#agregamos la columna al set de datos
dataSet['chain'] = chainColumn
#exportamos el csv con la data...
dataSet.to_csv(pathInput+"dataSet_addChain_"+codePDB+".csv", index=False)
