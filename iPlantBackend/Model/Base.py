#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from Shared import Logger


class Base(object):
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
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.streams = []


        self.timerInterval = 2 #minutes / TODO overide this value
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


        # Scheduler
        self.jobId = self.path.replace("/","")
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.job = self.scheduler.add_job(self.saveDataToDB, 'interval', minutes=self.timerInterval, id=self.jobId, replace_existing=True)
        self.job.pause()

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
        self.db.checkAliveStream()


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
        if data is None:
            payload = self.getDataDictionary()
        else:
            payload = data

        self.console.log("data=%s timestamp=%s", (payload["data"],payload["timestamp"]))
        self.db.updateData(self.path, payload)


    def setUptateTime(self, seconds):
        self.timerInterval = seconds
        self.console.log("Setting Periodic updates to %s minutes", self.timerInterval)
        self.job.reschedule(trigger='interval', minutes=self.timerInterval)


    def setPeriodicDBUpdates(self):
        self.console.log("Starting periodic updates to DB")
        self.job.resume()

    def stopPeriodicDBUpdates(self):
        self.console.log("Stopping periodic updates to DB")
        self.job.pause()

    #-------------------------------------------------------------
    #Destroyer Method
    def __del__(self):
        self.closeStreams()
        self.scheduler.shutdown(wait=False)
        pass


if __name__ == '__main__':
    # Main Loop
    pass
