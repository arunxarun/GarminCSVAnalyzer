'''
Created on Dec 21, 2011

@author: jacoba100
'''
import unittest
import kmeans
import pickle
import copy
import clusterdata

class Test(unittest.TestCase):

    def setUp(self):
        self.summaryDatas = self.loadSummaryDatas()
        pass
    def tearDown(self):
        pass
   
    def loadSummaryDatas(self):
        
        with open('../resources/objects.pyc') as f:
            summaryDatas = pickle.load(f)
            
        return summaryDatas

    
    def testFindClosestCentroid(self):
        km = kmeans.KmeansClusterer(4)
        centroids,mins,maxes = clusterdata.initializeCentroids(4,self.summaryDatas)
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
            
        
    