### need to be changed for oring paas payload protocal
'''
components in a basic publisher script:
    1. connector: 
    2. request-constructor
    3. a yaml config the connect params 
'''
import argparse
import json
import yaml

import request_modules as rm
import connector as cn

module_dict = {'containerStatusCheck': rm.container_checker}
connector_dict = {'mqtt': cn.}

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m", "--module", help="the module you want the device to run", type=str, required=True)
parser.add_argument(
    "-i", "--image", help="the target container's image, including the image tag", type=str)
# parser.add_argument(
#     "--host", help="mqtt broker ip", type=str, default="localhost")
parser.add_argument(
    "--protocol", help="the communication type", type=str, required=True)

args = parser.parse_args()

if(args.image):
    args.image = args.image.strip(' ')
    if len(args.image.split(':')) == 1:
        raise NameError("Requires both the image and the tag!")


requester = module_dict[args.module](image=args.image, host=args.host)
requester.construct_detail_info()
requester.construct_major_info()
requester.connect()
payload = requester.submit_request()
print(json.dumps(payload, indent=4))
requester.client.publish(requester.publish_path, json.dumps(payload))
