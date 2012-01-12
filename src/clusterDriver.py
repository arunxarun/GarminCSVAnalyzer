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
        print "please supply an input file to parse."
        sys.exit(1)
    
    allFilters = []    
    if(len(sys.argv) == 3):
        filterBy=sys.argv[2];
        allFilters = filterBy.split(',')
    else:
        allFilters = []
        
    inp = open(sys.argv[1])
    
    keepProcessing = True
    activityToId = {}
    activityHasLaps = {}
    lapHasTracks = {}
    trackHasTrackPoints = {}
    
    # load data 
    while(keepProcessing ):
        cur = inp.readline()
        
        if(cur == ''):
            break
        cur = cur.rstrip('\n')
        
        if(cur == 'Activity Table'):
            activityToId = msp.parseActivities(inp,allFilters)
        elif (cur == 'ActivityLap Table'):
            activityHasLaps = msp.parseActivityLaps(inp,activityToId.keys())
        elif (cur == 'Track Table'):
            lapHasTracks = msp.parseTracks(inp,activityHasLaps)
        elif (cur == 'TrackPoint Table'):
            lapHasTrackPoints = msp.parseTrackPoints(inp,lapHasTracks)
        
    # now process points.
    # (1) summarize data by lap.
    dataByLap = msp.generateLapData(activityToId,lapHasTrackPoints)
     
    km = kmeans.KmeansClusterer(4)
    
    print "clustering %d laps"%len(dataByLap)
    clustersByCentroid = km.cluster(dataByLap)
    
    for k, v in clustersByCentroid.items():
        print "------------------"
        print "cluster data avg values"
        k.prettyPrint() 
        print "%d cluster members"%len(v)