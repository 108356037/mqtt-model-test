import datetime
import json
import random
import time

import paho.mqtt.client as mqtt

ISOTIMEFORMAT = '%m/%d %H:%M:%S'

client = mqtt.Client()

client.username_pw_set("try", "xxx")

client.connect("localhost", port=1883, keepalive=60)

while True:
    t0 = random.randint(0, 30)
    t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
    payload = {'Temperature': t0, 'Time': t}
    print(json.dumps(payload))
    client.publish("Try/MQTT", json.dumps(payload))
    time.sleep(2.5)
