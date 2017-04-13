import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'iPlantBackend')))
from Database import Database

import unittest
import random
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

    #TestData
    data = {"data": [10,20,30,40,50],
            "name": "Monty Burns",
            "random": random.random()}

    #Test Database PATH
    path = "/test/backend-test/"

    def test_save_data_using_setData(self):
        self.db.setData(self.path, self.data)
        data = self.db.getData(self.path)
        self.assertEqual(data, self.data)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    pass
