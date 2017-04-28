import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'iPlantBackend')))
from Database import Database

from random import randint
import unittest
import random
import time





class TestDatabase(unittest.TestCase):


    #initial setup
    config = {
      "apiKey": "AIzaSyCeLjnaoNZ6c9BKkccXt5E0H74DGKJWXek",
      "authDomain": " testproject-cd274.firebaseapp.com",
      "databaseURL": "https://testproject-cd274.firebaseio.com",
      "storageBucket": " testproject-cd274.appspot.com"
    }

    #Database startup
    db = Database.Database(config,logs=False)
    db2 = Database.Database(config,logs=False)

    #TestData
    data = {"data": [10,20,30,40,50],
            "name": "Monty Burns",
            "random": random.random(),
            "stream": randint(0,9),
            "stream2": randint(0,9) }

    #Test Database PATH
    path = "/test/backend-test/"
    streamPath = path + "stream"
    streamPath2 = path + "stream2"

    received_event = ""
    received_path = ""
    received_data = ""

    received_event2 = ""
    received_path2 = ""
    received_data2 = ""

    def streamingHandler(self, message):
        self.received_event = message["event"]  #PUT POST etc
        self.received_path = message["path"] #always returns "/" for some reason
        self.received_data = message["data"]

    def streamingHandler2(self, message):
        self.received_event2 = message["event"]  #PUT POST etc
        self.received_path2 = message["path"] #always returns "/" for some reason
        self.received_data2 = message["data"]

    def test_save_data_using_setData(self):
        self.db.setData(self.path, self.data)
        data = self.db.getData(self.path)
        self.assertEqual(data, self.data)

    def test_streaming_of_data(self):
        self.db.setStream(self.streamPath, self.streamingHandler)
        self.db.setStream(self.streamPath2, self.streamingHandler2)
        self.sent_data = randint(10,99)
        self.sent_data2 = randint(10,99)
        self.db.setData(self.streamPath, self.sent_data)
        self.db.setData(self.streamPath2, self.sent_data2)
        time.sleep(1)
        self.db.closeStream(self.streamPath)
        self.db.closeStream(self.streamPath2)
        self.assertEqual(self.received_data, self.sent_data)
        self.assertEqual(self.received_data2, self.sent_data2)




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    pass
