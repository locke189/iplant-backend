'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import sys
import datetime
from DataLogger import DataLogger


class Sensor:
    def __init__(self, device, sensorId, type, version, enabled):
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
        self.dataLogger = DataLogger('sensorinit',device.storage,"/"+self.path+"/")

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
            "filterSamples": self.filterSamples,
            "dataset": self.dataset,
            "datasetAvg": self.datasetAvg,
            "datasetLabel": self.datasetLabel,
            "historic": self.dataLogger.logInfo["logs"]
            }
        return data

    #Updates data into the Database
    def saveSensorToDB(self):
        data = self.getSensorData()
        self.db.updateData(self.path,data)
        print("Sensor Saved")

    #Saves data into a file
    def saveHistoricRecord(self):
        self.historicFilename = "device_" + self.device.id + "_sensor_" + self.id + "_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".txt"
        fileData = str(self.timestamp) + "," + str(self.data)
        if self.filter:
            fileData += "," + str(self.avgData)
        fileData +=  "\n"

        file = open(self.historicFilename,"a")
        file.write(fileData)
        file.close()
        return self.historicFilename

    #Saves historic data into cloud storage
    def saveHistoricRecordToStorage(self):
        path = self.storageRoute + self.historicFilename
        self.device.storage.saveFile(path,self.historicFilename)


    def datasetDataEntry(self):
        if(len(self.dataset) == self.datasetMax):
            self.datasetAvg.pop(0)
            self.dataset.pop(0)
            self.datasetLabel.pop(0)

        self.datasetAvg.append(self.avgData)
        self.dataset.append(self.data)
        self.datasetLabel.append(datetime.datetime.now().strftime("%H:%M"))



if __name__ == '__main__':




    # Main Loop
    pass
