'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import sys
import datetime

class Sensor:
    def __init__(self, device, sensorId, type, version, enabled):
        self.db = device.db
        self.device = device
        self.id = sensorId
        self.type = type
        self.version = version
        self.enabled = enabled
        self.data = ""
        self.timestamp = ""
        self.path = device.path + "/sensors/" + str(self.id)
        self.timestamp = ""
        self.avgData = ""
        self.filter = False
        self.filterSamples = ""

    #Running AVG filter implementation
    def filterEnable(self, samples):
        self.filter = True
        self.filterSamples = samples
        self.filterData = [0] * self.filterSamples
        self.avgData = 0

    def filterRun(self, data):
        self.filterData.pop()
        self.filterData.insert(0,int(data))
        self.avgData = sum(self.filterData)/self.filterSamples
        print(self.filterData)
        print(self.avgData)

    def filterDisable(self):
        self.filter = False
        self.avgData = ""
        self.filterSamples = ""


    #Update sensor data from device readings
    def updateData(self, data):
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
            "filterSamples": self.filterSamples
            }
        return data

    #Updates data into the Database
    def saveSensorToDB(self):
        data = self.getSensorData()
        self.db.updateData(self.path,data)
        print("Sensor Saved")

    #Saves data into a file
    def saveHistoricRecord(self):
        filename = "device_" + self.device.id + "_sensor_" + self.id + "_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt"
        fileData = str(self.timestamp) + "," + str(self.data)
        if self.filter:
            fileData += "," + str(self.avgData)
        fileData +=  "\n"

        file = open(filename,"a")
        file.write(fileData)
        file.close()


if __name__ == '__main__':




    # Main Loop
    pass
