'''
Created on Dec 18, 2011

@author: jacoba100
'''
import sys
import logging
import datetime
import clusterdata

    
'''
map activity IDs to name strings
'''
class MileSplitParser:
    
    def __init__(self,isVerbose = False):
        self.logger = logging.getLogger('MileSplitParser')
        self.logger.addHandler(logging.StreamHandler())
        if(isVerbose == True):
            self.logger.setLevel(logging.DEBUG)
            
    '''
    get the list of activities to extract statistics for
    '''        
    def parseActivities(self,input,allFilters = []):
        
            
        activityToId = {}
        # skip trackId line
        cur = input.readline()
        keepProcessing = True
        while(keepProcessing):
            cur= input.readline()
            if(cur == '\n'):
                keepProcessing = False
                continue
            
            tokens = cur.split(',')
            
            addToMap = True
            
            for filter in allFilters:
                if(tokens[4] == filter):
                    addToMap = False
            
            if(addToMap == True):        
                activityToId[tokens[0]] = tokens[3]
    
        
        return activityToId
    
    '''
    map Laps to activities
    '''
    def parseActivityLaps(self,input,activities):
        activityHasLaps = {}
        
        # skip trackId line
        cur = input.readline()
    
        keepProcessing = True
        while(keepProcessing):
            cur= input.readline()
            if(cur == '\n'):
                keepProcessing = False
                continue
            
            tokens = cur.split(',')
            if tokens[1] in activities:
                if tokens[1] not in activityHasLaps:
                    activityHasLaps[tokens[1]] = []
                activityHasLaps[tokens[1]].append(tokens[0])
        
        self.logger.debug("%d activities detected\n"%len(activityHasLaps))
        return activityHasLaps
    
    '''
    map tracks to laps
    '''
    def parseTracks(self,input,activityHasLaps):
        lapHasTracks = {}
        # skip trackId line
        cur = input.readline()
        keepProcessing = True
        while(keepProcessing):
            cur= input.readline()
            if(cur == '\n'):
                keepProcessing = False
                continue
            
            tokens = cur.split(',')
            
            for lapsPerActivity in activityHasLaps.values():
                
                if tokens[1] in lapsPerActivity:
                    if (tokens[1] not in lapHasTracks):
                        lapHasTracks[tokens[1]] = []
                    lapHasTracks[tokens[1]].append(tokens[0])
                
        self.logger.debug(" %d laps detected\n"%len(lapHasTracks))    
        return lapHasTracks
    
    '''
    map trackpoints to tracks, store trackpoint data in trackpoints.
    trackpointID => trackpoint Object.
    '''
    def parseTrackPoints(self,input,lapHasTracks):
        lapHasTrackPoints = {}
        # skip trackId line
        cur = input.readline()
        keepProcessing = True
        curId = 1
        while(keepProcessing):
            cur= input.readline()
            if(cur == '\n'):
                keepProcessing = False
                continue
            
            tokens = cur.split(',')
            
            try:
                for lap,tracks in lapHasTracks.items():
                    if tokens[0] in tracks:
                        trackPoint = clusterdata.TrackPoint(curId,tokens)
                       
                        if lap not in lapHasTrackPoints:
                            lapHasTrackPoints[lap] = []
                        lapHasTrackPoints[lap].append(trackPoint)
                
                        curId+=1
                        break
                        
            except Exception as ex:
                self.logger.warning(ex)
                continue;
        
        self.logger.debug(" %d laps processed\n"%len(lapHasTrackPoints))
        self.logger.debug(" %d total trackpoints\n"%(curId - 1))
        return lapHasTrackPoints
     
    '''
    generate avg hr, pace, altitude gained/lost, total distance, per lap. 
    ''' 
    def generateLapData(self,activityHasLaps,lapHasTrackPoints):
        
        sortedLaps = sorted(lapHasTrackPoints.keys())
        allLapDatas = []
        for lap in sortedLaps:
            lastDist = 0
            badRecords = 0
            points  = lapHasTrackPoints[lap]
            startDist = 0
            endDist = 0
            totalDist = 0.0
            recordCt = 0
            totalHr = 0
            lastElevation = None
            netLost = 0.0
            netGained = 0.0
            startTime = None
            lastTime = None
            for point in points:
                
                if point.distance >= lastDist:
                    recordCt +=1
                    
                    if lastDist == 0:
                        startDist = point.distance
                    
                    lastDist = point.distance
                    
                    if lastElevation == None:
                        lastElevation = point.altitude
                   
                    if lastElevation >= point.altitude:
                        netLost += lastElevation - point.altitude
                    else:
                        netGained += point.altitude - lastElevation
                        
                    lastElevation = point.altitude
                    
                    
                    totalHr += point.heartRate
                    
                    if startTime == None:
                        startTime = point.time
                    
                    lastTime = point.time                  
                    # this is where we do aggregation, because distance is increasing. skip anomalous records
                    
                else:
                    #self.logger.warn('distance should be increasing! lap = %s, last dist = %f, cur dist = %f'%(lap,lastDist,point.distance))        
                    badRecords += 1

            # calc distance
            endDist = point.distance
            totalDist = endDist - startDist
            # calc avg HR
            avgHR = float(totalHr)/recordCt
            
            # calc total time
            
            time = lastTime - startTime
            
            lapData = clusterdata.LapData(lap,totalDist,avgHR,netGained,netLost,time.seconds,recordCt,badRecords)
            if badRecords > 0 :
                self.logger.warn("bad records = %d out of %d records"%(badRecords,len(points)))
            
            allLapDatas.append(lapData)
        
        return allLapDatas
        
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
     
    for lap in dataByLap:
        print lap.prettyPrint() 
    pass