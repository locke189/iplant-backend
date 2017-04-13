#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from Shared import Logger


class Broker:

    rc_code = {
        0: "Connection Successful",
        1: "Connection refused - incorrect protocol version",
        2: "Connection refused - invalid client identifier",
        3: "Connection refused - server unavailable",
        4: "Connection refused - bad username or password",
        5: "Connection refused - not authorised",
    }



    def __init__(self, topic="topic/channel", logs = True, logName='Broker'):
        self.mqttc = mqtt.Client()
        self.console = Logger.Logger(logName="Broker("+logName+")", enabled=logs, printConsole=True)
        self.console.log("Initialization...")
        self.callback = None
        self.rc = None
        self.topic = topic
        self.qos = 0
        self.mqttc = mqtt.Client()
        self.mqttc.on_connect = self._on_connect()
        self.mqttc.on_disconnect = self._on_disconnect
        self.mqttc.on_message = self._on_message
        self.mqttc.on_subscribe = self._on_subscribe
        self.mqttc.on_unsubscribe = self._on_unsubscribe
        self.mqttc.on_publish = self._on_publish
        self.mqttc.connect(host='localhost', port=1883)


    def _on_connect(self):
        def onConnect(anymqttc, userdata, rc):
            self.rc = rc
            self.console.log("Connecting... %s" , str(self.rc_code[self.rc]) )
            self.mqttc.subscribe(topic=self.topic, qos=self.qos)
        return onConnect

    def _on_disconnect(self,mqttc, userdata, rc):
        self.rc = rc
        if self.rc == 0:
            self.console.log("Disconnected.")
        else:
            self.console.log("Unexpected disconnection.")

    def _on_message(self, mqttc, userdata, msg):
        self.console.log("Message Received. topic: ' %s ', qos: ' %s ', message: ' %s '", (msg.topic, msg.qos, msg.payload))
        if self.callback:
            self.callback(msg.topic, msg.payload)

    def _on_subscribe(self, mqttc, userdata, mid, granted_qos):
        self.console.log("Subscribed to ' %s '", self.topic)

    def _on_unsubscribe(self, mqttc, userdata, mid, granted_qos):
        self.console.log("Unsubscribed to ' %s '", self.topic)

    def _on_publish(self, mqttc, userdata, mid):
        self.console.log("Message Published")
        #self.mqttc.disconnect()

    def setCallback( self, callback):
        self.callback = callback

    def startTimeout(timeout = 5.0):
        self.mqttc.loop(timeout)

    def start(self):
        self.console.log("Starting loop")
        self.mqttc.loop_start()

    def stop(self):
        self.console.log("Stopping loop")
        self.mqttc.loop_stop()
        self.mqttc.disconnect()

    def publishMessage(self,topic,payload):
        self.mqttc.publish(topic=topic, payload=payload, qos=self.qos)


if __name__ == '__main__':
    mqttc = mqtt.Client()
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc.on_message = on_message
    mqttc.on_subscribe = on_subscribe
    mqttc.on_unsubscribe = on_unsubscribe
    mqttc.connect(host='localhost', port=1883)
    mqttc.loop_forever()