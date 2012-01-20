'''
Created on Jan 11, 2012

@author: jacoba100
'''
import sys
from  milesplitparser import MileSplitParser
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
    
    # iterate fast: provide a parser class that will work with the dimensions we want. 
    # requirements: 
    #  manage allData
    #  expose specific subsets of each allData row to a clustering algorithm. 
    #  provide a way to express distance between each row given a specified subset. 
    #  
    
    #lap,totalDist,avgHR,netGained,netLost,timeSeconds,goodRecords,badRecords
    # each data should present these in a list. 
    # make that a contract.
    dataDescriptor = DataDescriptor([1,2,5])
    
    dataFilter = DataFilter(allData,dataDescriptor)
    
    clustersByCentroid = km.cluster(dataFilter)
    
    for k, v in clustersByCentroid.items():
        print "------------------"
        print "cluster data avg values"
        k.prettyPrint() 
        print "%d cluster members"%len(v)
        
        if(len(v) == 1):
            v[0].prettyPrint
        