import io
import json
import os
import subprocess
import argparse


from base_class import basic_reporter


parser = argparse.ArgumentParser()

parser.add_argument(
    "-i", "--image", help="the target container's image, including the image tag", type=str)

args = parser.parse_args()

class container_reporter(basic_reporter):

    def __init__(self, image, shell="/bin/bash", host="localhost"):
        super().__init__(shell, host)
        self.image = image

    def does_container_exist(self):
        exist_flag = False
        container_counter = 0
        result = subprocess.run([self.shell, '-c', "docker container ls"],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        buf = io.StringIO(result.stdout.decode('utf-8'))
        for line in buf.readlines()[1:]:
            res = ' '.join(line.split()).split()
            image_name = res[1]
            if image_name == self.image:
                exist_flag = True
                container_counter += 1
        return exist_flag, container_counter

    def construct_report(self):
        exist, container_numbers = self.does_container_exist()
        self.report['type'] = "statusReport"
        self.report['targetImage'] = self.image.split(':')[0]
        self.report['imageTag'] = self.image.split(':')[1]
        self.report['containerExist'] = str(exist)
        self.report['containerQuantites'] = str(container_numbers)
        self.report['time'] = self.provide_timestamp()


if __name__ == "__main__" :
    reporter = container_reporter(args.image)
    reporter.construct_report()
    payload = reporter.submit_report()
    print(json.dumps(payload))
    reporter.client.publish(
        "mota/statusReport/ContainerStatus", json.dumps(payload))
            

