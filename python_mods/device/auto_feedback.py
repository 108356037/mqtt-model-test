import json
import logging
import inspect
import os.path

import reporter_modules as rm

module_dict = {'containerStatusCheck': rm.container_reporter}

filename = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(filename))


with open(path+"/log_files/logs.txt", "r") as f:
    payload = f.readlines()
    payload = json.loads(payload[-1].strip('\n'))
    reporter = module_dict[payload["module"]](payload)
    reporter.construct_detail_report()
    reporter.construct_major_report()
    reporter.connect()
    report = reporter.submit_report()
    # print(json.dumps(report, indent=4))
    print('='*79)
    reporter.client.publish(reporter.publish_path, json.dumps(report))
