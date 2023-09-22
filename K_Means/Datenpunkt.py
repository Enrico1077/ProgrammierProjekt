import numpy as np

class Datenpunkt():


    #Methoden 
    def __init__(self, position):
        self.__position=position
        self.__nextCentroid=None
    
    def getPosition(self):
        return self.__position
    
    def getNextCentroid(self):
        return self.__nextCentroid
    
    def setPosition(self,position):
        self.__position=position

    def setNextCentroid(self, Centroid):
         self.__nextCentroid = Centroid
        
