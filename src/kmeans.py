import sys
import logging
from clusterdata  import ClusterData



class KmeansClusterer:
    
    def __init__(self,centroidCt):
        self.logger = logging.getLogger('KmeansClusterer')
        self.logger.addHandler(logging.StreamHandler())
        self.centroidCt = centroidCt
        
    def cluster(self,dataFilter):
        
        centroids =  dataFilter.initializeCentroids(self.centroidCt)
        
        clustersByCentroid = {}
        keepGoing = True
        while(keepGoing == True):
            for data in dataFilter.allData:
                centroid = self.findClosestCentroid(dataFilter,centroids,data)
                if(centroid not in clustersByCentroid):
                    clustersByCentroid[centroid] = []
                clustersByCentroid[centroid].append(data)
                
            newCentroids = self.generateNewCentroidsFromClusters(centroids,clustersByCentroid)
            
            if(self.areCentroidsCloseEnough(dataFilter,centroids,newCentroids)):
                keepGoing = False
            else:
                centroids = newCentroids
                clustersByCentroid = {}    
                
            
        return clustersByCentroid
            

    def areCentroidsCloseEnough(self,dataFilter,oldCentroids,newCentroids):
        
        for i in range(0,len(oldCentroids)):
            if dataFilter.inErrorRange(oldCentroids[i], newCentroids[i]) == False:
                return False
            
        
        return True
            
            
            
        
    def findClosestCentroid(self,dataFilter,centroids,data):
        mindist = float(sys.maxint)
        closestCentroid = None
        for centroid in centroids:
            dist = centroid.distanceTo(data,dataFilter)
            if(dist < mindist):
                mindist = dist
                closestCentroid = centroid
                
                 
        return closestCentroid
    
    
    def generateNewCentroidsFromClusters(self,dataFilter,oldCentroids,clustersByCentroids):
        newCentroids = []
        i = 0
        for centroid in oldCentroids:
            if centroid in clustersByCentroids:
                dataByCluster = clustersByCentroids[centroid]
                newCentroids.append(dataFilter.createMeanCentroid(centroid.getId(),dataByCluster))
            else:
                clusterName = "cluster %d"%i
                newCentroids.append(dataFilter.generateRandomCentroid(clusterName))
            
            i += 1
    
        return newCentroids
        