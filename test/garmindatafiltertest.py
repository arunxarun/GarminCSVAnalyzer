'''
Created on Jan 27, 2012

@author: jacoba100
'''
import unittest
from garmindatafilter import GarminDataFilter
from milesplitparser import MileSplitParser
from clusterdata import GarminLap
import datetime
import clusterdata

class Test(unittest.TestCase):


    '''
    make sure that all data gets netGained and netLost set
    '''
    
    def testInitializeGarminDataFilter(self):
        
        parser = MileSplitParser()
        parser.loadData('../resources/test.csv')
        gdf = GarminDataFilter(parser)
        self.assertNotEqual(None,gdf)
        assembledData = gdf.getAssembledData()
        self.assertNotEqual(None,assembledData)
        self.assertEqual(11,len(assembledData))
        
        for data in assembledData:
            self.assertNotEqual(clusterdata.UNSET,data.netGained)
            self.assertNotEqual(clusterdata.UNSET,data.netLost)
    
   
    def testGetNormalizedMeasure(self):
        parser = MileSplitParser()
        parser.loadData('../resources/test.csv')
        gdf = GarminDataFilter(parser)
        self.assertNotEqual(None,gdf)
        
        lo = gdf.loRanges[3]
        hi = gdf.hiRanges[3]
        
        range  = hi - lo
        val = lo + range/2
        
        
        retVal = gdf.getNormalizedMeasure(100, val, 3)
        
        self.assertEquals(50.0,retVal)
        

    def testInErrorRange(self):
        parser = MileSplitParser()
        parser.loadData('../resources/test.csv')
        gdf = GarminDataFilter(parser)
        self.assertNotEqual(None,gdf)
        
        lap1 = GarminLap.asLap(1,600,100,120,12,30)
        
        lap2 = GarminLap.asLap(2,400,300,150,123,300)
        
        
        self.assertFalse(gdf.inErrorRange(lap1, lap2))
        
        
        lap1 = GarminLap.asLap(1,600,100,120,12,30)
        
        lap2 = GarminLap.asLap(2,600,100,120,12,30)
        
        
        self.assertTrue(gdf.inErrorRange(lap1, lap2))
        
    def testGenerateRandomCentroids(self):
        parser = MileSplitParser()
        parser.loadData('../resources/test.csv')
        gdf = GarminDataFilter(parser)
        self.assertNotEqual(None,gdf)
        
        cent1 = gdf.generateRandomCentroid("foobar")
        
        cent2 = gdf.generateRandomCentroid("foobar1")

        self.assertFalse(gdf.inErrorRange(cent1, cent2))
     
    def testInitializeCentroids(self):
        parser = MileSplitParser()
        parser.loadData('../resources/test.csv')
        gdf = GarminDataFilter(parser)
        self.assertNotEqual(None,gdf)
        
        centroids = gdf.initializeCentroids(4)
        
        self.assertEqual(4,len(centroids))
                         
        
                        

        
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()