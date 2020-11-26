import paho.mqtt.client as mqtt

class connector_abc():

    def __init__(self, **kwargs):
        """
        pass in a dict (load in yaml)
        """
        raise NotImplementedError

    def connect(self):
        """
        this func connects to the server
        """
        raise NotImplementedError


class mqtt_connack(connector_abc):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print(f"received message payload from {msg.topic} \n")
        print(json.dumps(json.loads(msg.payload), indent=4, sort_keys=True))
        print("="*79)
        #return msg.payload.decode("utf-8")

    def connect(self):
        self.client.connect(self.host, self.port, self.keepalive)
        print(f"subscribe to {self.topic} on {self.host}:{self.port}")
        self.client.loop_forever()


        
