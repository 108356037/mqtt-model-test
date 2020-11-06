import datetime
import subprocess


import paho.mqtt.client as mqtt
from collections import defaultdict


class basic_reporter():

    def __init__(self, shell="/bin/bash", host="localhost"):
        self.shell = shell
        self.client = mqtt.Client()
        self.client.connect(host, port=1883, keepalive=60)
        self.report = defaultdict()

    def provide_timestamp(self):
        ISOTIMEFORMAT = '%Y/%m/%d %H:%M:%S'
        t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        return t

    def submit_report(self):
        return self.report

    def construct_report(self):
        # store the data in self.report based on each case
        pass
