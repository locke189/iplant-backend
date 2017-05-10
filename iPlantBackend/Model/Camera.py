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
from apscheduler.schedulers.background import BackgroundScheduler
import time

class Camera(Base.Base):

    actions = { "OFF":      0,
                "ON":       1,
                "TOGGLE":   2,
                "ERROR":    False,
                "IDLE":     False,
                "CAPTURE":  3,
                "START":    4,
                "STOP":     5 }


    def __init__(self, database, broker, id, type, enabled, settings, devicePath, logs=True, maxRetry=3, retryTime=10):

        #Initializing Base class
        super().__init__(database, broker, id, type, enabled, devicePath, categoryPath="/actuators/", logs = logs)


        #retry mechanism
        self.busy = False
        self.retry = 0
        self.maxRetry = maxRetry
        self.retryTime = retryTime
        #settingsFilename

        self.settings = settings

        #actions
        self.action = "IDLE"
        self.saveDataToDB()
        time.sleep(2)

        #Broker subscriptions
        self.subscribeDataTopic()
        self.broker.subscribeTopicWithCallback(self.path +"/ack" , self.receiveAck )

        self.streamFromDB("enabled", self.changeEnabledStateFromDB)
        self.streamFromDB("actions", self.changeActionsFromDB)
        self.streamFromDB("settings", self.changeSettingsFromDB)



        # Scheduler
        self.jobId = self.path.replace("/","")
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.job = self.scheduler.add_job(self.publishAndRetry, 'interval', seconds=self.retryTime, id=self.jobId, replace_existing=True)
        self.job.pause()


    #Sets the dictionary that is going to be sent to the database.
    def getDataDictionary(self):
        data = {
            "id": self.id,
            "type": self.type,
            "enabled": self.enabled,
            "data":  self.data,
            "timestamp": self.timestamp,
            "busy": self.busy,
            "actions": self.action,
            "settings": self.settings,
            }
        return data


    #-------------------------------------------------------------------------
    # Streaming methods
    # The following methods should deal with data comming in from the database.
    def changeEnabledStateFromDB(self, message):
        super().changeEnabledStateFromDB(message)
        self.broker.publishMessage(self.path + "/enabled", self.enabled)


    def changeActionsFromDB(self, message):
        if not self.busy:
            self.action = str(message["data"]).upper()
            if (self.action != "IDLE") :
                self.console.log("Action from remote: %s", self.action)
                if self.action in self.actions.keys():
                    self.message = self.actions[self.action]
                    self.busy = True
                    self.db.setData(self.path + "/busy", self.busy)
                    self.publishAndRetry()
                else:
                    self.console.log("Unrecognized action from remote: %s", self.action)
                    self.action = "IDLE"
                    self.saveDataToDB()
        else:
            self.action = "IDLE"
            self.saveDataToDB()

    def changeSettingsFromDB(self, message):
        if not self.busy:
            self.console.log("Path: %s", message["path"])
            self.console.log("data: %s", message["data"])
            if message['path'] != "/":
                self.busy = True
                self.db.setData(self.path + "/busy", self.busy)
                key = message['path'].replace("/","")
                if key in self.settings.keys():
                    self.settings[key] = message["data"]
                    self.message = message["data"]
                    self.publishAndRetry(self.path + "/settings/" + key)
                else:
                    self.busy = False
                    self.db.setData(self.path + "/busy", self.busy)

        else:
            if message['path'] != "/":
                key = message['path'].replace("/","")
                if key in self.settings.keys():
                    self.db.setData(self.path + "/settings/" + key, self.settings[key])


    def publishAndRetry(self, topic=""):
        if topic == "":
            topic = self.path

        if self.busy:
            if(self.retry < self.maxRetry):
                self.retry += 1
                self.console.log("Sending message attempt %s", self.retry)
                self.broker.publishMessage(topic, self.message)
                self.job.resume()
            elif self.busy and self.retry >= self.maxRetry:
                self.console.log("TIMEOUT: maximum attemps reached")
                self.busy = False
                self.retry = 0
                self.action = "TIMEOUT"
                self.saveDataToDB()
                self.job.pause()
            else:
                self.busy = False
                self.retry = 0
                self.action = "IDLE"
                self.saveDataToDB()
                self.job.pause()


    # Overide of setData method to include resetting of busy and
    #retry signals
    def setData(self, topic, payload):
        super().setData(topic,payload)
        self.job.pause()
        self.busy = False
        self.retry = 0
        self.action = "IDLE"
        self.saveDataToDB()



    def receiveAck(self, topic, payload):
        self.job.pause()
        self.busy = False
        self.retry = 0
        self.action = "IDLE"
        self.saveDataToDB()


if __name__ == '__main__':
    # Main Loop
    pass
