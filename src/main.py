import socket
import sys
import datetime
from Model import Device, Sensor
from Database import Database, Storage


# Create a TCP/IP socket
sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port
server_address = ('', 333)
print >>sys.stderr, 'starting up on %s port %s' % server_address
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
DB = Database.Database(config)
store = Storage.Storage(config)
#create a device
device = Device.Device(database=DB, storage=store, id="0", type="iplant", version="Beta", enabled=True)

#subscribe a sensor
device.addSensor("0", "MST", "beta", True)

#save device into db
device.saveDeviceToDB()

#acivate filter run
#update sensor data
device.sensors["0"].filterEnable(30)

# Listen for incoming connections


count = 0

while True:
    sock.listen(5)
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    connection.settimeout(90)
    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print >>sys.stderr, 'Time "%s"' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print >>sys.stderr, 'received "%s"' % data
            if data:
                print >>sys.stderr, 'Saving Data'


                #update sensor data
                device.sensors["0"].updateData(data)

                #Save sensor historic data
                device.sensors["0"].saveHistoricRecord()


                if count == 30:
                    #Save sensor data to DB
                    device.sensors["0"].saveSensorToDB()
                    device.sensors["0"].saveHistoricRecordToStorage()
                    count = 0
                else:
                    count += 1

    except Exception, e:
        print >> sys.stderr, 'Error exception!'
        print >> sys.stderr, str(e)

        connection.close()
        # Clean up the connection


    finally:
        # Clean up the connection
        print >> sys.stderr, 'Error finally!'
        connection.close()
