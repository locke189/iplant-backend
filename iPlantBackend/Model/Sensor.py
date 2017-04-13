#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import sys
import datetime
from DataLogger import DataLogger
from Shared import Logger
from Broker import Broker

class Sensor:
    def __init__(self, device, sensorId, type, version, enabled,logs=True):

        self.db = device.db
        self.device = device
        self.id = sensorId
        self.type = type
        self.version = version
        self.enabled = enabled
        self.path = device.path + "/sensors/" + str(self.id)
        self.timestamp = ""
        self.avgData = ""
        self.filter = False
        self.filterSamples = ""
        self.storageRoute = "/" + str(self.device.id) + "/" + self.id + "/"
        self.data = ""
        self.dataset = []
        self.datasetAvg = []
        self.datasetLabel = []
        self.datasetMax = 48
        #Initializaing logger
        self.console = Logger.Logger(logName="Sensor("+self.path+")", enabled=logs, printConsole=True)
        self.console.log("Initialization...")
        #Initializing DataLogger
        self.dataLogger = DataLogger('sensorinit',self.device.storage,"/"+self.path+"/",self.device)
        #Initializing broker
        self.broker = Broker.Broker(topic=self.path, logs = True, logName=self.path)
        self.broker.setCallback(self.brokerCallback)
        self.broker.start()

    def brokerCallback(self, topic, payload):
        self.console.log("Broker callback")
        self.updateData(int(payload))

    def getSensorDataFromDB(self):
        self.console.log("Getting sensor data from database")
        self.db.getData()


    #Running AVG filter implementation
    def filterEnable(self, samples):
        self.console.log("Enabling AVG filter - %s samples", (samples))
        self.filter = True
        self.filterSamples = samples
        self.filterData = [0] * self.filterSamples
        self.avgData = 0

    def filterRun(self, data):
        self.console.log("Filtering")
        self.filterData.pop()
        self.filterData.insert(0,int(data))
        self.avgData = sum(self.filterData)/self.filterSamples


    def filterDisable(self):
        self.console.log("AVG Filter disabled")
        self.filter = False
        self.avgData = ""
        self.filterSamples = ""


    #Update sensor data from device readings
    def updateData(self, data):
        self.console.log("Updating raw sensor data = %s", data)
        self.data = data
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #Running AVG filter implementation
        if self.filter:
            self.filterRun(data)

    #Sets the string that is going to be sent to the database
    def getSensorData(self):
        data = {
            "id": self.id,
            "type": self.type,
            "version": self.version,
            "enabled": self.enabled,
            "data":  self.data,
            "timestamp": self.timestamp,
            "filter": self.filter,
            "avgData": self.avgData,
            "filterSamples": self.filterSamples,
            "dataset": self.dataset,
            "datasetAvg": self.datasetAvg,
            "datasetLabel": self.datasetLabel,
            "historic": self.dataLogger.logInfo["logs"]
            }
        return data

    #Updates data into the Database
    def saveSensorToDB(self):
        self.console.log("Saving sensor data to database")
        data = self.getSensorData()
        self.db.updateData(self.path,data)


    def datasetDataEntry(self):

        if(len(self.dataset) == self.datasetMax):
            self.console.log("Saving sensor data to dataset (discarding old data)")
            self.datasetAvg.pop(0)
            self.dataset.pop(0)
            self.datasetLabel.pop(0)
        else:
            self.console.log("Saving sensor data to dataset")

        self.datasetAvg.append(self.avgData)
        self.dataset.append(self.data)
        self.datasetLabel.append(datetime.datetime.now().strftime("%H:%M"))

        self.console.log("Logging dataset")
        self.dataLogger.newLogEntry(self.data, self.avgData, datetime.datetime.now().strftime("%H:%M"))

    def onDestroy(self):
        self.broker.stop()


if __name__ == '__main__':




    # Main Loop
    pass
