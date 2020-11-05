import argparse
import datetime
import json

import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", "--image_name", help="the target container's image, including the image tag", type=str,  required=True)

ISOTIMEFORMAT = '%Y/%m/%d %H:%M:%S'

client = mqtt.Client()

client.connect("localhost", port=1883, keepalive=60)

t = datetime.datetime.now().strftime(ISOTIMEFORMAT)

args = parser.parse_args()
args.image_name = args.image_name.strip(' ')
if len(args.image_name.split(':')) == 1:
    raise NameError("Requires both the image and the tag!")

cmd_line = f"/usr/bin/python3 container_spitter.py -i {args.image_name}"

payload = {"type": "commandRequest",
           "command": cmd_line,
           "description": "request for a target container reqport",
           "time": t}
print(json.dumps(payload))
client.publish("mota/commandRequest/ContainerStatusRequest",
               json.dumps(payload))
