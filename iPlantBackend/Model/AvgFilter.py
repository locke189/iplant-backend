#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import sys
import datetime
from Model import DataLogger
from Shared import Logger
from Broker import Broker

class AvgFilter:
    def __init__(self, path ="", logs=True):
        #Filter inits disabled
        self.enabled = False
        self.avgData = 0
        self.filterSamples = 5

        #Initializaing logger
        self.console = Logger.Logger(logName="(Avg Filter: " + path + ")", enabled=logs, printConsole=True)
        self.console.log("Initialization...")
        pass

    def isEnabled(self):
        return self.enabled

    #Running AVG filter implementation
    def enable(self, samples):
        self.console.log("Enabling AVG filter - %s samples", (samples))
        self.enabled = True
        self.filterSamples = samples
        self.filterData = [0] * self.filterSamples
        self.avgData = 0

    def run(self, data):
        self.console.log("Filtering")
        self.filterData.pop()
        self.filterData.insert(0,int(data))
        self.avgData = sum(self.filterData)/self.filterSamples


    def disable(self):
        self.console.log("AVG Filter disabled")
        self.filter = False
        self.avgData = ""
        self.filterSamples = ""


    def getValue(self):
        return self.avgData
