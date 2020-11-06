import datetime
import io
import json
import os
import subprocess
import time

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


class container_reporter(basic_reporter):

    def __init__(self, image, shell="/bin/bash", host="localhost"):
        super().__init__(shell, host)
        self.image = image

    def does_container_exist(self):
        exist_flag = False
        container_counter = 0
        result = subprocess.run([self.shell, '-c', "docker container ls"],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        buf = io.StringIO(result.stdout.decode('utf-8'))
        for line in buf.readlines()[1:]:
            res = ' '.join(line.split()).split()
            image_name = res[1]
            if image_name == self.image:
                exist_flag = True
                container_counter += 1
        return exist_flag, container_counter

    def construct_report(self):
        exist, container_numbers = self.does_container_exist()
        self.report['type'] = "statusReport"
        self.report['targetImage'] = self.image.split(':')[0]
        self.report['imageTag'] = self.image.split(':')[1]
        self.report['containerExist'] = str(exist)
        self.report['containerQuantites'] = str(container_numbers)
        self.report['time'] = self.provide_timestamp()


# args = parser.parse_args()

# args.image_name = args.image_name.strip(' ')

# if len(args.image_name.split(':')) == 1:
#     raise NameError("Requires both the image and the tag!")

# reporter = container_reporter(args.image_name,)
# exist, container_numbers = reporter.does_container_exist()

# payload = {'type': "statusReport",
#            'targetImage': args.image_name.split(':')[0],
#            'imageTag': args.image_name.split(':')[1],
#            'containerExist': str(exist),
#            'containerQuantites': str(container_numbers),
#            'time': reporter.provide_timestamp()}

# print(json.dumps(payload))
# reporter.client.publish("mota/statusReport/ContainerStatus", json.dumps(payload))
