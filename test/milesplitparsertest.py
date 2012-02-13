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
        self.file = open('../resources/January_Test.tsv')
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


    def testGetActivityIds(self):
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
        lap38 = laps[38]
        self.assertEquals(38,lap38.id)
        self.assertEquals('2011-01-05T15:00:46Z',lap38.lap)    
        lap48 = laps[48]
        self.assertEquals(48,lap48.id)
        self.assertEquals(4,lap48.activityId)
        
        self.file.seek(self.lapParserPos,0)
        laps = msp.getLaps(self.file,True) # exclude manual laps
        self.assertFalse(laps == None)
        self.assertTrue(2,len(laps))
        
        
    def testGetTracksToLaps(self):
        
        msp = MileSplitParser()
        self.file.seek(self.trackParserPos)
        tracksToLaps = msp.getTracksToLaps(self.file)
        
        self.assertFalse(tracksToLaps == None)
        self.assertEquals(16,len(tracksToLaps))
        
        startTrack = 0
        for track in tracksToLaps.keys():
            self.assertTrue(track > startTrack)
            startTrack = track

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
       
    def testLoadData(self):
        msp = MileSplitParser()
        msp.loadData('../resources/January_Test.tsv')
        laps = msp.getData(MileSplitParser.LAPS);
        self.assertNotEquals(None,laps)
        self.assertNotEquals(0,len(laps))
        
        for lap in laps.values():
            self.assertNotEqual(0,lap.id)
            self.assertNotEqual(0,lap.activityId)
            self.assertNotEqual(None,lap.lap)
            self.assertNotEqual(0,lap.totalTime)
            self.assertNotEqual(0,lap.totalDistance)
            self.assertNotEqual(0,lap.avgHR)
            
        lapsToTracks = msp.getData(MileSplitParser.TRACKSTOLAPS)
        self.assertNotEquals(None,lapsToTracks)
        self.assertNotEquals(0,len(lapsToTracks))
        
        trackPoints = msp.getData(MileSplitParser.TRACKPOINTS)
        self.assertNotEquals(None,trackPoints)
        self.assertNotEquals(0,len(trackPoints))
        
        for trackPoint in trackPoints:
            self.assertNotEquals(0,trackPoint.id)
            self.assertNotEquals(0,trackPoint.trackId)
            self.assertNotEquals(None,trackPoint.time)
            self.assertNotEquals(0,trackPoint.lat)
            self.assertNotEquals(0,trackPoint.long)
            
            self.assertNotEquals(0,trackPoint.altitude)
            self.assertNotEquals(0,trackPoint.heartRate)
        # TODO: more integrity checking
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()