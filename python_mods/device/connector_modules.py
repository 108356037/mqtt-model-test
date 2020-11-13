import paho.mqtt.client as mqtt

class connector_abc():

    def __init__(self, **kwargs):
        pass

    def connect(self):
        """
        this func connects to the server
        """
        raise NotImplementedError


class mqtt(connector_abc):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


        
