'''
Created on Dec 21, 2011

@author: jacoba100
'''
import unittest
from milesplitparser import MileSplitParser
from clusterdata import ClusterData
import pickle

class Test(unittest.TestCase):


    def setUp(self):
        self.file = open('../resources/test.csv')
        keepProcessing = True
        while(keepProcessing):
            
            cur = self.file.readline()
            
            if(cur == ''):
                break
            cur = cur.rstrip('\n')
            if(cur == 'Activity Table'):
                self.activityParserPos = self.file.tell()
            elif (cur == 'ActivityLap Table'):
                self.lapParserPos = self.file.tell()
            elif (cur == 'Track Table'):
                self.trackParserPos = self.file.tell()
            elif (cur == 'TrackPoint Table'):
                self.trackPointParserPos = self.file.tell()
            
        self.actToId = None
        self.activityHasLaps = None
        self.lapHasTracks = None
        self.lapHasPoints = None

    def tearDown(self):
        self.file.close()
        pass


    def testActivityParser(self):
        msp = MileSplitParser()
        self.file.seek(self.activityParserPos,0)
        activitiesToIds = msp.getActivityIDs(self.file, [])
            
        self.assertTrue(activitiesToIds != None)
        
        self.assertEquals(1,len(activitiesToIds))
        
            
        self.file.seek(self.activityParserPos,0)
        activitiesToIds = msp.getActivityIDs(self.file, ['Biking'])
        
        self.assertTrue(activitiesToIds != None)
        
        self.assertEquals(1,len(activitiesToIds))
        
        self.file.seek(self.activityParserPos,0)
        activitiesToIds = msp.getActivityIDs(self.file, ['Running'])
        
        self.assertTrue(activitiesToIds != None)
        
        self.assertEquals(0,len(activitiesToIds))
        
    def testGetLaps(self):
        msp = MileSplitParser()
        self.file.seek(self.lapParserPos,0)
        laps = msp.getLaps(self.file)
        
        self.assertFalse(laps == None)
        self.assertTrue(11,len(laps))
        lap0 = laps[0]
        self.assertEquals(1,lap0.id)
        self.assertEquals('2011-01-05T15:00:46Z',lap0.lap)    
        lap11 = laps[10]
        self.assertEquals(11,lap11.id)
        self.assertEquals(1,lap11.activityId)
        
        self.file.seek(self.lapParserPos,0)
        laps = msp.getLaps(self.file,True) # exclude manual laps
        self.assertFalse(laps == None)
        self.assertTrue(2,len(laps))
        
        
    def testGetLapsToTracks(self):
        
        msp = MileSplitParser()
        self.file.seek(self.lapParserPos,0)
        laps = msp.getLaps(self.file)
        self.file.seek(self.trackParserPos)
        lapsToTracks = msp.getLapsToTracks(self.file, laps)
        
        self.assertFalse(lapsToTracks == None)
        self.assertEquals(11,len(lapsToTracks))
        
        self.assertFalse(lapsToTracks[1] == None)
        ltt1 = lapsToTracks[1]
        self.assertEquals(1,len(ltt1))
        self.assertEquals(1,ltt1[0])
        
        ltt2 = lapsToTracks[2]
        self.assertEquals(2,len(ltt2))
        self.assertEquals(2,ltt2[0])
        self.assertEquals(3,ltt2[1])

    def testGetTrackPoints(self):
        self.file.seek(self.trackPointParserPos,0)
        msp = MileSplitParser()
        trackPoints = msp.getTrackPoints(self.file)
        self.assertTrue(trackPoints != None)
        tp1= trackPoints[0]
        
        #1,2011-01-05T15:00:46Z,47.5859201,-122.2451507,79.4460449,0.0000000,73,,Absent,
        self.assertEquals(ClusterData.toDateTime('2011-01-05T15:00:46Z'),tp1.time)
        
        self.assertEquals(47.5859201,tp1.lat)
        self.assertEquals(-122.2451507,tp1.long)
        self.assertEquals(ClusterData.metersToFeet(79.4460449),tp1.altitude)
        self.assertEquals(0,tp1.distance)
        self.assertEquals(73,tp1.heartRate)
       
         
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()