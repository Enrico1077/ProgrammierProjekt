import random
import numpy as np


Anzahl_s = 20
Dimension_s =3

def RandData(Anzahl, Dimension):        #Erzeugt "Anzahl" viele "Dimension" dimensionale zufällige Datenpunkte(Test-Daten)

    Datenpunkte = []
    for i in range(0, Anzahl):
        Datenpunkt=[]
        for j in range(0,Dimension):
            Datenpunkt.append(random.randrange(100))   
        Datenpunkte.append(Datenpunkt)
    return np.array(Datenpunkte)

def CreateZent(Anzahl, Dimension):      #Erzeugt "Anzahl" viele zufällige Zentruide in der angegebenden Dimension(1. Interation)
    Datenpunkte=[]
    for i in range(0, Anzahl):
        Datenpunkt=[]
        for j in range(0,Dimension):
             Datenpunkt.append(random.randrange(100))   
        Datenpunkte.append(Datenpunkt)
    return np.array(Datenpunkte)


Zentruide=np.array([[5,7],[1,9]])
Datenpunkte=np.array([[5,7],[4,5],[8,4]])
#def CalcDistancesVec(Zentruide, Datenpunkte):
Differences=np.array([])
for Datapoint in Datenpunkte:
    Zentdiff=np.array([])
    for Zentruid in Zentruide:
        Diff=Zentruid-Datapoint
        if Zentdiff.size == 0:
                Zentdiff=Diff
        else:
            Zentdiff=np.stack((Zentdiff,Diff))
    if Differences.size==0:
        Differences=Zentdiff
    else:
        print(Differences)
        print("")
        print(Zentdiff)
        Differences=np.stack((Differences,Zentdiff))
#return Differences
    
#print(CalcDistancesVec(np.array([[5,7],[1,9]]),np.array([[5,7],[4,5],[8,4],[2,1],[5,7]])))
                



