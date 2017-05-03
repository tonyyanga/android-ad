import time
import argparse
import urllib
import re

""" Find any string following the format of Android Advertising ID

    See https://support.google.com/googleplay/android-developer/answer/6048248?hl=en
    for additional information
"""


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
