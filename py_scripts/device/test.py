import publish_modules
import json

reporter = publish_modules.container_reporter("nginx:latest")
reporter.construct_report()
payload = reporter.submit_report()
print(json.dumps(payload))
reporter.client.publish(
    "mota/statusReport/ContainerStatus", json.dumps(payload))
