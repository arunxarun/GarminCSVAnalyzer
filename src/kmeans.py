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
        loRanges = {}
        hiRanges = {}
        
            
        for summaryData in summaryDatas:
            '''
            self.totalDist = totalDist
            self.avgHR = avgHR
            self.netGained = netGained
            self.netLost = netLost
            self.timeSeconds = timeSeconds
            '''
            if(clusterdata.TOTAL_DIST not in loRanges):
                loRanges[clusterdata.TOTAL_DIST] = summaryData.totalDist
            elif(loRanges[clusterdata.TOTAL_DIST] > summaryData.totalDist):
                loRanges[clusterdata.TOTAL_DIST] = summaryData.totalDist
            
            if(clusterdata.TOTAL_DIST not in hiRanges):
                hiRanges[clusterdata.TOTAL_DIST] = summaryData.totalDist
            elif(hiRanges[clusterdata.TOTAL_DIST] < summaryData.totalDist):
                hiRanges[clusterdata.TOTAL_DIST] = summaryData.totalDist
            
            if(clusterdata.AVG_HR not in loRanges):
                loRanges[clusterdata.AVG_HR] = summaryData.avgHR
            elif(loRanges[clusterdata.AVG_HR] > summaryData.avgHR):
                loRanges[clusterdata.AVG_HR] = summaryData.avgHR
            
            if(clusterdata.AVG_HR not in hiRanges):
                hiRanges[clusterdata.AVG_HR] = summaryData.avgHR
            elif(hiRanges[clusterdata.AVG_HR] < summaryData.avgHR):
                hiRanges[clusterdata.AVG_HR] = summaryData.avgHR
            
            if(clusterdata.NET_GAINED not in loRanges):
                loRanges[clusterdata.NET_GAINED] = summaryData.netGained
            elif(loRanges[clusterdata.NET_GAINED] > summaryData.netGained):
                loRanges[clusterdata.NET_GAINED] = summaryData.netGained
            
            if(clusterdata.NET_GAINED not in hiRanges):
                hiRanges[clusterdata.NET_GAINED] = summaryData.netGained
            elif(hiRanges[clusterdata.NET_GAINED] < summaryData.netGained):
                hiRanges[clusterdata.NET_GAINED] = summaryData.netGained
                
            if(clusterdata.NET_LOST not in loRanges):
                loRanges[clusterdata.NET_LOST] = summaryData.netLost
            elif(loRanges[clusterdata.NET_LOST] > summaryData.netLost):
                loRanges[clusterdata.NET_LOST] = summaryData.netLost
            
            if(clusterdata.NET_LOST not in hiRanges):
                hiRanges[clusterdata.NET_LOST] = summaryData.netLost
            elif(hiRanges[clusterdata.NET_LOST] < summaryData.netLost):
                hiRanges[clusterdata.NET_LOST] = summaryData.netLost
            
            if(clusterdata.TIME not in loRanges):
                loRanges[clusterdata.TIME] = summaryData.timeSeconds
            elif(loRanges[clusterdata.TIME] > summaryData.timeSeconds):
                loRanges[clusterdata.TIME] = summaryData.timeSeconds
            
            if(clusterdata.TIME not in hiRanges):
                hiRanges[clusterdata.TIME] = summaryData.timeSeconds
            elif(hiRanges[clusterdata.TIME] < summaryData.timeSeconds):
                hiRanges[clusterdata.TIME] = summaryData.timeSeconds
                
            return loRanges,hiRanges
        