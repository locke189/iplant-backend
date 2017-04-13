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
    def __init__(self,options,logs = True):
        self.console = Logger.Logger(logName='Database', enabled=logs, printConsole=True)
        self.console.log("Initialization...")
        self.firebase = pyrebase.initialize_app(options)
        self.db = self.firebase.database()

    def setData(self, path, data):
        self.db.child(path).set(data)
        #print("SET: " + path + " -> " + str(data) )
        self.console.log("SET: %s -> %s" ,( path,str(data) ) )

    def updateData(self, path, data):
        self.db.child(path).update(data)
        #print("UPDATE: " + path + " -> " + str(data) )
        self.console.log("UPDATE: %s -> %s" ,( path,str(data) ) )

    def pushData(self, path, data):
        self.db.child(path).push(data)
        #print("PUSH: " + path + " -> " + str(data) )
        self.console.log("PUSH: %s -> %s" ,( path,str(data) ) )

    def getData(self, path):
        data = self.db.child(path).get()
        if (data != None):
            #print("GET: " + path + " <- " )
            #print(data.val())
            self.console.log("GET: %s -> %s" ,( path,str(data.val()) ) )
        else:
            self.console.log("GET: %s -> NO DATA" , path  )
        return data.val()



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
