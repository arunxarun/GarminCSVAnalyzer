'''
Created on Jan 24, 2012

@author: jacoba100
'''
class Parser:
    def __init__(self,isVerbose = False):
        raise NotImplementedError, "override in subclass!"
    
    def loadData(self,fileName):
        raise NotImplementedError, "override in subclass!"
    
    def getData(self,dataId):
        raise NotImplementedError, "override in subclass!"
    
class DataFilter:
    '''
    abstract base class (not using abc) for all data used by KMeans clusterer. 
    '''
    
    def initializeCentroids(self,centroidCt):
        raise NotImplementedError, "override in subclass!"
    
    def inErrorRange(self,point1,point2):
        raise NotImplementedError, "override in subclass!"
    
    def createMeanCentroid(self,clusterName,dataPoints):
        raise NotImplementedError, "override in subclass!"
    
    def generateRandomCentroid(self,pointName):
        raise NotImplementedError, "override in subclass!"
    
    def getNormalizedMeasure(self,scale,value,valueIndex):
        raise NotImplementedError, "override in subclass!"
    
class DataPoint:
    '''
    abstract base class for individual data points used by KMeans clusterer
    '''
    
    def distanceTo(self,otherDataPoint,dataFilter):
        raise NotImplementedError, "override in subclass!"
    
    def getId(self):
        raise NotImplementedError, "override in subclass!"
    
    def prettyPrint(self,separator = True):
        raise NotImplementedError, "override in subclass!"