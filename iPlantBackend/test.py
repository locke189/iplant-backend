from Model import Device, Sensor
from Database import Database

if __name__ == '__main__':

    #initial setup
    config = {
      "apiKey": "AIzaSyCeLjnaoNZ6c9BKkccXt5E0H74DGKJWXek",
      "authDomain": " testproject-cd274.firebaseapp.com",
      "databaseURL": "https://testproject-cd274.firebaseio.com",
      "storageBucket": " testproject-cd274.appspot.com"
    }

    #Database startup
    DB = Database.Database(config)

    #create a device
    device = Device.Device(database=DB, id="0", type="iplant", version="Beta", enabled=True)

    #subscribe a sensor
    device.addSensor("0", "MST", "beta", True)

    #save device into db
    device.saveDeviceToDB()


    #update sensor data
    device.sensors["0"].updateData(100)


    #acivate filter run
    #update sensor data
    device.sensors["0"].filterEnable(10)
    device.sensors["0"].updateData(100)
    device.sensors["0"].updateData(100)
    device.sensors["0"].updateData(100)
    device.sensors["0"].updateData(100)
    device.sensors["0"].updateData(100)

    #Save sensor data to DB
    device.sensors["0"].saveSensorToDB()

    #Save sensor historic data
    device.sensors["0"].saveHistoricRecord()

    # Main Loop

    pass
