# need to be changed for oring paas payload protocal
'''
components in a basic publisher script:
    1. connector
    2. payload-constructor
    3. a yaml config the connect params
'''
import argparse
import json
import yaml

import payload_construct_mods as pcmod
import connector_mods as cnmod

payload_construct_mods = {'containerStatusCheck': pcmod.container_checker}
connector_mods = {'mqtt': cnmod.mqtt_connack}

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m", "--module", help="the module you want the device to run", type=str, required=True)
parser.add_argument(
    "-i", "--image", help="the target container's image, including the image tag", type=str)
parser.add_argument(
    "--protocol", help="the communication type", type=str, required=True)

args = parser.parse_args()

if(args.image):
    args.image = args.image.strip(' ')
    if len(args.image.split(':')) == 1:
        raise NameError("Requires both the image and the tag!")


f = open('cloud_publish.yaml')
data = yaml.load(f, Loader=yaml.FullLoader)

constructor = payload_construct_mods[args.module](**data['payload_construct_mods']['container_status_check'])
connector = connector_mods[args.protocol](**data['connect_mods']['mqtt']['oringpass'])

constructor.construct_payload()
constructor.stringfy_value()

connector.connect()
connector.payload_submit(json.dumps(constructor.payload))
