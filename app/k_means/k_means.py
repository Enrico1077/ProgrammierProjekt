import enum
from . import datapoint as dp #
import numpy as np
import random
import matplotlib.pyplot as plt
import copy 
from . import data_handling #
import threading
import queue
from .parameter import KMeansParameter


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
        #ProzVerbes=((oldMiss-kMiss)/oldMiss)*100
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

        if oldMiss==0.0:
            break
        ProzVerbes=((oldMiss-kMiss)/oldMiss)*100
        if ProzVerbes<_ZykKrit:
            break


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
        #print("Wiederholung: "+str(j+1)+" Aktueller durschnittlicher Fehler: "+ str(curAvgMiss))
        if (avgMiss==-1 or (avgMiss>curAvgMiss)):
            avgMiss=curAvgMiss
            BestData=copy.deepcopy(_DataPoints)
        for Dp0 in _DataPoints:
            Dp0.setNextCentroid(None)

    print("k="+str(_k)+" Kleinster durschnittlicher Fehler= "+ str(avgMiss))

    return BestData, avgMiss



#---------------------------------------Multi-Processing--------------------------------------------------

def CompleteKmeansParalell(_Repeats,_autoZyk,_DataPoints,_Zyklen,_k,_Dimension,_MaxValueZet,_LenMes,_MinValueZet,_stopZyk,_ZykKrit):
    #m=multiprocessing.Manager()
    result_queue = queue.Queue()


    processes=[]
    for i in range (_Repeats):
        process = threading.Thread(target=KmeansRepeatProcess, args=(_autoZyk,copy.deepcopy(_DataPoints),_Zyklen,_k,_Dimension,_MaxValueZet,_LenMes,_MinValueZet,_stopZyk,_ZykKrit, result_queue))
        process.start()
        processes.append(process)
        print(f'Prozess {i} ist gestartet ')  

    for process in processes:
        process.join()

    best_result = None
    best_avg_distance = float('inf')

    while not result_queue.empty():
        result, avg_distance = result_queue.get()
        if avg_distance < best_avg_distance:
            best_result = result
            best_avg_distance = avg_distance

    print("k="+str(_k)+" Kleinster durschnittlicher Fehler= "+ str(best_avg_distance))
    return best_result, best_avg_distance


def KmeansRepeatProcess(_autoZyk,_DataPoints,_Zyklen,_k,_Dimension,_MaxValueZet,_LenMes,_MinValueZet,_stopZyk,_ZykKrit, result_queue):
    if _autoZyk==0:
            KmeansFesterZyk(_DataPoints,_Zyklen,_k,_Dimension,_MaxValueZet,_LenMes, _MinValueZet)
    else:
            KmeansAutoZyk(_DataPoints,_stopZyk,_k,_Dimension,_MaxValueZet,_LenMes,_ZykKrit, _MinValueZet)
    curAvgMiss=AverageMisstake(_DataPoints, _LenMes)
    result_queue.put((_DataPoints, curAvgMiss))  
    #print(str(os.getpid())+" | "+str(curAvgMiss))
    


def KmeansProcess(Repeats, autoZyk, Datenpunkte, Zyklen, k, Dimension, MaxValueZet, LenMes, MinValueZet, stopZyk, ZykKrit, results):
    result,avgDistance=CompleteKmeansParalell(Repeats, autoZyk, copy.deepcopy(Datenpunkte), Zyklen, k, Dimension, MaxValueZet, LenMes, MinValueZet, stopZyk, ZykKrit)
    results.put((result, avgDistance, k))


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------     
def kmeansMain(InputData, params: KMeansParameter):
####MainAblauf####

    #InputData-> Daten aus CSV/JASON Datei

    #Parameter
    IsRandom=0         # Falls "1" zufällige Datenpunkte, sonst Inport
    Anzahl=1000        #Anzahl von zufällig erzeugenten Testwerten
    MaxValue=100       #Maximaler Wert von zufälligen Werten
    MinValue=0
    Dimension=2         #Anzahl der Dimensionen von Werten bei zufälligen Werten

    multi=params.parallel_calculating             #Sollen k's parralel berechnet werden?
    simu=params.parallel_calculations             #Anzahl der parralelen Berechnungen für k

    k=params.k                              #Anzahl der Zentroide (k)
    Elbow=params.use_elbow                  #"0" für k Zentroide, "1" für Elbow verfahren
    maxK=params.max_centroids_abort         #Nach der Berechnung für "maxK" Zentroiden wird das Elbow-Verfahren abgebrochen
    inaccu=params.min_pct_elbow             #"inacu" beschreibt die benötigte prozentuale Abweichung um einen Elbow festzustellen 

    Zyklen=params.c                                 #Anzahl der Wiederholungen im Algorithmus
    autoZyk=params.auto_cycle                       #"0" für "Zyklen" Wiederholungen, "1" für "ZykKrit"
    ZykKrit=params.min_pct_auto_cycle               #Abbruch falls die prozentuale Verbesserung für die Wiederholung kleiner als "ZykKrit" ist
    stopZyk=params.max_auto_cycle_abort             #Abbruch nach "stopZyk" Wiederholungen auch wenn verbesserung nicht schlechter als "kKrit"

    Repeats=params.r                            #Anzahl der Wiederholungen mit unterschiedlichen Zentroiden
    LenMes=params.distance_matrix               #"0" für Euklid, "1" für Manhatten
    normali=params.norm_method                  #"0" für Keine, "1" für Min-Max-Normalisierung, "2" für z-Normalisierung

    if IsRandom==1:
        Datenpunkte=randData(Anzahl, Dimension, MaxValue, MinValue)
    else:
        Datenpunkte =data_handling.getAPIData(InputData) 
        #Datenpunkte = DataHandling.getData("app\K_Means\Examples\Example_Programmierprojekt.csv","c")
        Dimension=Datenpunkte[0].getPosition().size

    if(normali==1):
        MinMaxNorm(Datenpunkte)
    elif(normali==2):
        z_Norm(Datenpunkte)  


    MaxValueZet=maxLocation(Datenpunkte)
    MinValueZet=minLocation(Datenpunkte)
    bestDp=None
    avgDistance=None
    outK=-1

    if Elbow==0:
        bestDp,avgDistance=CompleteKmeansParalell(Repeats, autoZyk,Datenpunkte, Zyklen, k, Dimension, MaxValueZet, LenMes, MinValueZet, stopZyk, ZykKrit)
        outK=k
    elif(Elbow==1 and multi==0):

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

    else:       #multiprozessing elbow
        aktElbow=False
        resultDict=dict()
        for j in range(0,(int(maxK/simu)+1)):

            if aktElbow:
                break
            
            #m=multiprocessing.Manager()
            results=queue.Queue()
            processPool=[]
            for i in range(1,simu+1):
                process=threading.Thread(target=KmeansProcess, args=(Repeats, autoZyk, Datenpunkte, Zyklen, (j*simu+i), Dimension, MaxValueZet, LenMes, MinValueZet, stopZyk, ZykKrit, results))
                process.start()
                processPool.append(process)
           
            for process in processPool:
                process.join()

            print('Ordnen')

            while not results.empty():
                result_data, aktAvgDistance, k = results.get()
                resultDict[k]=(result_data, aktAvgDistance)

            print('Dict')
            print(j*simu)
            print((j+1)*simu)
            for i in range(j*simu,(j+1)*simu):
                if(i<3):
                    continue
                result_data,aktAvgDistance=resultDict[i]
                egal, oldAvgDistance=resultDict[i-1]
                egal, olderAvgDistance=resultDict[i-2]
                gradient=oldAvgDistance-olderAvgDistance
                gradient*=(1+(inaccu/100))
                print(f'k={i} -> Avg. Misstake= {aktAvgDistance}')
                print("Steigung: "+str(gradient)+" | Next DP > "+str(oldAvgDistance+gradient))

                if (oldAvgDistance+gradient)>=aktAvgDistance:
                        bestDp=result_data
                        avgDistance=aktAvgDistance 
                        outK=i                
                        print("Elbow bei k= "+str(i))
                        aktElbow=True
                        break
                
            if outK == -1:
                outK=maxK 
                         
            bestDp=result_data
            avgDistance=aktAvgDistance




        


#------Ergebnis to Dict-Array-------    
    #return bestDp
    Output=[]
    InfoLine=dict([])
    InfoLine["k"]=str(outK)
    InfoLine["avgDistance"]=str(avgDistance)
    Output.append(InfoLine)
    Output.append(data_handling.dpToJson(bestDp))

    return Output
    





        
    
    
            
         
     
