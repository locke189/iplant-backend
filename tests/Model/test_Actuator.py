import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'iPlantBackend')))

from Model import Actuator
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

def iAmACallbackFunction(topic, payload):
    broker.publishMessage("/devices/id/actuators/300/data", payload)
    time.sleep(2)

#Database startup
db = Database.Database(config,logs=True)

broker = Broker.Broker(topic="topic/channel", logs = True, logName='ActuatorBroker')
broker.setCallbacks()
broker.start()
broker.subscribeTopicWithCallback("/devices/id/actuators/300/actions", iAmACallbackFunction)



class TestActuatorClass(unittest.TestCase):


    #Database startup
    actuator = Actuator.Actuator(database = db, broker= broker, id=300, type="TST", enabled=True, devicePath="/devices/id", logs=True)


    def test_it_should_detect_changes_in_enabled_from_db(self):
        time.sleep(5)
        action = "on"
        db.setData(self.actuator.path + "/actions", action)
        time.sleep(5)
        self.actuator.closeStreams()
        self.assertEqual(self.actuator.data, str(self.actuator.actions[action.upper()]) )
        pass



if __name__ == '__main__':
    pass
