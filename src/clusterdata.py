import sys
import logging
import datetime
import math
from kmeansprimitives import DataPoint


METERS_IN_FEET = 3.28083989501312
MINUTE_IN_SECONDS = 60
UNSET = -1


class ClusterData:
    @staticmethod
    def toDateTime(time):
        zRemoved = time[0:len(time)-1]
        dt = datetime.datetime.strptime(zRemoved,'%Y-%m-%dT%H:%M:%S')
        return dt

    @staticmethod
    def metersToFeet(meters):
        feet = float(meters)*METERS_IN_FEET
        return feet




class GarminLap(DataPoint):
    DIMENSIONS = 5
    
    @staticmethod

    def asLap(id,time,dist,hr, netGained,netLost):
        #RecID,ActivityRecID,NextSportRecID,StartTime,TotalTimeSeconds,DistanceMeters,MaximumSpeed,Calories,AverageHeartRateBpm,MaximumHeartRateBpm,Intensity,AverageCadence,TriggerMethod,Notes,
        #1,1,,2011-01-05T15:00:46Z,576.5800000,1609.3439941,3.3762498,179,113,132,Active,,Distance,"",
        tokens = []
        tokens.append(0)
        tokens.append(0)
        tokens.append(0)
        tokens.append(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        tokens.append(time)
        tokens.append(dist)
        tokens.append(0)
        tokens.append(0)
        tokens.append(hr)
        
        lap = GarminLap(tokens)
        lap.lap = id
        lap.netGained = ClusterData.metersToFeet(netGained)
        lap.netLost = ClusterData.metersToFeet(netLost)
        
        return lap
    
        
    def __init__(self,tokens):
        #RecID,ActivityRecID,NextSportRecID,StartTime,TotalTimeSeconds,DistanceMeters,MaximumSpeed,Calories,AverageHeartRateBpm,MaximumHeartRateBpm,Intensity,AverageCadence,TriggerMethod,Notes,
        self.id = int(tokens[0])
        self.activityId = int(tokens[1])
        self.lap = tokens[3]
        self.startTime = ClusterData.toDateTime(tokens[3])
        self.totalTime = float(tokens[4])
        self.totalDistance = ClusterData.metersToFeet(float(tokens[5]))
        self.avgHR = float(tokens[8])
        self.netGained = UNSET
        self.netLost = UNSET
                
    
    # I need the mins and maxes here to normalize the different vectors against one another.
    # otherwise I have _no_idea_ what distance really means. 
        
    def distanceTo(self,otherSummaryData,dataFilter):
        
        myDist = dataFilter.getNormalizedMeasure(100,self.totalDistance,dataFilter.TOTAL_DIST)
        otherDist = dataFilter.getNormalizedMeasure(100,otherSummaryData.totalDistance,dataFilter.TOTAL_DIST)
        
        myHR = dataFilter.getNormalizedMeasure(100, self.avgHR,dataFilter.AVG_HR)
        otherHR = dataFilter.getNormalizedMeasure(100, otherSummaryData.avgHR, dataFilter.AVG_HR)
        
        myGained = dataFilter.getNormalizedMeasure(100, self.netGained, dataFilter.NET_GAINED)
        otherGained = dataFilter.getNormalizedMeasure(100, otherSummaryData.netGained, dataFilter.NET_GAINED)
        
        myLost = dataFilter.getNormalizedMeasure(100, self.netLost, dataFilter.NET_LOST)
        otherLost = dataFilter.getNormalizedMeasure(100, otherSummaryData.netLost, dataFilter.NET_LOST)
        
        myTime = dataFilter.getNormalizedMeasure(100, self.totalTime, dataFilter.TIME)
        otherTime = dataFilter.getNormalizedMeasure(100, otherSummaryData.totalTime, dataFilter.TIME)
        
        
        rawSum = math.pow(myDist-otherDist,2) + math.pow(myHR - otherHR,2) + math.pow(myGained - otherGained,2) + math.pow(myLost - otherLost, 2) + math.pow(myTime - otherTime,2)
        dist = math.sqrt(rawSum)
            
        
        return dist
        
    def prettyPrint(self,separator = True):
        if(separator == True):
            print "------"
        print "lap = %s,"%self.lap
        print "totalDistance = %f,"%self.totalDistance
        print "avgHR = %f,"%self.avgHR
        print "netGained = %f"%self.netGained
        print "netLost = %f"%self.netLost
        print "timeSecs = %f"%self.totalTime
            
    

class TrackPoint:
    def __init__(self,selfId, tokens):
        self.logger = logging.getLogger('TrackPoint')
        self.logger.addHandler(logging.StreamHandler())
        # tokens is an array in the following format: 
        # TrackRecID,Time,Latitude,Longitude,AltitudeMeters,DistanceMeters,HeartRateBpm,Cadence,SensorState
        if(len(tokens) < 6):
            raise Exception('invalid TrackPoint, only %d tokens'%len(tokens))
        
        if(tokens[4] == '' or tokens[5] == ''):
            raise Exception('invalid TrackPoint, altitude or distance are blank')
        self.id = selfId
        self.trackId = int(tokens[0])
        self.time = ClusterData.toDateTime(tokens[1])
        self.lat = float(tokens[2])
        self.long = float(tokens[3])
        self.altitude = ClusterData.metersToFeet(tokens[4])
        self.distance = ClusterData.metersToFeet(tokens[5])
        self.heartRate = float(tokens[6])
        
    
        
    def prettyPrint(self, useDelimiter = True):
        if(useDelimiter == True):
            sys.stderr.write("--------\n")
        sys.stderr.write("id = %s,"%self.id)
        sys.stderr.write("trackId = %s,"%self.trackId)
        sys.stderr.write("time = %s,"%self.time)
        sys.stderr.write("lat = %f,"%self.lat)
        sys.stderr.write("long = %f,"%self.long)
        sys.stderr.write("altitude = %f,"%self.altitude)
        sys.stderr.write("distance = %f,"%self.distance)
        sys.stderr.write("heart rate = %d\n"%self.heartRate)
        