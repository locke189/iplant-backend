#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Nov 7, 2015
Don't blink...
@author: Juan_Insuasti
'''

import pyrebase


class Storage:
    def __init__(self,options):
        self.firebase = pyrebase.initialize_app(options)
        self.storage = self.firebase.storage()

    def saveFile(self, path, file):
        self.storage.child(path).put(file)
        print("Saving: " + str(file) + " -> " + path )
        url = self.storage.child(path).get_url(1)
        print("URL: " + str(url) )
        return url


    def getUrl(self, path):
        url = self.storage.child(path).get_url(1)
        print("URL: " + str(url) )
        return url





if __name__ == '__main__':
    #initial setup
    config = {
      "apiKey": "AIzaSyCeLjnaoNZ6c9BKkccXt5E0H74DGKJWXek",
      "authDomain": "testproject-cd274.firebaseapp.com",
      "databaseURL": "https://testproject-cd274.firebaseio.com",
      "storageBucket": "testproject-cd274.appspot.com"
    }

    #storage startup
    store = Storage(config)

    #save a file
    print("Testing file save...")
    url = store.saveFile("test/testfile.txt","test.txt")
    print("Returned URL... " + url)
    #get url
    print("Testing getting url...")
    url2 = store.getUrl("test/testfile.txt")
    print("Returned URL2... " + url2)

    pass
