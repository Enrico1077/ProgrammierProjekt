import Datenpunkt as dp
import numpy as np
import random
import matplotlib.pyplot as plt
import copy 

#Erzeugt "Count" viele "Demensions"dimensionale zufällige Datenpunkte mit Werten von 0 bis "MaxValue"
def randData(Count, Dimensions, MaxVal, MinVal): 
    DataArray=[]
    for i in range(Count):
        Location=np.empty(0)
        for j in range(Dimensions):
                Location=np.append(Location,random.uniform(MinVal,MaxVal))
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
    maxLoc=DataPoints[0].getPosition()[0]
    for dp0 in DataPoints:
        aktLoc=dp0.getPosition()
        for i in range(aktLoc.size):
            if maxLoc<aktLoc[i]:
                maxLoc=aktLoc[1]
    return maxLoc

#Berechnet die minimalen Werte jeder Dimension 
def minLocation(DataPoints):
    minLoc=DataPoints[0].getPosition()[0]
    for dp0 in DataPoints:
        aktLoc=dp0.getPosition()
        for i in range(aktLoc.size):
            if minLoc>aktLoc[i]:
                minLoc=aktLoc[1]
    return minLoc

#Min-Max-Normalisiert die Datenpunkte
def MinMaxNorm(DataPoints):
    maxLoc=maxLocation(DataPoints)
    minLoc=minLocation(DataPoints)
    for dp0 in DataPoints:
        Locs=dp0.getPosition()
        for i in range(Locs.size):
            Locs[i]=((Locs[i]-minLoc)/(maxLoc-minLoc))
        dp0.setPosition(Locs)

#z-Normalisiert die Datenpunkte
def z_Norm(DataPoints):
    AllValues=np.empty(0)
    for dp0 in DataPoints:
        AllValues=np.append(AllValues,dp0.getPosition())
    avg=np.average(AllValues)
    stdab=np.std(AllValues)
    for dp0 in DataPoints:
        Locs=dp0.getPosition()
        for i in range(Locs.size):
            Locs[i]=((Locs[i]-avg)/stdab)
        dp0.setPosition(Locs)
    
    

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
def KmeansFestesK(_Datenpunkte, _k, _Centroid_count, _Dimension, _MaxValue, _LenMes, _MinValue):
    #Start des Algorithmuses
    Zentroide=randData(_Centroid_count,_Dimension, _MaxValue, _MinValue)
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
def KmeansAutoK(_Datenpunkte, _kstop, _Centroid_count, _Dimension, _MaxValue, _LenMes, _kKrit, _MinValue):
    #Start des Algorithmuses
    Zentroide=randData(_Centroid_count, _Dimension, _MaxValue, _MinValue)
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



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------     

####MainAblauf####

#Parameter
Anzahl=10000         #Anzahl von zufällig erzeugenten Testwerten
MaxValue=100       #Maximaler Wert von Zentroiden und zufälligen Werten
MinValue=0
Dimension=2         #Anzahl der Dimensionen von Werten und Zentroiden
Centroid_count=5   #Anzahl der Zentroide

k=20                #k (Anzahl der Wiederholungen im Algorithmus)
autoK=1             #"0" für k Wiederholungen, "1" für Elbow-Verfahren
kKrit=0.1           #Abbruch falls die prozentuale Verbesserung für die Wiederholung kleiner als "kKrit" ist (Elbow)
stopK=100           #Abbruch nach "stopK" Wiederholungen auch wenn verbesserung nicht schlechter als "kKrit"

Repeats=1           #Anzahl der Wiederholungen mit unterschiedlichen Zentroiden
LenMes=0            #"0" für Euklid, "1" für Manhatten
normali=0           #"0" für Keine, "1" für Min-Max-Normalisierung, "2" für z-Normalisierung

#Random-Werte(Datenpunkte)
Datenpunkte=randData(Anzahl, Dimension, MaxValue, MinValue)
if(normali==1):
    MinMaxNorm(Datenpunkte)
elif(normali==2):
    z_Norm(Datenpunkte)  


MaxValueZet=maxLocation(Datenpunkte)
MinValueZet=minLocation(Datenpunkte)
print(MaxValueZet)
print(MinValueZet)
avgMiss=-1
BestData=None

for j in range(Repeats):
    if autoK==0:
        KmeansFestesK(Datenpunkte,k,Centroid_count,Dimension,MaxValueZet,LenMes, MinValueZet)
    else:
        KmeansAutoK(Datenpunkte,stopK,Centroid_count,Dimension,MaxValueZet,LenMes,kKrit, MinValueZet)
    #Ergebnisse für die aktuelle Wiederholung mit unterschiedlichen Zentroiden
    curAvgMiss=AverageMisstake(Datenpunkte, LenMes)
    print("Wiederholung: "+str(j+1)+" Aktueller durschnittlicher Fehler: "+ str(curAvgMiss))
    if (avgMiss==-1 or (avgMiss>curAvgMiss)):
        avgMiss=curAvgMiss
        BestData=copy.deepcopy(Datenpunkte)
    for Dp0 in Datenpunkte:
        Dp0.setNextCentroid(None)

print("Kleinster durschnittlicher Fehler= "+ str(avgMiss))

if Dimension==2:
    visualize_clusters(BestData)
        
    
    
            
    
               







    
          
     
