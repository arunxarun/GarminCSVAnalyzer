'''
Created on Jan 27, 2012

@author: jacoba100
'''
import random
import time
from kmeansprimitives import DataFilter
from kmeansprimitives import Parser
from clusterdata import GarminLap
from milesplitparser import MileSplitParser

ERROR_DIST = 1

'''
TODO: this is the class that fucks with the data. Use this class to do everything specific to get the data into a place where kmeans can dick with it. 
ALSO: extend this class from an abstract class. 
'''
class GarminDataFilter(DataFilter):
    TOTAL_DIST = 0
    AVG_HR = 1
    NET_GAINED = 2
    NET_LOST = 3
    TIME = 4
    GOODRECS = 5
    BADRECS = 6

    
    def __init__(self,parser):
        self.hiRanges = {}
        self.loRanges = {}
        self.centroids = []
        self.parser= parser
        
        self.assembledData = self.assembleData(parser)
        
        self.initializeRanges(self.assembledData)
        
        
    '''
    this method assembles the data we want to test from the 
    extracted parts. In this case we want to assemble total altitude gained and 
    total altitude lost from raw trackpoint data, for each lap.
    '''
        
    def assembleData(self,parser):
        laps = parser.getData(MileSplitParser.LAPS);
        tracksToLaps = parser.getData(MileSplitParser.TRACKSTOLAPS)
        tracks = parser.getData(MileSplitParser.TRACKPOINTS)
        
        lapToRawAltitude = {}
        
        # get altitude. 
        for track in tracks:
            lapId = tracksToLaps[track.trackId]
            lap = laps[lapId]
            if(lapToRawAltitude.has_key(lap) == False):
                lapToRawAltitude[lap] = []
            
            lapToRawAltitude[lap].append(track.altitude)
        
        # now that we have altitude readings for all trackpoints per lap,
        # aggregate the gains and losses between trackpoints. 
            
        for lap, lapData  in lapToRawAltitude.items():
            netGained= 0
            netLost = 0
            
            lastData = -1
            for data in lapData:
                if data > lastData and lastData != -1:
                    netGained += data - lastData
                elif data < lastData: 
                    netLost += lastData - data
                
                lastData = data
             
            lap.netGained = netGained
            lap.netLost = netLost    
        
        return laps.values()    
                
    def getAssembledData(self):
        return self.assembledData 
    
        
    def getNormalizedMeasure(self,scale,value,valueIndex):
        if valueIndex < 0 or valueIndex > 6:
            raise Exception("index %d out of valid [0-6] range"%valueIndex)
        
        
        
        totalRange = self.hiRanges[valueIndex] - self.loRanges[valueIndex]
        offSet = value - self.loRanges[valueIndex]
        
        value =  float(offSet)/totalRange
        return value*scale
    
        
    def inErrorRange(self,point1,point2):
        if(point1.distanceTo(point2,self) >= ERROR_DIST):
            return False
        else:
            return True
    
    
    def createMeanCentroid(self,clusterName,centroids):
        
        summaryTotalTime = 0.0
        summaryTotalDistance = 0.0
        summaryAvgHR = 0.0
        summaryNetGained = 0.0
        summaryNetLost = 0.0
        
        for data in centroids:
            summaryTotalTime += data.totalTime
            summaryTotalDistance += data.totalDistance
            summaryAvgHR += data.avgHR
            summaryNetGained += data.netGained
            summaryNetLost += data.netLost
            
            
        
        divisor = len(centroids)
        
        avgTime = summaryTotalTime/divisor
        avgDist = summaryTotalDistance/divisor
        avgHR = summaryAvgHR/divisor
        avgNetGained = summaryNetGained/divisor
        avgNetLost = summaryNetLost/divisor
        
        return GarminLap.asLap(clusterName,avgTime,avgDist,avgHR, avgNetGained,avgNetLost)
            
    
    
    def initializeCentroids(self,centroidCt):
        centroids = []
        
        for i in range(centroidCt):
            isTooClose = True
            newCentroid = None
            while isTooClose == True:
                newCentroid = self.generateRandomCentroid("centroid %d"%i)
                isTooClose = False
                
                for centroid in centroids:
                    if self.inErrorRange(centroid,newCentroid):
                        isTooClose = True
                        break
                    
            if newCentroid != None:
                centroids.append(newCentroid)
            else:
                raise Exception("null centroid generated!")
        
        
        return centroids

    def generateRandomCentroid(self,pointName):
        avgDist=  self.hiRanges[self.TOTAL_DIST] - self.loRanges[self.TOTAL_DIST]
        if avgDist != 0:
            avgDist = random.randrange(int(self.loRanges[self.TOTAL_DIST]),int(self.hiRanges[self.TOTAL_DIST]))
        
        avgHR = self.hiRanges[self.AVG_HR] - self.loRanges[self.AVG_HR]
        if avgHR != 0:
            avgHR = random.randrange(int(self.loRanges[self.AVG_HR]),int(self.hiRanges[self.AVG_HR]))
            
        avgGained =  self.hiRanges[self.NET_GAINED] - self.loRanges[self.NET_GAINED]
        if avgGained != 0:
            avgGained = random.randrange(int(self.loRanges[self.NET_GAINED]),int(self.hiRanges[self.NET_GAINED]))
            
        avgLost = self.hiRanges[self.NET_LOST] - self.loRanges[self.NET_LOST]
        if avgLost != 0:
            avgLost = random.randrange(int(self.loRanges[self.NET_LOST]),int(self.hiRanges[self.NET_LOST]))
        
        avgTime = self.hiRanges[self.TIME] - self.loRanges[self.TIME]
        if avgTime != 0:
            avgTime = random.randrange(int(self.loRanges[self.TIME]),int(self.hiRanges[self.TIME]))   
        
        return GarminLap.asLap(pointName,                                              
                 random.randrange(int(self.loRanges[self.TIME]),int(self.hiRanges[self.TIME])),
                 random.randrange(int(self.loRanges[self.TOTAL_DIST]),int(self.hiRanges[self.TOTAL_DIST])),
                 random.randrange(int(self.loRanges[self.AVG_HR]),int(self.hiRanges[self.AVG_HR])),
                 random.randrange(int(self.loRanges[self.NET_GAINED]),int(self.hiRanges[self.NET_GAINED])),
                 random.randrange(int(self.loRanges[self.NET_LOST]),int(self.hiRanges[self.NET_LOST]))
                )

    def initializeRanges(self,summaryDatas):
        for summaryData in summaryDatas:
            '''
            self.totalDistance = totalDistance
            self.avgHR = avgHR
            self.netGained = netGained
            self.netLost = netLost
            self.timeSeconds = timeSeconds
            '''
            if(self.TOTAL_DIST not in self.loRanges):
                self.loRanges[self.TOTAL_DIST] = summaryData.totalDistance
            
            if(self.loRanges[self.TOTAL_DIST] > summaryData.totalDistance):
                self.loRanges[self.TOTAL_DIST] = summaryData.totalDistance
            
            if(self.TOTAL_DIST not in self.hiRanges):
                self.hiRanges[self.TOTAL_DIST] = summaryData.totalDistance
            if(self.hiRanges[self.TOTAL_DIST] < summaryData.totalDistance):
                self.hiRanges[self.TOTAL_DIST] = summaryData.totalDistance
            
            if(self.AVG_HR not in self.loRanges):
                self.loRanges[self.AVG_HR] = summaryData.avgHR
            
            if(self.loRanges[self.AVG_HR] > summaryData.avgHR):
                self.loRanges[self.AVG_HR] = summaryData.avgHR
            
            if(self.AVG_HR not in self.hiRanges):
                self.hiRanges[self.AVG_HR] = summaryData.avgHR
            if(self.hiRanges[self.AVG_HR] < summaryData.avgHR):
                self.hiRanges[self.AVG_HR] = summaryData.avgHR
            
            if(self.NET_GAINED not in self.loRanges):
                self.loRanges[self.NET_GAINED] = summaryData.netGained
            if(self.loRanges[self.NET_GAINED] > summaryData.netGained):
                self.loRanges[self.NET_GAINED] = summaryData.netGained
            
            if(self.NET_GAINED not in self.hiRanges):
                self.hiRanges[self.NET_GAINED] = summaryData.netGained
            if(self.hiRanges[self.NET_GAINED] < summaryData.netGained):
                self.hiRanges[self.NET_GAINED] = summaryData.netGained
                
            if(self.NET_LOST not in self.loRanges):
                self.loRanges[self.NET_LOST] = summaryData.netLost
            if(self.loRanges[self.NET_LOST] > summaryData.netLost):
                self.loRanges[self.NET_LOST] = summaryData.netLost
            
            if(self.NET_LOST not in self.hiRanges):
                self.hiRanges[self.NET_LOST] = summaryData.netLost
            if(self.hiRanges[self.NET_LOST] < summaryData.netLost):
                self.hiRanges[self.NET_LOST] = summaryData.netLost
            
            if(self.TIME not in self.loRanges):
                self.loRanges[self.TIME] = summaryData.totalTime
            if(self.loRanges[self.TIME] > summaryData.totalTime):
                self.loRanges[self.TIME] = summaryData.totalTime
            
            if(self.TIME not in self.hiRanges):
                self.hiRanges[self.TIME] = summaryData.totalTime
            if(self.hiRanges[self.TIME] < summaryData.totalTime):
                self.hiRanges[self.TIME] = summaryData.totalTime
        
