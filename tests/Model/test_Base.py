import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'iPlantBackend')))

from Model import Base
from Database import Database
from Broker import Broker

import unittest
from random import randint
import time

#initial setup
config = {
  "apiKey": "AIzaSyCeLjnaoNZ6c9BKkccXt5E0H74DGKJWXek",
  "authDomain": " testproject-cd274.firebaseapp.com",
  "databaseURL": "https://testproject-cd274.firebaseio.com",
  "storageBucket": " testproject-cd274.appspot.com"
}
#Database startup
db = Database.Database(config,logs=True)

broker = Broker.Broker(topic="topic/channel", logs = False, logName='baseBroker')
broker.setCallbacks()
broker.start()


class TestBaseClass(unittest.TestCase):

    localData = 1
    databaseData = 2
    sent_payload = 100
    received_payload = 200
    changedEnabledState = False


    #Database startup
    base = Base.Base(database = db, broker= broker, id=100, type="TST", enabled=True, devicePath="/devices/id", categoryPath="/category/", dataTopic = "/data", logs=True, maxSampleCount=5)
    base2 = Base.Base(database = db, broker= broker, id=100, type="TST", enabled=True, devicePath="/devices/id", categoryPath="/category/", dataTopic = "/data", logs=False, maxSampleCount=5)

    def test_it_should_save_data_from_database(self):
        self.base.data = randint(0,9)
        self.localData = self.base.getDataDictionary()
        self.base.saveDataToDB(self.localData)
        time.sleep(1)
        self.databaseData = self.base.loadDataFromDB()
        self.assertEqual(self.localData, self.databaseData)
        self.assertEqual(self.localData["data"],self.databaseData["data"])
        pass


    def test_it_should_save_data_from_broker_messages(self):
        self.sent_payload = randint(0,9)
        self.base2.subscribeDataTopic()
        broker.publishMessage("/devices/id/category/100/data", self.sent_payload)
        time.sleep(1)
        self.assertEqual(str(self.sent_payload), self.base2.data)
        pass

    def test_it_should_detect_enabled_changes_from_db(self):
        self.base.streamFromDB("enabled", self.base.changeEnabledStateFromDB)
        self.sent_enable = not(self.base.enabled)
        db.setData(self.base.path + "/enabled", self.sent_enable)
        time.sleep(1)
        self.base.closeStreams()

        self.assertEqual(self.base.enable, self.sent_enable )
        pass


if __name__ == '__main__':
    pass
