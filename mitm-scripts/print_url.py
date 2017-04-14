import time
import argparse
import urllib


class print_url:

    def response(self, flow):
        print(
            flow.request.method + " " + urllib.parse.unquote(flow.request.pretty_url) + "\n")


def start():
    return print_url()
