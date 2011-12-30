import sys
import logging
import datetime
import clusterdata
import random



class KmeansClusterer:
    
    def __init__(self,centroidCt):
        self.logger = logging.getLogger('KmeansClusterer')
        self.logger.addHandler(logging.StreamHandler())
        self.centroidCt = centroidCt
        
        
    def initializeCentroids(self,summaryDatas):
        
        loRanges,hiRanges = self.initializeRanges(summaryDatas)
        
        centroids = []
        for i in range(clusterdata.SummaryData.DIMENSIONS):
            centroids[i] = random.randrange(loRanges[i],hiRanges[i]) 
        
        return centroids
    
    def cluster(self,summaryDatas):
        if len(summaryDatas) < self.centroidCt:
            self.logger.error("exiting, less points than centroids")
            sys.exit()
            
        centroids =  self.initializeCentroids(summaryDatas)
        
        clustersByCentroid = {}
        keepGoing = True
        while(keepGoing == True):
            for data in summaryDatas:
                centroid = self.findClosestCentroid(centroids,data)
                if(clustersByCentroid[centroid] == None):
                    clustersByCentroid[centroid] = []
                clustersByCentroid[centroid].append(data)
                
            newCentroids = self.generateCentroidsFromClusters(self.centroids)
            
            if(self.areCentroidsCloseEnough(centroids,newCentroids)):
                keepGoing = False
            else:
                centroids = newCentroids
                clustersByCentroid = {}    
                
            
        return clustersByCentroid
            

    def findClosestCentroid(self,centroids,data):
        return centroids[1] # stub code
            
    def initializeRanges(self,summaryDatas):
        loRanges = []
        hiRanges = []
        
        for i in range(clusterdata.SummaryData.DIMENSIONS):
            loRanges[i] = None
            hiRanges[i] = None
            
        for summaryData in summaryDatas:
            '''
            self.totalDist = totalDist
            self.avgHR = avgHR
            self.netGained = netGained
            self.netLost = netLost
            self.timeSeconds = timeSeconds
            '''
            if(loRanges[clusterdata.TOTAL_DIST] == None):
                loRanges[clusterdata.TOTAL_DIST] = summaryData.totalDist
            if(loRanges[clusterdata.TOTAL_DIST] > summaryData.totalDist):
                loRanges[clusterdata.TOTAL_DIST] = summaryData.totalDist
            
            if(hiRanges[clusterdata.TOTAL_DIST] == None):
                hiRanges[clusterdata.TOTAL_DIST] = summaryData.totalDist
            if(hiRanges[clusterdata.TOTAL_DIST] < summaryData.totalDist):
                hiRanges[clusterdata.TOTAL_DIST] = summaryData.totalDist
            
            if(loRanges[clusterdata.AVG_HR] == None):
                loRanges[clusterdata.AVG_HR] = summaryData.avgHR
            if(loRanges[clusterdata.AVG_HR] > summaryData.avgHR):
                loRanges[clusterdata.AVG_HR] = summaryData.avgHR
            
            if(hiRanges[clusterdata.AVG_HR] == None):
                hiRanges[clusterdata.AVG_HR] = summaryData.avgHR
            if(hiRanges[clusterdata.AVG_HR] < summaryData.avgHR):
                hiRanges[clusterdata.AVG_HR] = summaryData.avgHR
            
            if(loRanges[clusterdata.NET_GAINED] == None):
                loRanges[clusterdata.NET_GAINED] = summaryData.netGained
            if(loRanges[clusterdata.NET_GAINED] > summaryData.netGained):
                loRanges[clusterdata.NET_GAINED] = summaryData.netGained
            
            if(hiRanges[clusterdata.NET_GAINED] == None):
                hiRanges[clusterdata.NET_GAINED] = summaryData.netGained
            if(hiRanges[clusterdata.NET_GAINED] < summaryData.netGained):
                hiRanges[clusterdata.NET_GAINED] = summaryData.netGained
                
            if(loRanges[clusterdata.NET_LOST] == None):
                loRanges[clusterdata.NET_LOST] = summaryData.netLost
            if(loRanges[clusterdata.NET_LOST] > summaryData.netLost):
                loRanges[clusterdata.NET_LOST] = summaryData.netLost
            
            if(hiRanges[clusterdata.NET_LOST] == None):
                hiRanges[clusterdata.NET_LOST] = summaryData.netLost
            if(hiRanges[clusterdata.NET_LOST] < summaryData.netLost):
                hiRanges[clusterdata.NET_LOST] = summaryData.netLost
            
            if(loRanges[clusterdata.TIME] == None):
                loRanges[clusterdata.TIME] = summaryData.timeSeconds
            if(loRanges[clusterdata.TIME] > summaryData.timeSeconds):
                loRanges[clusterdata.TIME] = summaryData.timeSeconds
            
            if(hiRanges[clusterdata.TIME] == None):
                hiRanges[clusterdata.TIME] = summaryData.timeSeconds
            if(hiRanges[clusterdata.TIME] < summaryData.timeSeconds):
                hiRanges[clusterdata.TIME] = summaryData.timeSeconds
                
            return loRanges,hiRanges
        