import time
import argparse
import urllib
import re


class print_url:

    def response(self, flow):
        regex = re.compile('\w*=(.{8}-.{4}-.{4}-.{4}-.{12}|[0-9a-fA-F]{32})')

        try:
            print(
                regex.search(urllib.unquote(flow.request.pretty_url) + "\n").group(0))
        except Exception:
            pass


def start():
    return print_url()
