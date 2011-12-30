'''
Created on Dec 21, 2011

@author: jacoba100
'''
import unittest
import kmeans
import pickle
import clusterdata

class Test(unittest.TestCase):

    def setUp(self):
        self.summaryDatas = self.loadSummaryDatas()
        pass
    def tearDown(self):
        pass
   
    def testInitializeRanges(self):
        km = kmeans.KmeansClusterer(4)
        mins, maxes = km.initializeRanges(self.summaryDatas)
        
        self.assertIsNotNone(mins)
        self.assertIsNotNone(maxes)
        self.assertEquals(clusterdata.SummaryData.DIMENSIONS,len(mins))
        self.assertEquals(clusterdata.SummaryData.DIMENSIONS,len(maxes))
        pass
    
    def testFindClosestCentroid(self):
        pass
    
    def testGetRandomNumberInRange(self):
        pass
    
    def testInitializeCentroids(self):
        
        
        pass
    
    
    def loadSummaryDatas(self):
        summaryDatas = None
        with open('../resources/objects.pyc') as f:
            summaryDatas = pickle.load(f)
            
        return summaryDatas
        