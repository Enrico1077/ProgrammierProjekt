from . import datapoint as dp #
import csv
import json
import numpy as np



#Dateityp: "c" für CSV , "j" für JSON
def getData(InputDatei, Dateityp):      
    
    #File -> Dictionary
    DatenArray=[]
    if Dateityp=="c":

        with open(InputDatei,'r') as csv_datei:
            csv_reader = csv.DictReader(csv_datei)
            for zeile in csv_reader:
                DatenArray.append(zeile)
    elif Dateityp=="j":
        with open(InputDatei, 'r') as datei:
            DatenArray = json.load(datei)

    #Dictionary -> Float-Array
    #print(DatenArray)
    OrdinaryDict=dict([])
    OutArray=[]
    for Zeile in DatenArray:
        vals=list(Zeile.values())
        newLine=[]
        for single in vals:
            try:
                newLine.append(float(single))
            except:
                if single in OrdinaryDict:
                    newLine.append(OrdinaryDict[single])
                else:
                    newVal=float(len(OrdinaryDict.values())+1)
                    OrdinaryDict[single]=newVal
                    newLine.append(newVal)
        OutArray.append(newLine)


    #FloatArray -> DataPoint-Array
    #print(OutArray)
    #print(OrdinaryDict)
    NewDataPoints=[]
    for Posi in OutArray:
        dp0= dp.Datenpunkt(np.array(Posi))
        NewDataPoints.append(dp0)

    return NewDataPoints



def getAPIData(DatenArray):      
      
    #Dictionary -> Float-Array
    OrdinaryDict=dict([])
    OutArray=[]
    for Zeile in DatenArray:
        vals=list(Zeile.values())
        newLine=[]
        for single in vals:
            try:
                newLine.append(float(single))
            except:
                if single in OrdinaryDict:
                    newLine.append(OrdinaryDict[single])
                else:
                    newVal=float(len(OrdinaryDict.values())+1)
                    OrdinaryDict[single]=newVal
                    newLine.append(newVal)
        OutArray.append(newLine)

    #FloatArray -> DataPoint-Array
    #print(OutArray)
    #print(OrdinaryDict)
    NewDataPoints=[]
    for Posi in OutArray:
        dp0= dp.Datenpunkt(np.array(Posi))
        NewDataPoints.append(dp0)

    #print("Klappt!")
    return NewDataPoints


def dpToJson(Datapoints):
    #DatenpunktArray->DictArray

    Output=[]
    for dp0 in Datapoints:
        posi=dp0.getPosition()
        curLine=dict([])
        for i in range(posi.size):
            curLine["PunktDimension"+str(i)]=posi[i]
        zentPosi=dp0.getNextCentroid().getPosition()
        for i in range(zentPosi.size):
            curLine["ZentDimension"+str(i)]=zentPosi[i]  
        Output.append(curLine)
    return(Output)







