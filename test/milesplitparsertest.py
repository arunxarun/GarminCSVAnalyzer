'''
Created on Dec 21, 2011

@author: jacoba100
'''
import unittest
from milesplitparser import MileSplitParser
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


    
            
            
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()