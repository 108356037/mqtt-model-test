import argparse
import os
import pathlib

import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t", "--topic_name", help="the topic to subscribe to", type=str,  required=True)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(args.topic_name)


def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode("utf-8"))
    curpath = pathlib.Path(__file__).parent.absolute()
    filename = f"{curpath}/log_files/{msg.topic}/"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    f = open(filename+"logs.txt", "w")
    f.write(msg.payload.decode("utf-8")+'\n')
    f.close()


args = parser.parse_args()
args.topic_name = args.topic_name.strip(' ')
print(args.topic_name)

client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message

client.connect("localhost", port=1883, keepalive=60)

client.loop_forever()
