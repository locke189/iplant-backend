'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''
from Sensor import Sensor
import sys
import datetime

class Device:
    def __init__(self, database, storage, id, type, version, enabled, basePath=""):
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
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        return data


    def saveDeviceToDB(self):
        data = self.getDeviceData()
        self.db.updateData(self.path,data)
        print("Device Saved")
        for sensorId in self.sensors.keys():
            self.sensors[sensorId].saveSensorToDB()

    def addSensor(self, sensorId, type, version, enabled):
        self.sensors[sensorId] = Sensor(self, sensorId, type, version, enabled)




if __name__ == '__main__':
    pass
