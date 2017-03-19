import time
import argparse
import urllib


class print_url:

    def response(self, flow):
        try:
            if flow.request.headers['Host'] == "pubads.g.doubleclick.net" and '/favicon.ico' not in flow.request.url:
                print(
                    flow.request.method + " " + urllib.unquote(flow.request.pretty_url) + "\n")
        except Exception:
            pass


def start():
    return print_url()
