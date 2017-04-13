#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import sys
import datetime
import os.path
import json
from Shared import Logger

class DataLogger:
    def __init__(self, initFile, storage, storageRoute,device, logPrefix = "", logs = True,logName='Data Logger'):
        self.console = Logger.Logger(logName=logName, enabled=logs, printConsole=True)
        self.console.log("Initialization...")
        self.initFile = initFile
        self.logInfo = {} #metadata of the existing logs
        self.storage = storage
        self.storageRoute = str(storageRoute)
        self.logPrefix = logPrefix
        self.logData = {} #Actual data of a log
        self.device = device
        self.openInitFile()



    def openInitFile(self):
        #Open init file if it doesn't exist then creates it
        self.console.log("Opening init file")
        logInfo = {}
        logInfo['logs'] = []
        logInfo['openLog'] = self.getLogFile()

        self.downloadFromStorage(self.initFile)


        if(not os.path.exists(self.getFilePath(self.initFile)) ):
            self.console.log("Init file does not exist")
            self.console.log("Creting init file -> %s", self.getFilePath(self.initFile))
            self.saveFile(self.initFile,logInfo)
            self.logInfo = self.loadFile(self.initFile)
            self.createNewLog(self.getLogFile())
            self.saveLogToStorage(self.initFile)

        self.console.log("Opening init file...")
        self.logInfo = self.loadFile(self.initFile)

        if(not os.path.exists(self.getFilePath(self.logInfo['openLog'])) ):
            self.console.log("Open log file does not exist")
            self.downloadFromStorage(self.logInfo['openLog'])

        self.console.log("Opening log file...")
        self.logData = self.loadFile(self.logInfo['openLog'])
        self.saveLogToStorage(self.logInfo['openLog'])

    def getFilePath(self, logFile):
        return self.logPrefix + logFile + '.json'

    def saveFile(self, file, data):
        self.console.log("Saving data to local disk => %s", file)
        filepath = self.getFilePath(file)
        with open(filepath, 'w') as outfile:
            json.dump(data, outfile)

    def loadFile(self, file):
        self.console.log("Loading data from local disk => %s", file)
        filepath = self.getFilePath(file)
        if(os.path.exists(filepath)):
            with open(filepath) as data_file:
                return json.load(data_file)

        self.console.log("File does not exist")

    #Saves historic data into cloud storage
    def saveLogToStorage(self, file):
        self.console.log("Uploading log file to storage.")
        filepath = str(self.getFilePath(file))
        path = self.storageRoute + filepath
        url = self.device.storage.saveFile(path,filepath)
        return url

    #gets data from storage
    def downloadFromStorage(self, file):
        self.console.log("Downloading log file from storage.")
        filepath = str(self.getFilePath(file))
        path = self.storageRoute + filepath
        url = self.device.storage.downloadFile(path,filepath)
        return url

    def createNewLog(self, logFile):
        self.console.log("Creating new log file %s", logFile)
        logData = {}
        logData['dataset'] = []
        logData['datasetAvg'] = []
        logData['datasetLabel'] =  []
        self.saveFile(logFile, logData)
        self.logData = self.loadFile(logFile)
        self.logInfo['openLog'] = logFile
        url = self.saveLogToStorage(logFile)
        self.logInfo['logs'].append({'date': logFile, 'url': url})
        self.saveFile(self.initFile, self.logInfo)
        self.saveLogToStorage(self.initFile)




    def newLogEntry(self, data, dataAvg, label):
        self.console.log("Creating new log entry", )
        logFile = self.getLogFile()
        self.checkLogOpen(logFile)
        self.logData['dataset'].append(data)
        self.logData['datasetAvg'].append(dataAvg)
        self.logData['datasetLabel'].append(label)
        self.saveFile(logFile, self.logData)


    def getLogFile(self):
        #The name of the logfile es automatically chosen
        #using the current date. 1 log per day.
        return datetime.datetime.now().strftime("%Y-%m-%d")


    def checkLogOpen(self, logFile):
        if (self.logInfo['openLog'] != logFile):
            self.saveLogToStorage(self.logInfo['openLog'])
            self.createNewLog(logFile)





if __name__ == '__main__':
    print('Starting Program')
    logger = DataLogger('device0.json')

    pass
