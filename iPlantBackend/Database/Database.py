#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import pyrebase
from Shared import Logger

class Database:
    def __init__(self,options,logs = True, debug=False):
        self.console = Logger.Logger(logName='Database', enabled=logs, printConsole=True)
        self.console.log("Initialization...")
        self.firebase = pyrebase.initialize_app(options)
        self.db = self.firebase.database()
        self.debug = debug
        self.streams = {}

    def setData(self, path, data):
        self.console.log("Database SET")
        self.db.child(path).set(data)
        if self.debug:
            self.console.log("SET: %s -> %s" ,( path,str(data) ) )

    def updateData(self, path, data):
        self.console.log("Database UPDATE")
        self.db.child(path).update(data)
        if self.debug:
            self.console.log("UPDATE: %s -> %s" ,( path,str(data) ) )

    def pushData(self, path, data):
        self.console.log("Database PUSH")
        self.db.child(path).push(data)
        if self.debug:
            self.console.log("PUSH: %s -> %s" ,( path,str(data) ) )

    def getData(self, path):
        self.console.log("Database GET")
        data = self.db.child(path).get()
        if (data != None):
            if self.debug:
                self.console.log("GET: %s -> %s" ,( path,str(data.val()) ) )
        else:
            if self.debug:
                self.console.log("GET: %s -> NO DATA" , path  )
        return data.val()

    def setStream(self, path, function):
        self.console.log("Streaming: %s " , path )
        self.streams[path] = self.db.child(path).stream(function)

    def closeStream(self, path):
        self.console.log("Closing stream: %s " , path )
        self.streams[path].close()

    def __del__(self):
        pass

if __name__ == '__main__':
    #initial setup
    config = {
      "apiKey": "AIzaSyCeLjnaoNZ6c9BKkccXt5E0H74DGKJWXek",
      "authDomain": " testproject-cd274.firebaseapp.com",
      "databaseURL": "https://testproject-cd274.firebaseio.com",
      "storageBucket": " testproject-cd274.appspot.com"
    }

    #Database startup
    DB = Database(config)

    #Read database
    #DB.getData("devices")
    DB.getData("users")

    #Write in database
    data = {"data": [10,20,30,40,50],
            "name": "Monty Burns"}

    DB.setData("users/test",data)


    pass
