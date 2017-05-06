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
import threading


class DeviceManager:

    def __init__(self, database, storage, topic="regDevice",logs=True, logName="DeviceManager", pingTimer = 600, pingPath='ping'):
        self.devices = []
        #Initializing loger
        self.console = Logger.Logger(logName=logName, enabled=logs, printConsole=True)
        #Initializing broker
        self.broker = Broker.Broker(topic=topic, logs = True, logName=logName)
        self.broker.setCallbacks()
        self.broker.start()
        self.broker.subscribeTopicWithCallback(topic, self.brokerCallback )
        self.db = database
        self.storage = storage
        self.pingPath = pingPath
        self.pingTimer = pingTimer
        self.timerInterval = 30
        self.response = False
        self.callPing()


    def brokerCallback(self, topic, payload):
        self.response = True
        payload2 = payload.replace("'", '"')
        self.console.log("Broker callback")
        data  = json.loads(payload2)
        self.console.log("Data: %s", data)
        self.console.log("Device ID: %s, Type: %s", (data['id'], data['type']))

        print( list(filter(lambda device: device.id == data['id'], self.devices) ))

        if ( list(filter(lambda device: device.id == data['id'], self.devices)) == []):
            self.console.log("New Device")
            self.devices.append( Device.Device(database=self.db, storage=self.storage, id=data['id'], type=data['type'], broker = self.broker, enabled=True))
        else:
            self.console.log("Device already exists")

        threading.Timer(self.pingTimer, self.callLongPing).start()

    def callPing(self):
        
        if not self.response:
            self.console.log("Sending PING message...")
            self.broker.publishMessage(self.pingPath, '0')
            threading.Timer(self.timerInterval, self.callPing).start()


    def callLongPing(self):
        self.response = False
        self.console.log("Sending PING message...")
        self.broker.publishMessage(self.pingPath, '0')
        threading.Timer(self.timerInterval, self.callPing).start()


if __name__ == '__main__':

    # Main Loop
    pass
