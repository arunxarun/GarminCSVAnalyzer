'''
Created on Dec 21, 2011

@author: jacoba100
'''
import unittest
import kmeans
import pickle
import copy
from clusterdata import ClusterData
import clusterdata
class Test(unittest.TestCase):

    def setUp(self):
        self.summaryDatas = self.loadLapDatas()
    def tearDown(self):
        pass
   
    def loadLapDatas(self):
        
        
        with open('../resources/objects.pyc') as f:
            summaryDatas = pickle.load(f)
            
        return summaryDatas

    
    def testFindClosestCentroid(self):
        km = kmeans.KmeansClusterer(4)
        
        centroids,mins,maxes = ClusterData.initializeCentroids(4,self.summaryDatas)
        
        self.assertEquals(4,len(centroids))
        
        for centroid in centroids:
            self.assertTrue(centroid.totalDist >= mins[clusterdata.TOTAL_DIST])
            self.assertTrue(centroid.totalDist <= maxes[clusterdata.TOTAL_DIST])
            
            self.assertTrue(centroid.avgHR >= mins[clusterdata.AVG_HR])
            self.assertTrue(centroid.avgHR <= maxes[clusterdata.AVG_HR])
            
            self.assertTrue(centroid.netGained >= mins[clusterdata.NET_GAINED])
            self.assertTrue(centroid.netGained <= maxes[clusterdata.NET_GAINED])
        
            self.assertTrue(centroid.netLost >= mins[clusterdata.NET_LOST])
            self.assertTrue(centroid.netLost <= maxes[clusterdata.NET_LOST])
            
            self.assertTrue(centroid.timeSeconds >= mins[clusterdata.TIME])
            self.assertTrue(centroid.timeSeconds <= maxes[clusterdata.TIME])
        
        
        centroids,mins,maxes = ClusterData.initializeCentroids(4,self.summaryDatas)
        self.assertEquals(4,len(centroids))
        
        # take the 4th centroid and clone it.
        
        data = copy.copy(centroids[3])
        centroid = km.findClosestCentroid(centroids, data,mins,maxes)
        
        '''
        self.lap = lap
        self.totalDist = totalDist
        self.avgHR = avgHR
        self.netGained = netGained
        self.netLost = netLost
        self.timeSeconds = timeSeconds
        self.goodRecords = goodRecords
        self.badRecords = badRecords
        '''
        self.assertEquals(centroid.lap,centroids[3].lap)
        self.assertEquals(centroid.totalDist,centroids[3].totalDist)
        self.assertEquals(centroid.avgHR,centroids[3].avgHR)
        self.assertEquals(centroid.netGained,centroids[3].netGained)
        self.assertEquals(centroid.netLost,centroids[3].netLost)
        self.assertEquals(centroid.timeSeconds,centroids[3].timeSeconds)
        self.assertEquals(centroid.goodRecords,centroids[3].goodRecords)
        self.assertEquals(centroid.badRecords,centroids[3].badRecords)
        self.assertEquals(centroid,centroids[3])
        pass
    
    
    def testCluster(self):
        
    
        km = kmeans.KmeansClusterer(4)
        
        clustersByCentroid = km.cluster(self.summaryDatas)
        
        self.assertFalse(clustersByCentroid == None)
        self.assertEqual(4,len(clustersByCentroid))
        
        for k,v in clustersByCentroid.items():
            
            self.assertTrue(len(v) > 0)
            
        
    
