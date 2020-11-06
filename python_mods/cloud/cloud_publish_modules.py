import datetime
import subprocess
from pathlib import Path

import paho.mqtt.client as mqtt
from collections import defaultdict


class basic_requester():

    def __init__(self, shell="/bin/bash", host="localhost"):
        self.shell = shell
        self.client = mqtt.Client()
        self.client.connect(host, port=1883, keepalive=60)
        self.request = defaultdict()
        self.command_pool_path = str(
            Path().absolute().parent)+'/device/command_pool/'

    def provide_timestamp(self):
        ISOTIMEFORMAT = '%Y/%m/%d %H:%M:%S'
        t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        return t

    def submit_request(self):
        return self.request

    def construct_request(self):
        # store the data in self.payload based on each case
        pass


class container_checker(basic_requester):

    def __init__(self, image, shell="/bin/bash", host="localhost"):
        super().__init__(shell, host)
        self.image = image
        self.module_name = "container_status_check.py"
        self.cmd = None

    def construct_request(self):
        self.request['type'] = "commandRequest"
        self.request['command'] = f"/usr/bin/python3 {self.command_pool_path+self.module_name} -i {self.image}"
        self.request['description'] = "request for a target container report"
        self.request['time'] = self.provide_timestamp()
