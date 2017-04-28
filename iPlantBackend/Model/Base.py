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

class Base:
    def __init__(self, database, broker, id, type, enabled, devicePath="/devices/id", categoryPath="/category/", dataTopic = "/data", logs=True, maxSampleCount=5):
        #Base properties
        self.db = database
        self.id = id
        self.type = type
        self.enabled = enabled
        self.path = devicePath + categoryPath + str(self.id)
        self.timestamp = ""
        self.streams = []

        #Data related
        self.data = "";

        #Initializaing logger
        self.console = Logger.Logger(logName="("+self.path+")", enabled=logs, printConsole=True)
        self.console.log("Initialization...")

        #Initializing broker
        self.dataTopic = self.path + dataTopic
        self.broker = broker
        #self.broker.setCallback(self.brokerCallback)
        #self.broker.start()

    #sets callback for new data from sensor/actuators
    def subscribeDataTopic(self):
        self.broker.subscribeTopicWithCallback(self.dataTopic, self.setData )


    def setData(self, topic, payload):
        self.console.log("set data method")
        self.data = payload




    #streaming methods
    def streamFromDB(self, property, callback):
        self.db.setStream(self.path +"/"+ property, callback)
        self.streams.append(self.path +"/"+ property)

    def closeStreams(self):
        while (self.streams != [] ):
            stream = self.streams.pop()
            self.db.closeStream(stream)

    def changeEnabledStateFromDB(self, message):
        if isinstance(message["data"], bool) :
            self.console.log("Enabled: %s",str(message["data"]))
            self.enable = message["data"]
        else:
            self.console.log("Cannot change enabled state: %s is not bool", str(message["data"]))

    def loadDataFromDB(self):
        self.console.log("Getting data from database")
        return self.db.getData(self.path)



    #Sets the string that is going to be sent to the database
    def getDataDictionary(self):
        data = {
            "id": self.id,
            "type": self.type,
            "enabled": self.enabled,
            "data":  self.data,
            "timestamp": self.timestamp,
            }
        return data


    #Updates data into the Database
    def saveDataToDB(self, data):
        self.console.log("Saving data to database")
        self.db.updateData(self.path,data)

    #Gets initial state from database
    def loadInitialData(self):
        self.console.log("Loading data from database")
        data = self.db.updateData(self.path,data)

    def __del__(self):
        self.closeStreams()
        pass


if __name__ == '__main__':
    # Main Loop
    pass
