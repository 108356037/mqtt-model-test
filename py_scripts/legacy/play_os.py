import os
import io
import logging
import argparse
import subprocess

logging.basicConfig(level=logging.DEBUG)


def does_container_exist(target):
    exist_flag = False
    result = subprocess.run(['/bin/bash', '-c', "docker container ls"],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    buf = io.StringIO(result.stdout.decode('utf-8'))
    for line in buf.readlines()[1:]:
        res = ' '.join(line.split()).split()
        image_name = res[1]
        if image_name == target:
            exist_flag = True
            break
    return exist_flag


print(does_container_exist('jupyter/datascience-'))
