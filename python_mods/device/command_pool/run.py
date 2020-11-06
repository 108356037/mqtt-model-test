import json
import subprocess

with open("logs.txt","r") as f:
    cmd = f.readlines()
    cmd = json.loads(cmd[0].strip('\n'))['command'].split(' ')
    subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    f.close()

