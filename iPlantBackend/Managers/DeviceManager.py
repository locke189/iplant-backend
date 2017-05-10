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
from Model import Device
from Broker import Broker



class DeviceManager:

    def __init__(self, database, storage, topic="regDevice",logs=True, logName="DeviceManager", pingPath='ping'):
        self.devices = {}
        #Initializing loger
        self.console = Logger.Logger(logName=logName, enabled=logs, printConsole=True)
        #Initializing broker
        self.broker = Broker.Broker(topic=topic, logs = True, logName=logName)
        self.regTopic = topic
        self.broker.setCallbacks()
        self.broker.start()
        self.broker.subscribeTopicWithCallback(topic, self.brokerCallback)
        self.db = database
        self.storage = storage
        self.pingPath = pingPath
        self.response = False



    def brokerCallback(self, topic, payload):
        self.response = True
        payload2 = payload.replace("'", '"')
        self.console.log("Broker callback")
        data = json.loads(payload2)
        self.console.log("Data: %s", data)
        self.console.log("Device ID: %s, Type: %s", (data['id'], data['type']))

        if(topic ==  self.regTopic):
            if(data['id'] not in self.devices.keys()):
                self.console.log("New Device")
                self.devices[data['id']] = Device.Device(database=self.db,
                                                         storage=self.storage,
                                                         id=data['id'],
                                                         type=data['type'],
                                                         broker=self.broker,
                                                         enabled=True)
            else:
                self.console.log("Device already exists")


if __name__ == '__main__':

    # Main Loop
    pass
