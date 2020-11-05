import argparse
import datetime
import io
import json
import os
import re
import subprocess
import time

import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser()
parser.add_argument(
    "-i", "--image_name", help="the target container's image, including the image tag", type=str,  required=True)


def does_container_exist(target):
    exist_flag = False
    container_counter = 0
    result = subprocess.run(['/bin/bash', '-c', "docker container ls"],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    buf = io.StringIO(result.stdout.decode('utf-8'))
    for line in buf.readlines()[1:]:
        res = ' '.join(line.split()).split()
        image_name = res[1]
        if image_name == target:
            exist_flag = True
            container_counter += 1
    return exist_flag, container_counter


args = parser.parse_args()

ISOTIMEFORMAT = '%Y/%m/%d %H:%M:%S'

client = mqtt.Client()

client.connect("localhost", port=1883, keepalive=60)

args.image_name = args.image_name.strip(' ')

if len(args.image_name.split(':')) == 1:
    raise NameError("Requires both the image and the tag!")

# while True:
#     exist, container_numbers = does_container_exist(args.image_name)
#     t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
#     payload = { 'type': "statusReport",
#                 'targetImage': args.image_name.split(':')[0],
#                'imageTag': args.image_name.split(':')[1],
#                'containerExist': str(exist),
#                'containerQuantites': str(container_numbers),
#                'Time': t}
#     print(json.dumps(payload))
#     client.publish("mota/statusReport/ContainerStatus", json.dumps(payload))
#     time.sleep(3.50)


exist, container_numbers = does_container_exist(args.image_name)
t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
payload = {'type': "statusReport",
           'targetImage': args.image_name.split(':')[0],
           'imageTag': args.image_name.split(':')[1],
           'containerExist': str(exist),
           'containerQuantites': str(container_numbers),
           'time': t}
print(json.dumps(payload))
client.publish("mota/statusReport/ContainerStatus", json.dumps(payload))
