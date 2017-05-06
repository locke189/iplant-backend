import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'iPlantBackend')))

from Broker import Broker

import unittest
from random import randint
import time


class TestBroker(unittest.TestCase):


    #Database startup
    broker1 = Broker.Broker(topic="topic/channel", logs = False, logName='Broker1')
    broker2 = Broker.Broker(topic="topic/channel", logs = False, logName='Broker2')
    broker3 = Broker.Broker(topic="topic/channel", logs = False, logName='Broker3')
    broker1.subscribe(topic="topic/channel")
    broker2.subscribe(topic="topic/channel")
    payload = randint(0,9)
    payload2 = randint(0,9)
    payload3 = randint(0,9)
    received_payload = ' '

    def iAmACallbackFunction(self, topic, payload):
        self.received_topic = topic
        self.received_payload = payload
        self.broker1.stop()

    def iAmACallbackFunction2(self, topic, payload):
        self.received_topic = topic
        self.received_payload2 = payload
        self.broker1.stop()

    def iAmACallbackFunction3(self, topic, payload):
        self.received_topic = topic
        self.received_payload3 = payload
        self.broker1.stop()

    def test_it_should_receive_message(self):
        self.broker1.setCallback(self.iAmACallbackFunction)
        self.broker1.start()
        self.broker2.start()
        self.broker2.publishMessage("topic/channel",self.payload)
        self.broker2.stop()
        time.sleep(1)
        self.broker1.stop()
        self.assertEqual(str(self.payload), self.received_payload)


    def test_it_should_subscribe_to_multiple_topics(self):
        self.broker3.subscribeTopicWithCallback("topic/channel2",self.iAmACallbackFunction2)
        self.broker3.subscribeTopicWithCallback("topic/channel3",self.iAmACallbackFunction3)
        self.broker3.setCallbacks()
        self.broker3.start()
        self.broker3.publishMessage("topic/channel2",self.payload2)
        time.sleep(1)
        self.broker3.publishMessage("topic/channel3",self.payload3)
        time.sleep(1)
        self.broker3.stop()
        self.assertEqual(str(self.payload2), self.received_payload2)
        self.assertEqual(str(self.payload3), self.received_payload3)
        pass


if __name__ == '__main__':
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabase)
    #unittest.TextTestRunner(verbosity=2).run(suite)

    def iAmACallbackFunction(topic, value):
        print('Inside callback')
        text = "I am a callback function and the passed value is " + str(topic) + " " + str(value)
        print(text)

    #Database startup
    broker1 = Broker.Broker(topic="topic/channel", logs = True, logName='Broker1')
    broker2 = Broker.Broker(topic="topic/channel", logs = True, logName='Broker2')
    broker1.setCallback(iAmACallbackFunction)
    broker1.start()
    broker2.start()
    broker2.publishMessage("topic/channel","Hello from broker2")
    broker2.stop()


    while True:
        pass
