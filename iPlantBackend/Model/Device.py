#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''
from Model import Sensor
from Model import Actuator
import sys
import datetime
from Shared import Logger
from Broker import Broker
import json

class Device:
    def __init__(self, database, storage, id, type, broker, enabled, basePath="", topicSensor="/regSensor", topicActuator="/regActuator", logs=True, logName="Device"):
        self.db = database
        self.storage = storage
        self.online = True
        self.id = id
        self.type = type
        self.enabled = enabled
        self.sensors = {}
        self.actuators = {}
        self.path = basePath + "/devices/" + str(self.id)
        self.console = Logger.Logger(logName="Device("+self.path+")", enabled=logs, printConsole=True)
        self.topicSensor = self.path + topicSensor
        self.topicActuator = self.path + topicActuator
        self.console.log("Initialization...")
        #Initializing broker
        self.broker = broker
        self.broker.subscribeTopicWithCallback(self.topicSensor, self.brokerCallback )
        self.broker.subscribeTopicWithCallback(self.topicActuator, self.brokerCallback )
        self.broker.subscribeTopicWithCallback(self.path, self.onlineCheck )
        self.saveDeviceToDB()


    def onlineCheck(self, topic, payload):
        if topic == "connected":
            self.online = True
        if topic == "disconnected":
            self.online = False

    def brokerCallback(self, topic, payload):
        payload2 = payload.replace("'", '"')
        self.console.log("Broker callback")
        data  = json.loads(payload2)
        self.console.log("Topic: %s", topic)
        self.console.log("ID: %s, Type: %s", (data['id'], data['type']))

        if (topic ==  self.topicActuator):
            if ( data['id'] not in self.actuators.keys()):
                self.console.log("New Actuator")
                self.addActuator(data['id'], data['type'], True)
                self.saveDeviceToDB()
            else:
                self.console.log("Actuator already exists")

        elif (topic ==  self.topicSensor):
            if ( data['id'] not in self.sensors.keys()):
                self.console.log("New Sensor")
                self.addSensor(data['id'], data['type'], True)
                self.saveDeviceToDB()
            else:
                self.console.log("Sensor already exists")


    def getDeviceData(self):
        data = {
            "id": self.id,
            "type": self.type,
            "enabled": self.enabled,
            "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "online": self.online
            }

        return data


    def saveDeviceToDB(self):
        self.console.log("Saving device data to database")
        data = self.getDeviceData()
        self.db.updateData(self.path,data)
        for sensorId in self.sensors.keys():
            self.sensors[sensorId].saveDataToDB()
        for actuatorId in self.actuators.keys():
            self.actuators[actuatorId].saveDataToDB()

    def addSensor(self, sensorId, type, enabled):
        self.console.log("Adding sensor(%s) %s ",(sensorId, type))
        self.sensors[sensorId] = Sensor.Sensor(database=self.db, storage=self.storage, broker = self.broker, id=sensorId, type=type, enabled=enabled, filterSamples=30, devicePath= self.path, datasetLength = 24, skipSamples=30)

    def addActuator(self, actuatorId, type, enabled):
        self.console.log("Adding Actuator(%s) %s ",(actuatorId, type))
        self.actuators[actuatorId] = Actuator.Actuator(database=self.db, broker = self.broker, id=actuatorId, type=type, enabled=enabled, devicePath= self.path)





if __name__ == '__main__':
    pass
