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
import threading
import time

class Actuator(Base.Base):

    actions = { "OFF":      0,
                "ON":       1,
                "TOGGLE":   2,
                "ERROR":    False,
                "IDLE":     False,
                "CAPTURE":  3,
                "START":    4,
                "STOP":     5 }


    def __init__(self, database, broker, id, type, enabled, devicePath, logs=True, maxRetry=2, retryTime=8):

        #Initializing Base class
        super().__init__(database, broker, id, type, enabled, devicePath, categoryPath="/actuators/", logs = logs)


        #retry mechanism
        self.busy = False
        self.retry = 0
        self.maxRetry = maxRetry
        self.retryTime = retryTime

        #actions
        self.action = "IDLE"
        self.saveDataToDB()

        self.subscribeDataTopic()
        self.streamFromDB("enabled", self.changeEnabledStateFromDB)
        self.streamFromDB("actions", self.changeActionsFromDB)


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
                    time.sleep(2)


    def publishAndRetry(self):
        if self.busy:
            if(self.retry < self.maxRetry):
                self.retry += 1
                self.console.log("Sending message attempt %s", self.retry)
                self.broker.publishMessage(self.path, self.message)
                self.timer = threading.Timer(self.retryTime, self.publishAndRetry).start()
            elif self.busy and self.retry >= self.maxRetry:
                self.console.log("TIMEOUT: maximum attemps reached")
                self.busy = False
                self.retry = 0
                self.action = "TIMEOUT"
                self.saveDataToDB()
                time.sleep(2)
            else:
                self.busy = False
                self.retry = 0
                self.action = "IDLE"
                self.saveDataToDB()
                time.sleep(2)


    # Overide of setData method to include resetting of busy and
    #retry signals
    def setData(self, topic, payload):
        super().setData(topic,payload)
        self.busy = False
        self.retry = 0
        self.action = "IDLE"
        self.saveDataToDB()
        time.sleep(2)



if __name__ == '__main__':
    # Main Loop
    pass
