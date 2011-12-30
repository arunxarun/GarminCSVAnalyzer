'''
Created on Dec 21, 2011

@author: jacoba100
'''
import unittest
import kmeans
import pickle
import clusterdata
import random

class Test(unittest.TestCase):

    def setUp(self):
        self.summaryDatas = self.loadSummaryDatas()
        
    def tearDown(self):
        pass
   
    def testInitializeRanges(self):
        km = kmeans.KmeansClusterer(4)
        mins, maxes = km.initializeRanges(self.summaryDatas)
        
        self.assertIsNotNone(mins)
        self.assertIsNotNone(maxes)
        self.assertEquals(clusterdata.SummaryData.DIMENSIONS,len(mins))
        self.assertEquals(clusterdata.SummaryData.DIMENSIONS,len(maxes))
        
        for i in range(0,clusterdata.SummaryData.DIMENSIONS):
            self.assertTrue(maxes[i] > mins[i])
        
        
    
    def testInitializeCentroids(self):
        
        km = kmeans.KmeansClusterer(4)
        mins, maxes = km.initializeRanges(self.summaryDatas)
        centroids = km.initializeCentroids(self.summaryDatas)
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
        
        
        
    
    def testFindClosestCentroid(self):
        
        pass
    
    def testGetRandomNumberInRange(self):
        pass
    
    
    
    
    def loadSummaryDatas(self):
        summaryDatas = None
        with open('../resources/objects.pyc') as f:
            summaryDatas = pickle.load(f)
            
        return summaryDatas
        