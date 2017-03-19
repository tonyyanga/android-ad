import time
import argparse


class log_url:

    def __init__(self, dir):
        self.dir = dir

    def response(self, flow):
        filename = self.dir + str(int(time.time()))
        with open(filename, "a") as f:
            f.write(flow.request.method + " " +
                    urllib.unquote(flow.request.pretty_url) + "\n")


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-L", "--log-dir", required=True, help="A directory in which logs can be stored")
    args = parser.parse_args()

    log_dir = args.log_dir

    return log_url(log_dir)
