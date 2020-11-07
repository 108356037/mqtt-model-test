import datetime
import subprocess
from pathlib import Path

import paho.mqtt.client as mqtt
from collections import defaultdict


class basic_requester():

    def __init__(self, host, shell="/bin/bash"):
        self.shell = shell
        self.host = host
        self.client = mqtt.Client()
        self.request = defaultdict()
        self.command_pool_path = str(
            Path().absolute().parent)+'/device/command_pool/'

    def provide_timestamp(self):
        ISOTIMEFORMAT = '%Y/%m/%d %H:%M:%S'
        t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        return t

    def connect(self):
        self.client.connect(self.host, port=1883, keepalive=60)

    def submit_request(self):
        return self.request

    def construct_request(self):
        # store the data in self.payload based on each case
        pass


class container_checker(basic_requester):

    def __init__(self, image, host, shell="/bin/bash"):
        super().__init__(host, shell)
        self.image = image
        self.module_name = "container_status_check.py"
        self.cmd = None

    def construct_request(self):
        self.request['type'] = "commandRequest"
        self.request['command'] = f"/usr/bin/python3 {self.command_pool_path+self.module_name} -i {self.image} --host {self.host}"
        self.request['description'] = "request for a target container report"
        self.request['time'] = self.provide_timestamp()
