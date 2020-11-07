import datetime
import subprocess

import paho.mqtt.client as mqtt


class basic_requester():

    def __init__(self, host, shell="/bin/bash"):
        self.shell = shell
        self.host = host
        self.client = mqtt.Client()
        self.request = {}
        self.publish_path = None

    def provide_timestamp(self):
        ISOTIMEFORMAT = '%Y/%m/%d %H:%M:%S'
        t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        return t

    def connect(self):
        self.client.connect(self.host, port=1883, keepalive=60)

    def submit_request(self):
        return self.request

    def construct_request(self):
        '''
        store the data in self.payload, structured as below:
        {
            type (str): the payload type,
            module (str): the module for the device to execute
            requireInfo (dict): a dict containing the args for module
            brokerHost (str): the ip of mqtt broker
            description (str): the module usage
            time (str): payload send time
        }
        '''
        pass

    def construct_info_required(self):
        pass


class container_checker(basic_requester):

    def __init__(self, image, host, shell="/bin/bash"):
        super().__init__(host, shell)
        self.image = image
        self.publish_path = "mota/request/containerStatusCheck"
        self.request['requireInfo'] = {}

    def construct_major_info(self):
        self.request['type'] = "commandRequest"
        self.request['module'] = "containerStatusCheck"
        self.request['brokerHost'] = self.host
        self.request['description'] = "request for a target container report"
        self.request['time'] = self.provide_timestamp()

    def construct_detail_info(self):
        buffer = self.request['requireInfo']
        buffer['image'] = self.image.split(':')[0]
        buffer['imageTag'] = self.image.split(':')[1]
