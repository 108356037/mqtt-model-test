import argparse
import datetime
import json

import paho.mqtt.client as mqtt
from publish_modules import *

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", help="the target container's image, including the image tag", type=str,  required=True,)
parser.add_argument("-m", "--module", help="the module you want the device to run", type=str, required=True)

args = parser.parse_args()
args.image = args.image.strip(' ')
if len(args.image.split(':')) == 1:
    raise NameError("Requires both the image and the tag!")

cmd_line = f"/usr/bin/python3 {args.module} -i {args.image}"

payload = {"type": "commandRequest",
           "command": cmd_line,
           "description": "request for a target container report",
           "time": t}
print(json.dumps(payload))
client.publish("mota/commandRequest/ContainerStatusRequest",
               json.dumps(payload))
