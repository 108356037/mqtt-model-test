import argparse
import json

import cloud_publish_modules

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m", "--module", help="the module you want the device to run", type=str, required=True)
parser.add_argument(
    "-i", "--image", help="the target container's image, including the image tag", type=str)

args = parser.parse_args()

if(args.image):
    args.image = args.image.strip(' ')
    if len(args.image.split(':')) == 1:
        raise NameError("Requires both the image and the tag!")

args.module = args.module.strip(' ')

if args.module == "containerStatusCheck":
    requester = cloud_publish_modules.container_checker(args.image)

requester.construct_request()
payload = requester.submit_request()
print(json.dumps(payload))
requester.client.publish("mota/request/containerStatusRequest",
                         json.dumps(payload))
