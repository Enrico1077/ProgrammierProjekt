import random
import numpy as np



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


def CalcDistancesVec(Zentruide, Datenpunkte):           #Stellt ein 3D Array auf in welchen die Abstandsvektoren von jedem Zentroid zu jedem Datenpunkt enthalten sind
    Differences=np.array([])
    for Datapoint in Datenpunkte:
        Zentdiff=np.array([])
        for Zentruid in Zentruide:
            Diff=np.array(Zentruid-Datapoint)
            if Zentdiff.size == 0:
                    Zentdiff=np.array([Diff])
            else:
                Zentdiff=np.append(Zentdiff,[Diff], axis=0)
        if Differences.size==0:
            Differences=np.array([Zentdiff])
        else:
            Differences=np.append(Differences,[Zentdiff], axis=0)
    return Differences
    

def EuklidLen(DiffVecs):
    DataArray=np.empty((0,int(DiffVecs[0].size/DiffVecs[0,0].size)))    #Berechnet die Euklidsche Länge der eingegebenen Abstandsvektoren
    for DataVecs in DiffVecs:
        ZentLengs =np.empty((0))  
        for SingleVec in DataVecs:            
            SqrSum=0
            for Wert in SingleVec:
                SqrSum=SqrSum+Wert**2
            SqrSum=SqrSum**0.5
            ZentLengs=np.append(ZentLengs,[SqrSum], axis=0)        
        DataArray = np.append(DataArray, [ZentLengs], axis=0)
    return DataArray


def getIndexOfS(LenArray):
    shortestLenArray=np.empty(0)
    for Lens in LenArray:
        smallest=np.argmin(Lens)
        shortestLenArray= np.append(shortestLenArray,[smallest], axis=0)
    return shortestLenArray




print(CalcDistancesVec(np.array([[5,7,1],[1,9,1],[1,4,1]]),np.array([[5,7,1],[4,5,1],[8,4,1],[2,1,1],[5,7,1]])))
print(EuklidLen(CalcDistancesVec(np.array([[5,7,1],[1,9,1],[1,4,1]]),np.array([[5,7,1],[4,5,1],[8,4,1],[2,1,1],[5,7,1]]))))
print(getIndexOfS(EuklidLen(CalcDistancesVec(np.array([[5,7,1],[1,9,1],[1,4,1]]),np.array([[5,7,1],[4,5,1],[8,4,1],[2,1,1],[5,7,1]])))))
                



