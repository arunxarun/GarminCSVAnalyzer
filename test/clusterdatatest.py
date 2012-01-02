'''
Created on Dec 31, 2011

@author: jacoba100
'''
import unittest
import clusterdata
import pickle

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
        

    def testSummaryDataGetNormalizedMeasure(self):
        # totalDist,avgHR,netGained,netLost,timeSeconds,goodRecords,badRecords
        sd  = clusterdata.SummaryData("1",120,130,1400,1200,200,0,0)
        mins = [5,50,0,0,0]
        maxes = [150,160,1500,1500,360]
        
        myDist = sd.getNormalizedMeasure(100,sd.totalDist,mins[clusterdata.TOTAL_DIST],maxes[clusterdata.TOTAL_DIST])
        
        self.assertTrue(myDist >= mins[clusterdata.TOTAL_DIST])
        self.assertTrue(myDist <= maxes[clusterdata.TOTAL_DIST])
        
        self.assertEquals((float(115)/145)*100,myDist)
        pass


    def testSummaryDataDistanceTo(self):
        
        sd  = clusterdata.SummaryData("1",120,130,1400,1200,200,0,0)
        mins = [5,50,0,0,0]
        maxes = [150,160,1500,1500,360]
        
        
        sd2 = clusterdata.SummaryData("2",120,130,1400,1200,200,0,0)
        
        
        self.assertEquals(0, sd.distanceTo(sd2, mins, maxes))
        
        # probably need something a little beefier here as well
        
        
    def testInitializeRanges(self):
        mins, maxes = clusterdata.initializeRanges(self.summaryDatas)
        
        self.assertFalse(None == mins)
        self.assertFalse(None == maxes)
        self.assertEquals(clusterdata.SummaryData.DIMENSIONS,len(mins))
        self.assertEquals(clusterdata.SummaryData.DIMENSIONS,len(maxes))
        
        for i in range(0,clusterdata.SummaryData.DIMENSIONS):
            self.assertTrue(maxes[i] > mins[i])
        
    
    def testInitializeCentroids(self):
                
        centroids,mins,maxes = clusterdata.initializeCentroids(4,self.summaryDatas)
        self.assertFalse(centroids == None)
        self.assertFalse(mins == None)
        self.assertFalse(maxes == None)
        
        self.assertEquals(4,len(centroids))
        
    def testCreateMeanCentroid(self):
        mins,maxes = clusterdata.initializeRanges(self.summaryDatas)
        centroid = clusterdata.createMeanCentroid("foobar", self.summaryDatas)
        
        self.assertFalse(centroid == None)
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

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()