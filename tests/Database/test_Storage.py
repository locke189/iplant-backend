import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'iPlantBackend')))
from Database import Storage

from random import randint
import unittest
import random
import time
import json




class TestStorage(unittest.TestCase):


    #initial setup
    config = {
      "apiKey": "AIzaSyCeLjnaoNZ6c9BKkccXt5E0H74DGKJWXek",
      "authDomain": " testproject-cd274.firebaseapp.com",
      "databaseURL": "https://testproject-cd274.firebaseio.com",
      "storageBucket": "testproject-cd274.appspot.com"
    }

    #Database startup
    storage = Storage.Storage(config,logs=False)


    #TestData
    data = {"data": [10,20,30,40,50],
            "name": "Monty Burns",
            "random": random.random(),
            "stream": randint(0,9),
            "stream2": randint(0,9) }

    #Test Stirage PATH
    path = "/test/backend-test/"
    file = "test.json"

    def test_save_data_to_storage(self):
        with open(self.file, 'w') as outfile:
            json.dump(self.data, outfile)

        self.storage.saveFile(self.path + self.file, self.file)

        self.assertEqual(self.data, self.data)







if __name__ == '__main__':
    pass
