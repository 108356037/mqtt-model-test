import argparse
import connector

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t", "--topic", help="the topic to subscribe to", type=str, default="mota/#")
parser.add_argument(
    "--host", help="mqtt broker ip", type=str, default="localhost")
parser.add_argument(
    "-p", "--port", help="the port to connect mqtt broker", type=int, default=1883)
parser.add_argument(
    "--client_id", help="the id used to connect mqtt broker", type=str, default=None)
parser.add_argument(
    "-w", "--write", help="the output will be written to file if on", action="store_true")

args = parser.parse_args()

subscriber = connector.subscriber(
    args.host, args.port, args.client_id, args.topic)
if args.write:
    subscriber.turn_on_write()

subscriber.connect()
