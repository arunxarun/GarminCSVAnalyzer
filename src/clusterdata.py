import sys
import logging
import datetime

METERS_IN_FEET = 3.28083989501312
MINUTE_IN_SECONDS = 60
TOTAL_DIST = 0
AVG_HR = 1
NET_GAINED = 2
NET_LOST = 3
TIME = 4
GOODRECS = 5
BADRECS = 6

class SummaryData:
    DIMENSIONS = 5
    
        
    def __init__(self,lap,totalDist,avgHR,netGained,netLost,timeSeconds,goodRecords,badRecords):
        self.lap = lap
        self.totalDist = totalDist
        self.avgHR = avgHR
        self.netGained = netGained
        self.netLost = netLost
        self.timeSeconds = timeSeconds
        self.goodRecords = goodRecords
        self.badRecords = badRecords
        
    def prettyPrint(self,separator = True):
        if(separator == True):
            print "------"
        print "lap = %s,"%self.lap
        print "totalDist = %f,"%self.totalDist
        print "avgHR = %f,"%self.avgHR
        print "netGained = %f"%self.netGained
        print "netLost = %f"%self.netLost
        print "timeSecs = %f"%self.timeSeconds
        print "goodRecords = %d"%self.goodRecords
        print "badRecords = %d"%self.badRecords
            
    

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
        self.trackId = tokens[0]
        self.time = self.toDateTime(tokens[1])
        self.lat = float(tokens[2])
        self.long = float(tokens[3])
        self.altitude = self.metersToFeet(tokens[4])
        self.distance = self.metersToFeet(tokens[5])
        self.heartRate = float(tokens[6])
        
    def toDateTime(self,time):
        zRemoved = time[0:len(time)-1]
        dt = datetime.datetime.strptime(zRemoved,'%Y-%m-%dT%H:%M:%S')
        return dt

    def metersToFeet(self,meters):
        feet = float(meters)*METERS_IN_FEET
        return feet
        
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
        