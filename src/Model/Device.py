#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''
from Sensor import Sensor
import sys
import datetime
from Shared import Logger

class Device:
    def __init__(self, database, storage, id, type, version, enabled, basePath="", logs=True, logName="Device"):
        self.console = Logger.Logger(logName=logName, enabled=logs, printConsole=True)
        self.console.log("Initialization...")
        self.db = database
        self.storage = storage
        self.id = id
        self.type = type
        self.version = version
        self.enabled =enabled
        self.sensors = {}
        self.actuators = {}
        self.path = basePath + "devices/" + str(self.id)

    def getDeviceData(self):
        data = {
            "id": self.id,
            "type": self.type,
            "version": self.version,
            "enabled": self.enabled,
            "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            }

        return data


    def saveDeviceToDB(self):
        self.console.log("Saving device data to database")
        data = self.getDeviceData()
        self.db.updateData(self.path,data)
        print("Device Saved")
        for sensorId in self.sensors.keys():
            self.sensors[sensorId].saveSensorToDB()

    def addSensor(self, sensorId, type, version, enabled):
        self.console.log("Adding sensor(%s) %s ",(sensorId, type))
        self.sensors[sensorId] = Sensor(self, sensorId, type, version, enabled)




if __name__ == '__main__':
    pass
