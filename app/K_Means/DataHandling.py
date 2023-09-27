import Datenpunkt as dp
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

    #Dictionary -> FloatArray
    OutArray=[]
    for Zeile in DatenArray:
        vals=list(Zeile.values())
        newLine=[]
        for single in vals:
            newLine.append(float(single))
        OutArray.append(newLine)

    #FloatArray -> DataPoint-Array
    NewDataPoints=[]
    for Posi in OutArray:
        dp0= dp.Datenpunkt(np.array(Posi))
        NewDataPoints.append(dp0)

    return NewDataPoints









