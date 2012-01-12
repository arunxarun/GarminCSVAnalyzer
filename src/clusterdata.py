import sys
import logging
import datetime
import math
import random

METERS_IN_FEET = 3.28083989501312
MINUTE_IN_SECONDS = 60
TOTAL_DIST = 0
AVG_HR = 1
NET_GAINED = 2
NET_LOST = 3
TIME = 4
GOODRECS = 5
BADRECS = 6

ERROR_DIST = 1

class ClusterData:
    @staticmethod
    def inErrorRange(point1,point2,minRange,maxRange):
        if(point1.distanceTo(point2,minRange,maxRange) >= ERROR_DIST):
            return False
        else:
            return True
    @staticmethod

    def createMeanCentroid(clusterName,summaryDatas):
        
        summaryTotalDist = 0.0
        summaryAvgHr = 0.0
        summaryNetGained = 0.0
        summaryNetLost = 0.0
        summaryTime = 0.0
        summaryGoodRecs = 0.0
        summaryBadRecs = 0.0
        
        for data in summaryDatas:
            summaryTotalDist += data.totalDist
            summaryAvgHr += data.avgHR
            summaryNetGained += data.netGained
            summaryNetLost += data.netLost
            summaryTime += data.timeSeconds
            summaryGoodRecs += data.goodRecords
            summaryBadRecs += data.badRecords
            
        
        divisor = len(summaryDatas)
        avgDist = summaryTotalDist/divisor
        avgHr = summaryAvgHr/divisor
        avgNetGained = summaryNetGained/divisor
        avgNetLost = summaryNetLost/divisor
        avgTime = summaryTime/divisor
        avgGoodRecs = summaryGoodRecs/divisor
        avgBadRecs = summaryBadRecs/divisor
        
        return LapData(clusterName,avgDist,avgHr,avgNetGained,avgNetLost,avgTime,avgGoodRecs,avgBadRecs)
    
    @staticmethod

    def initializeCentroids(centroidCt,summaryDatas):
        
        loRanges,hiRanges = ClusterData.initializeRanges(summaryDatas)
        
        centroids = []
        
        for i in range(centroidCt):
            centroids.append(ClusterData.generateRandomSummaryData("centroid %d"%i,loRanges,hiRanges))
        
        return centroids,loRanges,hiRanges

    @staticmethod

    def generateRandomSummaryData(pointName,loRanges,hiRanges):
        return LapData( 
                pointName,                                              
                random.randrange(int(loRanges[TOTAL_DIST]),int(hiRanges[TOTAL_DIST])),
                random.randrange(int(loRanges[AVG_HR]),int(hiRanges[AVG_HR])),
                random.randrange(int(loRanges[NET_GAINED]),int(hiRanges[NET_GAINED])),
                random.randrange(int(loRanges[NET_LOST]),int(hiRanges[NET_LOST])),
                random.randrange(int(loRanges[TIME]),int(hiRanges[TIME])),0,0)

    @staticmethod
    
    def initializeRanges(summaryDatas):
        loRanges = {}
        hiRanges = {}
        
            
        for summaryData in summaryDatas:
            '''
            self.totalDist = totalDist
            self.avgHR = avgHR
            self.netGained = netGained
            self.netLost = netLost
            self.timeSeconds = timeSeconds
            '''
            if(TOTAL_DIST not in loRanges):
                loRanges[TOTAL_DIST] = summaryData.totalDist
            
            if(loRanges[TOTAL_DIST] > summaryData.totalDist):
                loRanges[TOTAL_DIST] = summaryData.totalDist
            
            if(TOTAL_DIST not in hiRanges):
                hiRanges[TOTAL_DIST] = summaryData.totalDist
            if(hiRanges[TOTAL_DIST] < summaryData.totalDist):
                hiRanges[TOTAL_DIST] = summaryData.totalDist
            
            if(AVG_HR not in loRanges):
                loRanges[AVG_HR] = summaryData.avgHR
            
            if(loRanges[AVG_HR] > summaryData.avgHR):
                loRanges[AVG_HR] = summaryData.avgHR
            
            if(AVG_HR not in hiRanges):
                hiRanges[AVG_HR] = summaryData.avgHR
            if(hiRanges[AVG_HR] < summaryData.avgHR):
                hiRanges[AVG_HR] = summaryData.avgHR
            
            if(NET_GAINED not in loRanges):
                loRanges[NET_GAINED] = summaryData.netGained
            if(loRanges[NET_GAINED] > summaryData.netGained):
                loRanges[NET_GAINED] = summaryData.netGained
            
            if(NET_GAINED not in hiRanges):
                hiRanges[NET_GAINED] = summaryData.netGained
            if(hiRanges[NET_GAINED] < summaryData.netGained):
                hiRanges[NET_GAINED] = summaryData.netGained
                
            if(NET_LOST not in loRanges):
                loRanges[NET_LOST] = summaryData.netLost
            if(loRanges[NET_LOST] > summaryData.netLost):
                loRanges[NET_LOST] = summaryData.netLost
            
            if(NET_LOST not in hiRanges):
                hiRanges[NET_LOST] = summaryData.netLost
            if(hiRanges[NET_LOST] < summaryData.netLost):
                hiRanges[NET_LOST] = summaryData.netLost
            
            if(TIME not in loRanges):
                loRanges[TIME] = summaryData.timeSeconds
            if(loRanges[TIME] > summaryData.timeSeconds):
                loRanges[TIME] = summaryData.timeSeconds
            
            if(TIME not in hiRanges):
                hiRanges[TIME] = summaryData.timeSeconds
            if(hiRanges[TIME] < summaryData.timeSeconds):
                hiRanges[TIME] = summaryData.timeSeconds
                
        return loRanges,hiRanges


class LapData:
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
        
    
        
    
        
        
    def getNormalizedMeasure(self,scale,value,minRange,maxRange):
        totalRange = maxRange - minRange
        offSet = value - minRange
        
        value =  float(offSet)/totalRange
        return value*scale
    
    # I need the mins and maxes here to normalize the different vectors against one another.
    # otherwise I have _no_idea_ what distance really means. 
        
    def distanceTo(self,otherSummaryData,mins,maxes):
        
        myDist = self.getNormalizedMeasure(100,self.totalDist,mins[TOTAL_DIST],maxes[TOTAL_DIST])
        otherDist = self.getNormalizedMeasure(100,otherSummaryData.totalDist,mins[TOTAL_DIST],maxes[TOTAL_DIST])
        
        myHR = self.getNormalizedMeasure(100, self.avgHR, mins[AVG_HR], maxes[AVG_HR])
        otherHR = self.getNormalizedMeasure(100, otherSummaryData.avgHR, mins[AVG_HR], maxes[AVG_HR])
        
        myGained = self.getNormalizedMeasure(100, self.netGained, mins[NET_GAINED], maxes[NET_GAINED])
        otherGained = self.getNormalizedMeasure(100, otherSummaryData.netGained, mins[NET_GAINED], maxes[NET_GAINED])
        
        myLost = self.getNormalizedMeasure(100, self.netLost, mins[NET_LOST], maxes[NET_LOST])
        otherLost = self.getNormalizedMeasure(100, otherSummaryData.netLost, mins[NET_LOST], maxes[NET_LOST])
        
        myTime = self.getNormalizedMeasure(100, self.timeSeconds, mins[TIME], maxes[TIME])
        otherTime = self.getNormalizedMeasure(100, otherSummaryData.timeSeconds, mins[TIME], maxes[TIME])
        
        
        rawSum = math.pow(myDist-otherDist,2) + math.pow(myHR - otherHR,2) + math.pow(myGained - otherGained,2) + math.pow(myLost - otherLost, 2) + math.pow(myTime - otherTime,2)
        dist = math.sqrt(rawSum)
            
        
        return dist
        
        
        
        
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
        