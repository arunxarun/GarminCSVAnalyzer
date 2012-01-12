import sys
import logging
from clusterdata  import ClusterData



class KmeansClusterer:
    
    def __init__(self,centroidCt):
        self.logger = logging.getLogger('KmeansClusterer')
        self.logger.addHandler(logging.StreamHandler())
        self.centroidCt = centroidCt
        
    def cluster(self,summaryDatas):
        if len(summaryDatas) < self.centroidCt:
            self.logger.error("exiting, less points than centroids")
            sys.exit()
       
            
        centroids,mins,maxes =  ClusterData.initializeCentroids(self.centroidCt,summaryDatas)
        
        clustersByCentroid = {}
        keepGoing = True
        while(keepGoing == True):
            for data in summaryDatas:
                centroid = self.findClosestCentroid(centroids,data,mins,maxes)
                if(centroid not in clustersByCentroid):
                    clustersByCentroid[centroid] = []
                clustersByCentroid[centroid].append(data)
                
            newCentroids = self.generateNewCentroidsFromClusters(centroids,clustersByCentroid,mins,maxes)
            
            if(self.areCentroidsCloseEnough(centroids,newCentroids,mins,maxes)):
                keepGoing = False
            else:
                centroids = newCentroids
                clustersByCentroid = {}    
                
            
        return clustersByCentroid
            

    def areCentroidsCloseEnough(self,oldCentroids,newCentroids,mins,maxes):
        
        for i in range(0,len(oldCentroids)):
            if ClusterData.inErrorRange(oldCentroids[i], newCentroids[i], mins,maxes) == False:
                return False
            
        
        return True
            
            
            
        
    def findClosestCentroid(self,centroids,data,mins,maxes):
        mindist = float(sys.maxint)
        closestCentroid = None
        for centroid in centroids:
            dist = centroid.distanceTo(data,mins,maxes)
            if(dist < mindist):
                mindist = dist
                closestCentroid = centroid
                
                 
        return closestCentroid
    
    
    def generateNewCentroidsFromClusters(self,oldCentroids,clustersByCentroids,mins,maxes):
        newCentroids = []
        i = 0
        for centroid in oldCentroids:
            if centroid in clustersByCentroids:
                dataByCluster = clustersByCentroids[centroid]
                newCentroids.append(ClusterData.createMeanCentroid(centroid.lap,dataByCluster))
            else:
                clusterName = "cluster %d"%i
                newCentroids.append(ClusterData.generateRandomSummaryData(clusterName,mins,maxes))
            
            i += 1
    
        return newCentroids
        