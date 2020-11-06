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
