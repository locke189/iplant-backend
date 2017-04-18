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

    def __init__(self, database, storage, topic="regDevice",logs=True, logName="DeviceManager"):
        self.devices = []
        #Initializing loger
        self.console = Logger.Logger(logName=logName, enabled=logs, printConsole=True)
        #Initializing broker
        self.broker = Broker.Broker(topic=topic, logs = True, logName=logName)
        self.broker.setCallback(self.brokerCallback)
        self.broker.start()
        self.db = database
        self.storage = storage


    def brokerCallback(self, topic, payload):
        payload2 = payload.replace("'", '"')
        self.console.log("Broker callback")
        data  = json.loads(payload2)
        self.console.log("Data: %s", data)
        self.console.log("Device ID: %s, Type: %s", (data['id'], data['type']))

        if ( filter(lambda device: device.id == data['id'], self.devices) == []):
            self.console.log("New Device")
            self.devices.append( Device.Device(database=self.db, storage=self.storage, id=data['id'], type=data['type'], version="Beta", enabled=True))
        else:
            self.console.log("Device already exists")


if __name__ == '__main__':

    # Main Loop
    pass
