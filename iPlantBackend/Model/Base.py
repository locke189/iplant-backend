#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import sys
import datetime
import threading
from Model import DataLogger
from Shared import Logger
from Broker import Broker

class Base:
    #Base class
    #Implements all the base attributes for sensors/actuators as well as
    #specific broker, database update / receive methods.
    def __init__(self, database, broker, id, type, enabled, devicePath="/devices/id", categoryPath="/category/", dataTopic = "/data", logs=True):
        #Base properties
        self.db = database
        self.id = id
        self.type = type
        self.enabled = enabled
        self.path = devicePath + categoryPath + str(self.id)
        self.timestamp = ""
        self.streams = []

        self.timerInterval = 5 #seconds
        self.periodicUpdates = False

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

    #-------------------------------------------------------------
    #Broker Methods:
    # These methods should handle data from sensors / MQTT Broker
    # sets callback for new data from sensor/actuators
    def subscribeDataTopic(self):
        self.broker.subscribeTopicWithCallback(self.dataTopic, self.setData )


    def setData(self, topic, payload):
        self.console.log("set data method")
        self.data = payload
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #-------------------------------------------------------------
    #Streaming methods -
    # For data changes that come from the DB we set streams, that "subscribe"
    # to a specific field and respond with a callback whenever data is changed
    # BEWARE >> Streams must be closed or the app will never die...

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


    #-------------------------------------------------------------
    # Database methods
    #

    # Loading data from the database
    # It will bring all data into a dictionary, from the sensor/Actuator
    def loadDataFromDB(self):
        self.console.log("Getting data from database")
        return self.db.getData(self.path)


    #Updates data into the Database
    # There are 2 ways to update data into de DB
    #   1. Scheduled
    #   2. Manual

    #Sets the dictionary that is going to be sent to the database.
    def getDataDictionary(self):
        data = {
            "id": self.id,
            "type": self.type,
            "enabled": self.enabled,
            "data":  self.data,
            "timestamp": self.timestamp,
            }
        return data

    #Saves the dictionary (from getDataDictionary method) into DB
    #can be used for a manual update.
    def saveDataToDB(self, data = None):
        self.console.log("Saving data to database")

        if data == None:
            data = self.getDataDictionary()

        self.db.updateData(self.path,data)
        if self.periodicUpdates:
            threading.Timer(self.timerInterval, self.saveDataToDB).start()

    def setUptateTime(self, seconds):
        self.timerInterval = seconds
        self.console.log("Setting Periodic updates to %s seconds", self.timerInterval)

    def setPeriodicDBUpdates(self):
        self.console.log("Starting periodic updates to DB")
        self.periodicUpdates = True
        threading.Timer(self.timerInterval, self.saveDataToDB).start()

    def stopPeriodicDBUpdates(self):
        self.console.log("Stopping periodic updates to DB")
        self.periodicUpdates = False

    #-------------------------------------------------------------
    #Destroyer Method
    def __del__(self):
        self.closeStreams()
        pass


if __name__ == '__main__':
    # Main Loop
    pass
