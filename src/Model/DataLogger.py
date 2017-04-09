'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import sys
import datetime
import os.path
import json

class DataLogger:
    def __init__(self, initFile, storage, storageRoute, logPrefix = ""):
        self.initFile = initFile
        self.logInfo = {} #metadata of the existing logs
        self.storage = storage
        self.storageRoute = storageRoute
        self.logPrefix = logPrefix
        self.logData = {} #Actual data of a log
        self.openInitFile()


    def openInitFile(self):
        #Open init file if it doesn't exist then creates it

        logInfo = {}
        logInfo['logs'] = []
        logInfo['openLog'] = self.getLogFile()

        if(not os.path.exists(self.initFile) ):
            self.saveFile(self.initFile,logInfo)
            self.createNewLog(self.getLogFile())

        self.logInfo = self.loadFile(self.initFile)
        self.logData = self.loadFile(self.logInfo['openLog'])
        self.saveLogToStorage(self.logInfo['openLog'])

    def getFilePath(self, logFile):
        return self.logPrefix + logFile + '.json'

    def saveFile(self, file, data):
        filepath = self.getFilePath(file)
        if(not os.path.exists(filepath) ):
            with open(filepath, 'w') as outfile:
                json.dump(data, outfile)

    def loadFile(self, file):
        filepath = self.getFilePath(file)
        if(not os.path.exists(filepath) ):
            with open(filepath) as data_file:
                return json.load(data_file)

    #Saves historic data into cloud storage
    def saveLogToStorage(self, file):
        filepath = self.getFilePath(file)
        path = self.storageRoute + self.filepath
        url = self.storage.saveFile(path,filepath)
        return url

    def createNewLog(self, logFile):
        self.logInfo['openLog'] = logFile
        logData = {}
        logData['data'] = []
        logData['dataAvg'] = []
        logData['label'] =  []
        self.saveFile(logFile, logData)
        self.logData = self.loadFile(logFile)
        url = self.saveLogToStorage(logFile):
        self.logInfo['logs'].append({'date': logFile, 'url': url})
        self.saveFile(self.initFile, self.logInfo)



    def newLogEntry(self, data, dataAvg, label):
        logFile = self.getLogFile()
        self.checkLogOpen(logFile)
        self.logData['data'].append(data)
        self.logData['dataAvg'].append(dataAvg)
        self.logData['label'].append(label)
        self.saveFile(logFile, self.logData)


    def getLogFile(self):
        return datetime.datetime.now().strftime("%Y-%m-%d")


    def checkLogOpen(self, logFile):
        if (self.logInfo['openLog'] != logFile):
            self.saveLogToStorage(self.logInfo['openLog'])
            self.createNewLog(logfile)





if __name__ == '__main__':
    print('Starting Program')
    logger = DataLogger('device0.json')

    pass
