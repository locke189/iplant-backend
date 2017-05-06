#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import sys
import datetime
from Model import DataLogger
from Shared import Logger
from Broker import Broker
from Model import Base
from Model import AvgFilter

class Sensor(Base.Base):

    def __init__(self, database, storage, broker, id, type, enabled, devicePath, logs=True, filterSamples=5, datasetLength = 10, skipSamples=10, dbUpdateTime = 1800):

        #Initializing Base class
        super().__init__(database, broker, id, type, enabled, devicePath, categoryPath="/sensors/", logs = logs)
        self.subscribeDataTopic()

        #datasets
        self.dataset = []
        self.datasetAvg = []
        self.datasetLabel = []
        self.datasetLength = datasetLength

        #Skip samples
        self.skipSamples = skipSamples
        self.sampleCount = 0

        #Initializing filter
        self.avgFilter = AvgFilter.AvgFilter(path=self.path, logs=logs)
        self.avgFilter.enable(filterSamples)

        #Initializing DataLogger
        self.dataLogger = DataLogger.DataLogger('sensorinit' , storage=storage , storageRoute=self.path+"/", logs=logs)


        #set pediodic updates to DB
        self.setUptateTime(dbUpdateTime)
        self.setPeriodicDBUpdates()

    #-------------------------------------------------------------------------
    # Filtering methods
    # The following methods should deal with data comming in from the sensors.
    # The main idea is that there is going to be an array of data, one for
    # average data, and one array for labels to indicate when the data ways
    # taken.


    # Overide of setData method to include update of filters and labels
    def setData(self, topic, payload):
        super().setData(topic,payload)
        #Running AVG filter implementation
        if self.avgFilter.isEnabled():
            self.avgFilter.run(self.data)

        #maxSampleCount to updata dataset
        if self.sampleCount >= self.skipSamples:
            self.datasetDataEntry()
            self.sampleCount = 0
        else:
            self.sampleCount += 1


    #Sets the string that is going to be sent to the database
    def getDataDictionary(self):
        data = {
            "id": self.id,
            "type": self.type,
            "enabled": self.enabled,
            "data":  self.data,
            "timestamp": self.timestamp,
            "filter": self.avgFilter.isEnabled(),
            "avgData": self.avgFilter.getValue(),
            "filterSamples": self.avgFilter.filterSamples,
            "dataset": self.dataset,
            "datasetAvg": self.datasetAvg,
            "datasetLabel": self.datasetLabel,
            "historic": self.dataLogger.logInfo["logs"]
            }
        return data

    #-----------------------------------------------------------------------
    # Dataset Methods:
    # The purpose of datasets is to give the frontend a portion of historic
    # sensor data in order to plot some charts. datasets are actually buffers
    # so we discard the oldest entry as soon as new data gets in and the
    # buffer is full.
    # Historic data is saved via dataLogger class. The idea is to save the
    # same data that goes into the dataset to the historic.

    def datasetDataEntry(self):

        if(len(self.dataset) == self.datasetLength):
            self.console.log("Saving sensor data to dataset (discarding old data)")
            self.datasetAvg.pop(0)
            self.dataset.pop(0)
            self.datasetLabel.pop(0)
        else:
            self.console.log("Saving sensor data to dataset")

        self.datasetAvg.append( self.avgFilter.getValue() )
        self.dataset.append(self.data)
        self.datasetLabel.append(datetime.datetime.now().strftime("%H:%M"))

        self.console.log("Logging dataset")
        self.dataLogger.newLogEntry(self.data, self.avgFilter.getValue() , datetime.datetime.now().strftime("%H:%M"))

    def __del__(self):
        self.stopPeriodicDBUpdates()


if __name__ == '__main__':




    # Main Loop
    pass
