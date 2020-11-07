import argparse
import datetime
import io
import json
import os
import subprocess
from pathlib import Path

import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser()

# parser.add_argument(
#     "-i", "--image", help="the target container's image, including the image tag", type=str)
# parser.add_argument(
#     "--host", help="mqtt broker ip", type=str)

args = parser.parse_args()


'''
reporter機制：

1. 基於module種類去建構reporter

2. construct major/detail report 兩個func 把該回報的值處理好包成dict

3. 把 report submit 給 mqtt broker

'''


class basic_reporter():

    def __init__(self, request_payload, shell="/bin/bash"):
        self.shell = shell
        self.client = mqtt.Client()
        self.report = {}
        self.module_pool = str(Path().absolute())
        self.request_payload = request_payload
        self.publish_path = None

    def provide_timestamp(self):
        ISOTIMEFORMAT = '%Y/%m/%d %H:%M:%S'
        t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        return t

    def connect(self):
        self.client.connect(
            self.request_payload['brokerHost'], port=1883, keepalive=60)

    def submit_report(self):
        return self.report

    def construct_major_report(self):
        pass

    def construct_detail_report(self):
        pass


class container_reporter(basic_reporter):

    def __init__(self, request_payload, shell="/bin/bash"):
        super().__init__(request_payload, shell)
        self.report['reportContent'] = {}
        self.publish_path = "mota/report/containerStatusCheck"

    def does_container_exist(self):
        exist_flag = False
        container_counter = 0
        result = subprocess.run([self.shell, '-c', "docker container ls"],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        buf = io.StringIO(result.stdout.decode('utf-8'))
        for line in buf.readlines()[1:]:
            try:
                res = ' '.join(line.split()).split()
                img_name, img_tag = res[1].split(':')[0], res[1].split(':')[1]
                target_img = self.request_payload['requireInfo']['image']
                target_tag = self.request_payload['requireInfo']['imageTag']
                if (img_name, img_tag) == (target_img, target_tag):
                    exist_flag = True
                    container_counter += 1
            except:
                print(f"wrong, container image: {res[1]}")
        return exist_flag, container_counter

    def construct_major_report(self):
        self.report['type'] = "statusReport"
        self.report['brokerHost'] = self.request_payload['brokerHost']
        self.report['module'] = self.request_payload['module']
        self.report['time'] = self.provide_timestamp()

    def construct_detail_report(self):
        exist, container_numbers = self.does_container_exist()
        detail_report = self.report['reportContent']
        detail_report['image'] = self.request_payload['requireInfo']['image']
        detail_report['imageTag'] = self.request_payload['requireInfo']['imageTag']
        detail_report['containerExist'] = str(exist)
        detail_report['containerQuantites'] = str(container_numbers)
