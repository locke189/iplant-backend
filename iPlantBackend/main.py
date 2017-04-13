#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import datetime
from Model import Device, Sensor
from Database import Database, Storage
from Shared import Logger

#creates Application Logger
console = Logger.Logger(logName='Application', enabled=True, printConsole=True)

# Create a TCP/IP socket
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port
server_address = ('', 333)
console.log('starting up on %s port %s', server_address)
#print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

#DeviceSetup
#Database startup
    #initial setup
config = {
  "apiKey": "AIzaSyCeLjnaoNZ6c9BKkccXt5E0H74DGKJWXek",
  "authDomain": "testproject-cd274.firebaseapp.com",
  "databaseURL": "https://testproject-cd274.firebaseio.com",
  "storageBucket": "testproject-cd274.appspot.com"
}
#DB = Database.Database(config)
#store = Storage.Storage(config)

#create a device
#device = Device.Device(database=DB, storage=store, id="0", type="iplant", version="Beta", enabled=True)

#subscribe a sensor
#device.addSensor("0", "MST", "beta", True)

#save device into db
#device.saveDeviceToDB()

#acivate filter run
#update sensor data
#device.sensors["0"].filterEnable(30)

# Listen for incoming connections


count = 0

while True:
    sock.listen(5)
    # Wait for a connection
    #print >>sys.stderr, 'waiting for a connection'
    console.log('Waiting for a connection')
    connection, client_address = sock.accept()
    connection.settimeout(90)
    try:
        #print >>sys.stderr, 'connection from', client_address
        console.log('Connection from IP=%s, PORT=%s', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            #print >>sys.stderr, 'received "%s"' % data
            console.log('received "%s"', data)

            if data:
                #print >>sys.stderr, 'Saving Data'
                #update sensor data
                console.log("Updating Sensor 0 data")
                #device.sensors["0"].updateData(data)

                if count == 2:
                    #Save sensor data to DB
                    console.log("Saving Sensor 0 Dataset")
                    #device.sensors["0"].datasetDataEntry()
                    console.log("Saving Sensor 0 data to DB")
                    #device.sensors["0"].saveSensorToDB()
                    count = 0
                else:
                    count += 1

    except Exception, e:
        #print >> sys.stderr, 'Error exception!'
        #print >> sys.stderr, str(e)
        console.log('ERROR: Exception')
        console.log('ERROR: "%s"', str(e) )


        connection.close()
        # Clean up the connection


    finally:
        # Clean up the connection
        #print >> sys.stderr, 'Error finally!'
        console.log("ERROR: CLEANUP")
        connection.close()
