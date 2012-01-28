'''
Created on Jan 27, 2012

@author: jacoba100
'''
import unittest
from garmindatafilter import GarminDataFilter
from milesplitparser import MileSplitParser
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
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()