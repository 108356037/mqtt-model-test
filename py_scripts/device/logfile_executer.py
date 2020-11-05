import os
import json
import subprocess


path = "../logs_files/mota/commandRequest/ContainerStatusRequest/logs.txt"
with open(path,'r') as f:
    cmd = f.readlines()
    cmd = json.loads(cmd[0].strip('\n'))['command'].split(' ')
    subprocess.call(cmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    f.close()