from . import Datenpunkt as dp 
import numpy as np
import random
import matplotlib.pyplot as plt
import copy 
from . import DataHandling 

#Erzeugt "Count" viele "Demensions"dimensionale zufällige Datenpunkte mit Werten von MinValue bis "MaxValue"
def randData(Count, Dimensions, MaxVal, MinVal): 
    DataArray=[]
    for i in range(Count):
        Location=np.empty(0)
        for j in range(Dimensions):
                Location=np.append(Location,random.uniform(MinVal,MaxVal))
        DataArray.append(dp.Datenpunkt(Location))
    return DataArray

#Erzeugt "Count" viele "Demensions"dimensionale zufällige Datenpunkte mit Werten von MinValue bis "MaxValue" für jede Dimension
def randArrData(Count, Dimensions, MaxVal, MinVal): 
    DataArray=[]
    for i in range(Count):
        Location=np.empty(0)
        for j in range(Dimensions):
                Location=np.append(Location,random.uniform(MinVal[j],MaxVal[j]))
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

#Zentroide werden in die Mitte der zugeordneten Datenpunkte gesetzt
def newCentroids(Datenpunkte, Zentroide):
     for j in range(len(Zentroide)):
        MatchinDP=[]
        for Dp0 in Datenpunkte:
            if (Dp0.getNextCentroid()==Zentroide[j]):
                MatchinDP.append(Dp0)
        if len(MatchinDP)>0:
            Zentroide[j].setPosition(FindMid(MatchinDP))

#Berechnet die maximalen Werte jeder Dimension 
def maxLocation(DataPoints):
    maxLoc=copy.deepcopy(DataPoints[0].getPosition())
    for dp0 in DataPoints:
        aktLoc=copy.deepcopy(dp0.getPosition())
        for i in range(aktLoc.size):
            if maxLoc[i]<aktLoc[i]:
                maxLoc[i]=aktLoc[i]
    return maxLoc

#Berechnet die minimalen Werte jeder Dimension 
def minLocation(DataPoints):
    minLoc=copy.deepcopy(DataPoints[0].getPosition())
    for dp0 in DataPoints:
        aktLoc=copy.deepcopy(dp0.getPosition())
        for i in range(aktLoc.size):
            if minLoc[i]>aktLoc[i]:
                minLoc[i]=aktLoc[i]
    return minLoc

#Min-Max-Normalisiert die Datenpunkte
def MinMaxNorm(DataPoints):
    maxLoc=maxLocation(DataPoints)
    minLoc=minLocation(DataPoints)
    for dp0 in DataPoints:
        Locs=copy.deepcopy(dp0.getPosition()).astype(np.float64)
        for i in range(Locs.size):
            if minLoc[i]==maxLoc[i]:
                Locs[i]=1.0
            else:
                Locs[i]=((Locs[i]-minLoc[i])/(maxLoc[i]-minLoc[i]))
        dp0.setPosition(Locs)

#z-Normalisiert die Datenpunkte
def z_Norm(DataPoints):
    avg=FindMid(DataPoints) 
    allValues=retAllPos(DataPoints)
    stdArray=[]
    for i in range (allValues[0].size):
        stdArray.append(np.std(allValues[:,i]))
    for dp0 in DataPoints:
        Locs=copy.deepcopy(dp0.getPosition()).astype(np.float64)
        for i in range(Locs.size):
            if stdArray[i]==0:
                Locs[i]=0.0
            else:
                Locs[i]=float((Locs[i]-avg[i])/stdArray[i])
        dp0.setPosition(Locs)

#Gibt ein 2d-Array zurück in welchem die Positionen eines jeden Datenpunktes aufgelistet sind  
def retAllPos(DatapPoints):
    allPos=[]
    for dp0 in DatapPoints:
        allPos.append(dp0.getPosition())
    return np.array(allPos)

#Brechnet den Durchschnittlichen Abstand zwischen Datenpunkten und dem zugeordneten Zentruid
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
def KmeansFesterZyk(_Datenpunkte, _Zyklen, _k, _Dimension, _MaxValue, _LenMes, _MinValue):
    #Start des Algorithmuses
    Zentroide=randArrData(_k,_Dimension, _MaxValue, _MinValue)
    for i in range(_Zyklen):

        #Zuweisung der Datenpunkte zu den Zentroiden
        MatchDpZent(_Datenpunkte,Zentroide,_LenMes)

        #Berechnung des alten allgemeinen Fehlers
        oldMiss=AverageMisstake(_Datenpunkte, _LenMes)

        #Zentroide in die Mitte der zugewiesenden Datenpunkte setzen
        newCentroids(_Datenpunkte,Zentroide)

        #Berechnung der prozendtualen Abnahme des Fehlers
        kMiss=AverageMisstake(_Datenpunkte, _LenMes)
        ProzVerbes=((oldMiss-kMiss)/oldMiss)*100
        #print("Zyklus= "+str(i+1)+" Verbesserung in %: "+str(ProzVerbes))
        
    

#kMeans-Agorithmus mit dem ZykKrit-Wiederholungen
def KmeansAutoZyk(_Datenpunkte, _Zykstop, _k, _Dimension, _MaxValue, _LenMes, _ZykKrit, _MinValue):
    #Start des Algorithmuses
    Zentroide=randArrData(_k, _Dimension, _MaxValue, _MinValue)
    for i in range(_Zykstop):

        #Zuweisung der Datenpunkte zu den Zentroiden
        MatchDpZent(_Datenpunkte,Zentroide,_LenMes)

        #Berechnung des alten allgemeinen Fehlers
        oldMiss=AverageMisstake(_Datenpunkte, _LenMes)

        #Zentroide in die Mitte der zugewiesenden Datenpunkte setzen
        newCentroids(_Datenpunkte,Zentroide)

        #Berechnung der prozendtualen Abnahme des Fehlers
        kMiss=AverageMisstake(_Datenpunkte, _LenMes)
        ProzVerbes=((oldMiss-kMiss)/oldMiss)*100
        print("Zyklus= "+str(i+1)+" Verbesserung in %: "+str(ProzVerbes))
        if ProzVerbes<_ZykKrit:
            break

#---------------------Methode von Chat-GPT zum Testen(Visualisieren)---------------------------------------------

def visualize_clusters(data_points):
    # Extrahieren Sie die Positionen der Datenpunkte und ihre Cluster-Zuordnungen
    positions = np.array([dp.getPosition() for dp in data_points])
    cluster_ids = [dp.getNextCentroid().getPosition() if dp.getNextCentroid() is not None else None for dp in data_points]

    # Erstellen Sie eine Liste von eindeutigen Cluster-IDs
    unique_clusters = np.unique(cluster_ids, axis=0)

    # Erstellen Sie eine Farbpalette für die Cluster
    colors = plt.cm.get_cmap('tab10', len(unique_clusters))

    # Erstellen Sie ein Streudiagramm für die Datenpunkte und verwenden Sie Farben basierend auf den Clustern
    for i, cluster_id in enumerate(unique_clusters):
        # Filtern Sie die Datenpunkte, die zu diesem Cluster gehören
        cluster_indices = [j for j, c_id in enumerate(cluster_ids) if np.array_equal(c_id, cluster_id)]
        cluster_points = positions[cluster_indices]

        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], label=f'Cluster {i}', c=colors(i), alpha=0.5, marker='o')

    # Extrahieren Sie die Positionen der Zentroide aus den Datenpunkten
    centroid_positions = np.array([dp.getNextCentroid().getPosition() for dp in data_points if dp.getNextCentroid() is not None])

    # Fügen Sie die Zentroide hinzu
    plt.scatter(centroid_positions[:, 0], centroid_positions[:, 1], marker='x', color='red', s=100, label='Zentroide')

    plt.xlabel('X-Achse')
    plt.ylabel('Y-Achse')
    plt.title('k-Means Clustering Ergebnisse mit Farben pro Cluster und Zentroiden')

    # Fügen Sie eine Legende hinzu
    plt.legend()

    # Zeigen Sie das Diagramm an
    plt.show()


def CompleteKmeans(_Repeats,_autoZyk,_DataPoints,_Zyklen,_k,_Dimension,_MaxValueZet,_LenMes,_MinValueZet,_stopZyk,_ZykKrit):
    avgMiss=-1
    BestData=None

    for j in range(_Repeats):
        if _autoZyk==0:
            KmeansFesterZyk(_DataPoints,_Zyklen,_k,_Dimension,_MaxValueZet,_LenMes, _MinValueZet)
        else:
            KmeansAutoZyk(_DataPoints,_stopZyk,_k,_Dimension,_MaxValueZet,_LenMes,_ZykKrit, _MinValueZet)
        #Ergebnisse für die aktuelle Wiederholung mit unterschiedlichen Zentroiden
        curAvgMiss=AverageMisstake(_DataPoints, _LenMes)
        print("Wiederholung: "+str(j+1)+" Aktueller durschnittlicher Fehler: "+ str(curAvgMiss))
        if (avgMiss==-1 or (avgMiss>curAvgMiss)):
            avgMiss=curAvgMiss
            BestData=copy.deepcopy(_DataPoints)
        for Dp0 in _DataPoints:
            Dp0.setNextCentroid(None)

    print("Kleinster durschnittlicher Fehler= "+ str(avgMiss))

    return BestData, avgMiss



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------     
def kmeansMain(InputData, Elbow=1, k=1 ,maxK=100 , inaccu=0 , Zyklen=10 , autoZyk=1 , ZykKrit=0.5 , stopZyk=25 , Repeats=5 , LenMes=0 , normali=2):
####MainAblauf####

    #InputData-> Daten aus CSV/JASON Datei

    #Parameter
    IsRandom=1         # Falls "1" zufällige Datenpunkte, sonst Inport
    Anzahl=1000        #Anzahl von zufällig erzeugenten Testwerten
    MaxValue=100       #Maximaler Wert von zufälligen Werten
    MinValue=0
    Dimension=2         #Anzahl der Dimensionen von Werten bei zufälligen Werten

    #k=10                #Anzahl der Zentroide (k)
    #Elbow=1             #"0" für k Zentroide, "1" für Elbow verfahren
    #maxK=100            #Nach der Berechnung für "maxK" Zentroiden wird das Elbow-Verfahren abgebrochen
    #inaccu=0            #"inacu" beschreibt die benötigte prozentuale Abweichung um einen Elbow festzustellen 

    #Zyklen=10           #Anzahl der Wiederholungen im Algorithmus
    #autoZyk=1           #"0" für "Zyklen" Wiederholungen, "1" für "ZykKrit"
    #ZykKrit=0.5         #Abbruch falls die prozentuale Verbesserung für die Wiederholung kleiner als "ZykKrit" ist
    #stopZyk=25          #Abbruch nach "stopZyk" Wiederholungen auch wenn verbesserung nicht schlechter als "kKrit"

    #Repeats=5          #Anzahl der Wiederholungen mit unterschiedlichen Zentroiden
    #LenMes=0            #"0" für Euklid, "1" für Manhatten
    #normali=2           #"0" für Keine, "1" für Min-Max-Normalisierung, "2" für z-Normalisierung


    if IsRandom==1:
        Datenpunkte=randData(Anzahl, Dimension, MaxValue, MinValue)
    else:
        Datenpunkte =DataHandling.getAPIData(InputData)
        Dimension=Datenpunkte[0].getPosition().size

    if(normali==1):
        MinMaxNorm(Datenpunkte)
    elif(normali==2):
        z_Norm(Datenpunkte)  


    MaxValueZet=maxLocation(Datenpunkte)
    MinValueZet=minLocation(Datenpunkte)
    print(MaxValueZet)
    print(MinValueZet)
    bestDp=None
    avgDistance=None
    outK=None

    if Elbow==0:
        bestDp,avgDistance=CompleteKmeans(Repeats, autoZyk, Datenpunkte, Zyklen, k, Dimension, MaxValueZet, LenMes, MinValueZet, stopZyk, ZykKrit)
        outK=k
    else:

    
        DistHistroy=[]
        for i in range(1,maxK):
            result,avgDistance=CompleteKmeans(Repeats, autoZyk, Datenpunkte, Zyklen, i, Dimension, MaxValueZet, LenMes, MinValueZet, stopZyk, ZykKrit)
            DistHistroy.append(avgDistance)
            outK=i
            print("k="+str(i)+" avg. Distance: "+str(avgDistance))
        

            if len(DistHistroy)>2:
                gradient=DistHistroy[len(DistHistroy)-2]-DistHistroy[len(DistHistroy)-3]
                gradient*=(1+(inaccu/100))
                print("Steigung: "+str(gradient)+" | Next DP > "+str(DistHistroy[len(DistHistroy)-2]+gradient))

                if ((DistHistroy[len(DistHistroy)-2]+gradient)>=DistHistroy[len(DistHistroy)-1]):
                    bestDp=result
                    avgDistance=DistHistroy[len(DistHistroy)-2]                    
                    print("Elbow bei k= "+str(i))
                    break

            bestDp=result

#------Ergebnis to Dict-Array-------    
   
    Output=[]
    InfoLine=dict([])
    InfoLine["k"]=str(outK)
    InfoLine["avgDistance"]=str(avgDistance)
    Output.append(InfoLine)
    Output.append(DataHandling.dpToJson(bestDp))

    return Output
    






        
    
    
            
         
     
