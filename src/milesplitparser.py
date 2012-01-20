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
            
        self.activitiesById = {}
        self.laps = []
        self.lapsToTracks = {}
        self.trackPoints = []
            
            
    def getData(self,fileName,filters = None,excludeManualLaps = False):
        
        inp = open(sys.argv[1])
    
        keepProcessing = True
                
        # load data 
        while(keepProcessing ):
            cur = inp.readline()
           
            cur = cur.rstrip('\n')
            
            if(cur == 'Activity Table'):
                self.activityToId = self.getActivityIDs(inp,filters)
            elif (cur == 'ActivityLap Table'):
                self.lapData = self.getLaps(inp,excludeManualLaps)
            elif (cur == 'Track Table'):
                self.lapsToTracks = self.getLapsToTracks(inp, self.lapData)
            elif (cur == 'TrackPoint Table'):
                self.trackData = self.getTrackPoints(inp)
                break
                
            
        
    '''
    get the list of activities to extract statistics for
    '''        
    def getActivityIDs(self,input,allFilters = []):
        
            
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
    def getLaps(self,input,excludeManualLaps = False):
        allLaps = []
        
        # skip trackId line
        cur = input.readline()
    
        keepProcessing = True

        while(keepProcessing):
            cur= input.readline()
            if(cur == '\n'):
                keepProcessing = False
                continue
            
            tokens = cur.split(',')
            
                
            # RecID,ActivityRecID,NextSportRecID,StartTime,TotalTimeSeconds,DistanceMeters,MaximumSpeed,Calories,AverageHeartRateBpm,MaximumHeartRateBpm,Intensity,AverageCadence,TriggerMethod,Notes,
            
            if excludeManualLaps == True and tokens[12] == 'Manual':
                continue
            
            lap = clusterdata.Lap(tokens)
            allLaps.append(lap)
        
        self.logger.debug("%d laps total"%len(allLaps))
        
        return allLaps
    
    '''
    map tracks to laps
    '''
    def getLapsToTracks(self,input,lapData):
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
            
            for lap in lapData:
                
                if tokens[1]  == lap.id:
                    if (tokens[1] not in lapHasTracks):
                        lapHasTracks[tokens[1]] = []
                    lapHasTracks[tokens[1]].append(tokens[0])
                
        self.logger.debug(" tracks for %d laps found\n"%len(lapHasTracks.keys()))    
        return lapHasTracks
    
    
    def getTrackPoints(self,input):
        trackPoints = []
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
                trackPoint = clusterdata.TrackPoint(curId,tokens)
                trackPoints.append(trackPoint)
            except Exception as ex:
                #self.logger.warning(ex)
                continue;
        
        return trackPoints
     
    
    