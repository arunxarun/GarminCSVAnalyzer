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
        
        for i in range(self.centroidCt):
            centroids.append(clusterdata.SummaryData( 
                "centroid %d"%i,                                              
                random.randrange(int(loRanges[clusterdata.TOTAL_DIST]),int(hiRanges[clusterdata.TOTAL_DIST])),
                random.randrange(int(loRanges[clusterdata.AVG_HR]),int(hiRanges[clusterdata.AVG_HR])),
                random.randrange(int(loRanges[clusterdata.NET_GAINED]),int(hiRanges[clusterdata.NET_GAINED])),
                random.randrange(int(loRanges[clusterdata.NET_LOST]),int(hiRanges[clusterdata.NET_LOST])),
                random.randrange(int(loRanges[clusterdata.TIME]),int(hiRanges[clusterdata.TIME])),0,0)
            )
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
            
            if(loRanges[clusterdata.TOTAL_DIST] > summaryData.totalDist):
                loRanges[clusterdata.TOTAL_DIST] = summaryData.totalDist
            
            if(clusterdata.TOTAL_DIST not in hiRanges):
                hiRanges[clusterdata.TOTAL_DIST] = summaryData.totalDist
            if(hiRanges[clusterdata.TOTAL_DIST] < summaryData.totalDist):
                hiRanges[clusterdata.TOTAL_DIST] = summaryData.totalDist
            
            if(clusterdata.AVG_HR not in loRanges):
                loRanges[clusterdata.AVG_HR] = summaryData.avgHR
            
            if(loRanges[clusterdata.AVG_HR] > summaryData.avgHR):
                loRanges[clusterdata.AVG_HR] = summaryData.avgHR
            
            if(clusterdata.AVG_HR not in hiRanges):
                hiRanges[clusterdata.AVG_HR] = summaryData.avgHR
            if(hiRanges[clusterdata.AVG_HR] < summaryData.avgHR):
                hiRanges[clusterdata.AVG_HR] = summaryData.avgHR
            
            if(clusterdata.NET_GAINED not in loRanges):
                loRanges[clusterdata.NET_GAINED] = summaryData.netGained
            if(loRanges[clusterdata.NET_GAINED] > summaryData.netGained):
                loRanges[clusterdata.NET_GAINED] = summaryData.netGained
            
            if(clusterdata.NET_GAINED not in hiRanges):
                hiRanges[clusterdata.NET_GAINED] = summaryData.netGained
            if(hiRanges[clusterdata.NET_GAINED] < summaryData.netGained):
                hiRanges[clusterdata.NET_GAINED] = summaryData.netGained
                
            if(clusterdata.NET_LOST not in loRanges):
                loRanges[clusterdata.NET_LOST] = summaryData.netLost
            if(loRanges[clusterdata.NET_LOST] > summaryData.netLost):
                loRanges[clusterdata.NET_LOST] = summaryData.netLost
            
            if(clusterdata.NET_LOST not in hiRanges):
                hiRanges[clusterdata.NET_LOST] = summaryData.netLost
            if(hiRanges[clusterdata.NET_LOST] < summaryData.netLost):
                hiRanges[clusterdata.NET_LOST] = summaryData.netLost
            
            if(clusterdata.TIME not in loRanges):
                loRanges[clusterdata.TIME] = summaryData.timeSeconds
            if(loRanges[clusterdata.TIME] > summaryData.timeSeconds):
                loRanges[clusterdata.TIME] = summaryData.timeSeconds
            
            if(clusterdata.TIME not in hiRanges):
                hiRanges[clusterdata.TIME] = summaryData.timeSeconds
            if(hiRanges[clusterdata.TIME] < summaryData.timeSeconds):
                hiRanges[clusterdata.TIME] = summaryData.timeSeconds
                
        return loRanges,hiRanges
        