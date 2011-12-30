'''
Created on Dec 21, 2011

@author: jacoba100
'''
import unittest
import milesplitparser
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


    def testParseActivities(self):
        msp = milesplitparser.MileSplitParser()
        allFilters = []
        allFilters.append("Cycling")
        self.file.seek(self.activityParserPos)
        self.actToId = msp.parseActivities(self.file,allFilters)
        self.assertIsNotNone(self.actToId)
        self.assertEquals(1,len(self.actToId))
        self.assertIsNotNone(self.actToId['1'])
        assert(self.actToId['1'] == '2011-01-05T15:00:46Z')

    def testParseLaps(self):
        if(self.actToId == None):
            self.testParseActivities()
        msp = milesplitparser.MileSplitParser()
        self.file.seek(self.lapParserPos)
        self.activityHasLaps = msp.parseActivityLaps(self.file, self.actToId)
        self.assertIsNotNone(self.activityHasLaps)
        self.assertEquals(11,len(self.activityHasLaps['1']))
        
        
    def testParseTracks(self):
        if(self.actToId == None):
            self.testParseActivities()
        if(self.activityHasLaps == None):
            self.testParseLaps()
        
     
        msp = milesplitparser.MileSplitParser()
        self.file.seek(self.trackParserPos)
        self.lapHasTracks = msp.parseTracks(self.file,self.activityHasLaps)
        self.assertIsNotNone(self.lapHasTracks)
        self.assertEquals(11,len(self.lapHasTracks))
        
    def testParseTrackPoints(self):
        if(self.actToId == None):
            self.testParseActivities()
        if(self.activityHasLaps == None):
            self.testParseLaps()
        if(self.lapHasTracks == None):
            self.testParseTracks()
        
        self.file.seek(self.trackPointParserPos)
        msp = milesplitparser.MileSplitParser()
        self.lapHasPoints = msp.parseTrackPoints(self.file, self.lapHasTracks)
        self.assertIsNotNone(self.lapHasPoints)
        self.assertEquals(11,len(self.lapHasPoints))
        self.assertIsNotNone(self.lapHasPoints['1'])
        self.assertEquals(116,len(self.lapHasPoints['1']))
        
    def testGenerateLapData(self):
        if(self.actToId == None):
            self.testParseActivities()
        if(self.activityHasLaps == None):
            self.testParseLaps()
        if(self.lapHasTracks == None):
            self.testParseTracks()
        if(self.lapHasPoints == None):
            self.testParseTrackPoints()
            
        msp = milesplitparser.MileSplitParser()
        dataByLap = msp.generateLapData(self.activityHasLaps, self.lapHasPoints)
        self.assertIsNotNone(dataByLap)
        self.assertEquals(11,len(dataByLap))
        
        with open('../resources/objects.pyc', 'w') as pickleFile:
            pickle.dump(dataByLap,pickleFile)
            
            
        
    def testLoadPickledFile(self):
        testDict = None
        with open('../resources/objects.pyc', 'r') as pickleFile:
            testDict = pickle.load(pickleFile)
        
        
        self.assertIsNotNone(testDict)
            
            
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()