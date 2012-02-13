'''
Created on Dec 18, 2011

@author: jacoba100
'''
import sys
import logging
import datetime
import clusterdata
from kmeansprimitives import Parser
    
'''
This class parses garmin data files. There are two methods:
call loadData() first, then call getData() to retrieve specific parsed data.
'''

class MileSplitParser(Parser):
    
    LAPS = 0
    TRACKSTOLAPS = 1
    TRACKPOINTS = 2
    SEPARATOR = '\t'
    
    def __init__(self,isVerbose = False):
        self.logger = logging.getLogger('MileSplitParser')
        self.logger.addHandler(logging.StreamHandler())
        
        if(isVerbose == True):
            self.logger.setLevel(logging.DEBUG)
            
        self.activitiesById = {}
        self.laps = []
        self.lapsToTracks = {}
        self.trackPoints = []
            
    
    def getData(self,dataId): 
        
        if(dataId == self.LAPS):
            return self.laps
        elif(dataId == self.TRACKSTOLAPS):
            return self.lapsToTracks
        elif(dataId == self.TRACKPOINTS):
            return self.trackPoints
               
    def loadData(self,fileName,filters = [],excludeManualLaps = False):
        
        inp = open(fileName)
    
        keepProcessing = True
                
        # load data 
        while(keepProcessing ):
            cur = inp.readline()
           
            cur = cur.rstrip('\n')
            
            if(cur == 'Activity Table'):
                self.activityToId = self.getActivityIDs(inp,filters)
            elif (cur == 'ActivityLap Table'):
                self.laps = self.getLaps(inp,excludeManualLaps)
            elif (cur == 'Track Table'):
                self.lapsToTracks = self.getTracksToLaps(inp)
            elif (cur == 'TrackPoint Table'):
                self.trackPoints = self.getTrackPoints(inp)
                break
                
            
        
    '''
    get the list of activities to extract statistics for
    '''        
    def getActivityIDs(self,input,allFilters = []):
        
            
        activitiesToIds = {}
        # skip trackId line
        cur = input.readline()
        keepProcessing = True
        while(keepProcessing):
            cur= input.readline()
            if(cur == '\n'):
                keepProcessing = False
                continue
            
            tokens = cur.split(self.SEPARATOR)
            
            addToMap = True
            
            for filter in allFilters:
                if(tokens[4] == filter):
                    addToMap = False
            
            if(addToMap == True):        
                activitiesToIds[tokens[0]] = tokens[3]
    
        
        return activitiesToIds
    
    '''
    map Laps to activities
    '''
    def getLaps(self,input,excludeManualLaps = False):
        allLaps = {}
        
        # skip trackId line
        cur = input.readline()
    
        keepProcessing = True

        while(keepProcessing):
            cur= input.readline()
            if(cur == '\n'):
                keepProcessing = False
                continue
            
            tokens = cur.split(self.SEPARATOR)
            
                
            # RecID,ActivityRecID,NextSportRecID,StartTime,TotalTimeSeconds,DistanceMeters,MaximumSpeed,Calories,AverageHeartRateBpm,MaximumHeartRateBpm,Intensity,AverageCadence,TriggerMethod,Notes,
            
            if excludeManualLaps == True and tokens[12] == 'Manual':
                continue
            
            lap = clusterdata.GarminLap(tokens)
            allLaps[lap.id] = lap
        
        self.logger.debug("%d laps total"%len(allLaps))
        
        return allLaps
    
    '''
    map tracks to laps
    '''
    def getTracksToLaps(self,input):
        trackHasLap = {}
        # skip trackId line
        cur = input.readline()
        keepProcessing = True
        while(keepProcessing):
            cur= input.readline()
            if(cur == '\n'):
                keepProcessing = False
                continue
            
            tokens = cur.split(self.SEPARATOR)
            
            testLapId = int(tokens[1])
            testTrackId = int(tokens[0])
            trackHasLap[testTrackId] = testLapId
            
        return trackHasLap
    
    
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
            
            tokens = cur.split(self.SEPARATOR)
            
            try:
                trackPoint = clusterdata.TrackPoint(curId,tokens)
                trackPoints.append(trackPoint)
            except Exception as ex:
                #self.logger.warning(ex)
                continue;
        
        return trackPoints
     
