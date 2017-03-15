import time
import argparse


class print_host:

    def __init__(self, dir):
        self.dir = dir

    def response(self, flow):
        filename = self.dir + str(int(time.time()))
        with open(filename, "a") as f:
            f.write(flow.request.method + " " + flow.request.pretty_url + "\n")


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-L", "--log-dir", required=True, help="A directory in which logs can be stored")
    args = parser.parse_args()

    log_dir = args.log_dir

    return print_host(log_dir)
