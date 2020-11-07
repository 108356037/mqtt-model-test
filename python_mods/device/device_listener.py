import argparse
import os
import pathlib
import json

import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t", "--topic_name", help="the topic to subscribe to", type=str,  required=True)

parser.add_argument(
    "--host", help="mqtt broker ip", type=str, default="localhost")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(args.topic_name)


def on_message(client, userdata, msg):
    print(f"received message payload from {msg.topic} \n")
    print(json.dumps(json.loads(msg.payload), indent=4, sort_keys=True))
    print("="*79)
    curpath = pathlib.Path(__file__).parent.absolute()
    filename = f"{curpath}/log_files/"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename+"logs.txt", "w")
    f.write(msg.payload.decode("utf-8")+'\n')
    f.close()


args = parser.parse_args()
args.topic_name = args.topic_name.strip(' ')
args.host = args.host.strip(' ')
print(f"subscribe to {args.topic_name} on {args.host}:1883")

client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message

client.connect(args.host, port=1883, keepalive=60)

client.loop_forever()
