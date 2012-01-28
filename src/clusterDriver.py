'''
Created on Jan 11, 2012

@author: jacoba100
'''
import sys
from  milesplitparser import MileSplitParser
from garmindatafilter import GarminDataFilter
import kmeans


if __name__ == '__main__':
    
    msp = MileSplitParser()
    
    if(len(sys.argv) < 2):
        print "clusterDriver.py [input file] {comma separated filter list}"
        sys.exit(1)
    
    allFilters = []    
    if(len(sys.argv) == 3):
        filterBy=sys.argv[2];
        allFilters = filterBy.split(',')
    else:
        allFilters = []
    
    allData = msp.getData(sys.argv[1])
    
    
    km = kmeans.KmeansClusterer(4)
    
    parser = MileSplitParser()
    parser.loadData('../resources/test.csv')
    gdf = GarminDataFilter(parser) 
    
    clustersByCentroid = km.cluster(gdf)
    
    for k, v in clustersByCentroid.items():
        print "------------------"
        print "cluster data avg values"
        k.prettyPrint() 
        print "%d cluster members"%len(v)
        
        if(len(v) == 1):
            v[0].prettyPrint
        