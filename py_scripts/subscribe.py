import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("mota/getContainerStatus")


def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode("utf-8"))


client = mqtt.Client()

client.on_connect = on_connect

client.on_message = on_message

client.username_pw_set("try", "xxx")

client.connect("localhost", port=1883, keepalive=60)

client.loop_forever()
