import os
import json
import subprocess
import pathlib
import logging

path = pathlib.Path(__file__).parent.absolute().parent
path = str(path)+'/log_files/mota/commandRequest/ContainerStatusRequest/logs.txt'

with open(path,'r') as f:
    cmd = f.readlines()
    cmd = json.loads(cmd[0].strip('\n'))['command'].split(' ')
    logging.critical(subprocess.call(cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT))
    f.close()