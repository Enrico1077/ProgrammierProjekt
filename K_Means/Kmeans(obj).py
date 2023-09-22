import Datenpunkt as dp
import numpy as np
import random


#Erzeugt "Count" viele "Demensions"dimensionale zufällige Datenpunkte mit Werten von 0 bis "MaxValue"
def randData(Count, Dimensions, MaxValue): 
    DataArray=[]
    for i in range(Count):
        Location=np.empty(0)
        for j in range(Dimensions):
                Location=np.append(Location,random.randrange(MaxValue))
        DataArray.append(dp.Datenpunkt(Location))
    return DataArray

#Berechnet die Euklidische Distanz zwischen zwei Datenpunkten gleicher Dimension
def EuklidDistance(Datenpunkt1, Datenpunkt2):    
    Loc1=Datenpunkt1.getPosition()
    Loc2=Datenpunkt2.getPosition()
    SqrLen=0
    for i in range(Loc1.size):
         SqrLen+=(Loc1[i]-Loc2[i])**2
    return (SqrLen**0.5)    

#Findet aus einem Array voller Datenpunkte die Mitte
def FindMid(Datenpunkte):
    Dims=Datenpunkte[0].getPosition().size
    MidPoint=np.zeros(Dims)
    for DataPoint in Datenpunkte:      
        for i in range(Dims):
            MidPoint[i]=(MidPoint[i]+DataPoint.getPosition()[i])
    for i in range(MidPoint.size):
             MidPoint[i]/=len(Datenpunkte)    
    return MidPoint

#Zuweisung der Datenpunkte zu den Zentroiden
def MatchDpZent(Datenpunkte, Zentroide):
    for Dp0 in Datenpunkte:
        minLen=EuklidDistance(Dp0,Zentroide[0])
        Dp0.setNextCentroid(Zentroide[0])
        for i in range(len(Zentroide)):
            aktLen=EuklidDistance(Dp0,Zentroide[i])
            if(minLen>aktLen):
                minLen=aktLen
                Dp0.setNextCentroid(Zentroide[i])

def newCentroids(Datenpunkte, Zentroide):
     for j in range(len(Zentroide)):
        MatchinDP=[]
        for Dp0 in Datenpunkte:
            if (Dp0.getNextCentroid()==Zentroide[j]):
                MatchinDP.append(Dp0)
        if len(MatchinDP)>0:
            Zentroide[j].setPosition(FindMid(MatchinDP))

def AverageMisstake(DatenPunkte):
    AvgMiss=0
    for Dp0 in DatenPunkte:
        AvgMiss+=EuklidDistance(Dp0,Dp0.getNextCentroid())
    AvgMiss/=len(DatenPunkte)
    return AvgMiss
    
     

####MainAblauf####

#Parameter
Anzahl=100
MaxValue=100
Dimension=2
Centroid_count=1
k=10

#Random-Werte
Datenpunkte=randData(Anzahl, Dimension, MaxValue)

#Start des Algorithmuses
Zentroide=randData(Centroid_count,Dimension, MaxValue)
for i in range(k):

    #Zuweisung der Datenpunkte zu den Zentroiden
    MatchDpZent(Datenpunkte,Zentroide)

    #Zentroide in die Mitte der zugewiesenden Datenpunkte setzen
    newCentroids(Datenpunkte,Zentroide)

    #Ergebnisse für aktuelles K
    print("Aktuelles Z = "+str(i+1))
    print("Allgemeiner Fehler = "+str(AverageMisstake(Datenpunkte)))
    
    
            
    
               







    
          
     
