import os
import pathlib
import json

import paho.mqtt.client as mqtt


class basic_connect_config():
    def __init__(self, host, port, client_id):
        self.host = host
        self.port = port
        self.client = mqtt.Client(client_id=client_id)
        self.type = None

    def on_connect(self):
        pass

    def on_message(self):
        pass


class subscriber(basic_connect_config):

    def __init__(self, host, port, client_id, topic):
        super().__init__(host, port, client_id)
        self.topic = topic
        self.type = "subscribe"
        self.write = False
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print(f"received message payload from {msg.topic} \n")
        print(json.dumps(json.loads(msg.payload), indent=4, sort_keys=True))
        print("="*79)
        if self.write:
            curpath = pathlib.Path(__file__).parent.absolute()
            filename = f"{curpath}/log_files/"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            f = open(filename+"logs.txt", "w")
            f.write(msg.payload.decode("utf-8")+'\n')
            f.close()

    def connect(self):
        self.client.connect(self.host, self.port, keepalive=60)
        print(f"subscribe to {self.topic} on {self.host}:{self.port}")
        self.client.loop_forever()

    def turn_on_write(self):
        self.write = True
