import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'iPlantBackend')))

from Model import Sensor
from Database import Database
from Database import Storage
from Broker import Broker

import unittest
from random import randint
from math import floor
import time

#initial setup
config = {
  "apiKey": "AIzaSyCeLjnaoNZ6c9BKkccXt5E0H74DGKJWXek",
  "authDomain": "testproject-cd274.firebaseapp.com",
  "databaseURL": "https://testproject-cd274.firebaseio.com",
  "storageBucket": "testproject-cd274.appspot.com"
}
#Database startup
db = Database.Database(config,logs=False)

#storage startup
store = Storage.Storage(config, logs=False)

broker = Broker.Broker(topic="topic/channel", logs = False, logName='SensorBroker')
broker.setCallbacks()
broker.start()


class TestSensorClass(unittest.TestCase):

    localData = 1
    databaseData = 2
    sent_payload = 100
    received_payload = 200
    changedEnabledState = False


    #Database startup
    sensor = Sensor.Sensor(database = db, storage = store, broker= broker, id=200, type="TST", enabled=True, devicePath="/devices/id", logs=False, filterSamples=3, datasetLength = 3, skipSamples=2)


    def test_it_should_filter_data_from_sensors(self):
        x = randint(0,9)
        y = randint(0,9)
        z = randint(0,9)
        average = floor( (x+y+z)/3 )
        broker.publishMessage("/devices/id/sensors/200/data", x)
        broker.publishMessage("/devices/id/sensors/200/data", y)
        broker.publishMessage("/devices/id/sensors/200/data", z)
        time.sleep(2)
        self.assertEqual(average, floor(self.sensor.avgFilter.getValue()) )

        x = 3
        y = 6
        z = 3
        average = 4
        broker.publishMessage("/devices/id/sensors/200/data", x)
        broker.publishMessage("/devices/id/sensors/200/data", y)
        broker.publishMessage("/devices/id/sensors/200/data", z)
        time.sleep(2)
        self.assertEqual(average, floor(self.sensor.avgFilter.getValue()) )
        pass


    def test_it_should_save_datasets_to_database(self):
        pass



if __name__ == '__main__':
    pass
