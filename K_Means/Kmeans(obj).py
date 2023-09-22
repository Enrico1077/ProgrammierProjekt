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

def ManhattenDistance(Dp1,Dp2):
    Loc1=Dp1.getPosition()
    Loc2=Dp2.getPosition()
    Distance=0
    for i in range (Loc1.size):
        Distance+=abs(Loc1[i]-Loc2[i])
    return Distance


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
def MatchDpZent(Datenpunkte, Zentroide, Metric):
    for Dp0 in Datenpunkte:
        minLen=-1
        for i in range(len(Zentroide)):
            aktLen=-1
            if Metric==0:
                aktLen=EuklidDistance(Dp0,Zentroide[i])
            else:
                aktLen=ManhattenDistance(Dp0,Zentroide[i])
            if(minLen>aktLen or minLen==-1):
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

def AverageMisstake(DatenPunkte, Metric):
    AvgMiss=0
    for Dp0 in DatenPunkte:
        if Metric==0:
            AvgMiss+=EuklidDistance(Dp0,Dp0.getNextCentroid())
        else:
            AvgMiss+=ManhattenDistance(Dp0,Dp0.getNextCentroid())
    AvgMiss/=len(DatenPunkte)
    return AvgMiss

#kMeans-Agorithmus für ein Festes k (kein Elbow)
def KmeansFestesK(_Datenpunkte, _k, _Centroid_count, _Dimension, _MaxValue, _LenMes):
    #Start des Algorithmuses
    Zentroide=randData(_Centroid_count,_Dimension, _MaxValue)
    for i in range(_k):

        #Zuweisung der Datenpunkte zu den Zentroiden
        MatchDpZent(_Datenpunkte,Zentroide,_LenMes)

        #Berechnung des alten allgemeinen Fehlers
        oldMiss=AverageMisstake(_Datenpunkte, _LenMes)

        #Zentroide in die Mitte der zugewiesenden Datenpunkte setzen
        newCentroids(_Datenpunkte,Zentroide)

        #Berechnung der prozendtualen Abnahme des Fehlers
        kMiss=AverageMisstake(_Datenpunkte, LenMes)
        ProzVerbes=((oldMiss-kMiss)/oldMiss)*100
        print("k= "+str(i+1)+" Verbesserung in %: "+str(ProzVerbes))
    

#kMeans-Agorithmus mit dem Elbow-Verfahren
def KmeansAutoK(_Datenpunkte, _kstop, _Centroid_count, _Dimension, _MaxValue, _LenMes, _kKrit):
    #Start des Algorithmuses
    Zentroide=randData(_Centroid_count, _Dimension, _MaxValue)
    for i in range(_kstop):

        #Zuweisung der Datenpunkte zu den Zentroiden
        MatchDpZent(_Datenpunkte,Zentroide,_LenMes)

        #Berechnung des alten allgemeinen Fehlers
        oldMiss=AverageMisstake(_Datenpunkte, _LenMes)

        #Zentroide in die Mitte der zugewiesenden Datenpunkte setzen
        newCentroids(_Datenpunkte,Zentroide)

        #Berechnung der prozendtualen Abnahme des Fehlers
        kMiss=AverageMisstake(_Datenpunkte, LenMes)
        ProzVerbes=((oldMiss-kMiss)/oldMiss)*100
        print("k= "+str(i+1)+" Verbesserung in %: "+str(ProzVerbes))
        if ProzVerbes<_kKrit:
            break
     

####MainAblauf####

#Parameter
Anzahl=1000         #Anzahl von zufällig erzeugenten Testwerten
MaxValue=1000       #Maximaler Wert von Zentroiden und zufälligen Werten
Dimension=2         #Anzahl der Dimensionen von Werten und Zentroiden
Centroid_count=10   #Anzahl der Zentroide

k=10                #k (Anzahl der Wiederholungen im Algorithmus)
autoK=0             #"0" für k Wiederholungen, "1" für Elbow-Verfahren
kKrit=0.1           #Abbruch falls die prozentuale Verbesserung für die Wiederholung kleiner als "kKrit" ist (Elbow)
stopK=100           #Abbruch nach "stopK" Wiederholungen auch wenn verbesserung nicht schlechter als "kKrit"

Repeats=5           #Anzahl der Wiederholungen mit unterschiedlichen Zentroiden
LenMes=0            #0 für Euklid, 1 für Manhatten

#Random-Werte
Datenpunkte=randData(Anzahl, Dimension, MaxValue)

avgMiss=-1
BestData=None
for j in range(Repeats):
    if autoK==0:
        KmeansFestesK(Datenpunkte,k,Centroid_count,Dimension,MaxValue,LenMes)
    else:
        KmeansAutoK(Datenpunkte,stopK,Centroid_count,Dimension,MaxValue,LenMes,kKrit)
    #Ergebnisse für die aktuelle Wiederholung mit unterschiedlichen Zentroiden
    curAvgMiss=AverageMisstake(Datenpunkte, LenMes)
    print("Wiederholung: "+str(j+1)+" Aktueller durschnittlicher Fehler: "+ str(curAvgMiss))
    if (avgMiss==-1 or (avgMiss>curAvgMiss)):
        avgMiss=curAvgMiss
        BestData=Datenpunkte
    for Dp0 in Datenpunkte:
        Dp0.setNextCentroid(None)

print("Kleinster durschnittlicher Fehler= "+ str(avgMiss))
        
    
    
            
    
               







    
          
     
