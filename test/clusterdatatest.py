'''
Created on Jan 22, 2012

@author: jacoba100
'''
import unittest
from clusterdata import GarminLap
from clusterdata import ClusterData
from clusterdata import TrackPoint

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testNewLapFromTokens(self):
        string = '1,1,,2011-01-05T15:00:46Z,576.5800000,1609.3439941,3.3762498,179,113,132,Active,,Distance,"",'
        tokens = string.split(',')
        lap= GarminLap(tokens)
        self.assertFalse(None == lap)
        self.assertEquals('2011-01-05T15:00:46Z',lap.lap)
        self.assertEquals(1,lap.id)
        self.assertEquals(1,lap.activityId)
        self.assertEquals(ClusterData.metersToFeet(1609.3439941),lap.totalDistance)
        self.assertEquals(576.58,lap.totalTime)
        
    def testNewGarminLapFromAsGarminLap(self):
        lap1 = GarminLap.asLap(1,589,300,140, 100,200)
        
        self.assertFalse(None == lap1)
        self.assertEquals(1,lap1.lap)
        
        self.assertEquals(589,lap1.totalTime)
        self.assertEquals(ClusterData.metersToFeet(300),lap1.totalDistance)
        self.assertEquals(ClusterData.metersToFeet(100),lap1.netGained)
        self.assertEquals(ClusterData.metersToFeet(200),lap1.netLost)
        
    def testNewTrackPointFromTokens(self):
        string = '1,2011-01-05T15:00:46Z,47.5859201,-122.2451507,79.4460449,0.0000000,73,,Absent,'
        tokens = string.split(',')

        trackPoint = TrackPoint('foo',tokens)
        self.assertTrue(trackPoint != None)
        self.assertEquals(trackPoint.id,'foo')
        self.assertEquals(47.5859201,trackPoint.lat)
        self.assertEquals(-122.2451507,trackPoint.long)
        self.assertEquals(ClusterData.metersToFeet(79.4460449),trackPoint.altitude)
        
        
        string = '2,2011-01-05T15:16:46Z,,,,,,,,'
        tokens = string.split(',')
        try:
            trackPoint = TrackPoint('foo',tokens)
            self.assertFalse(True) # shouldn't have reached here!
        except Exception as ex:
            self.assertTrue(True)
            
   

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()