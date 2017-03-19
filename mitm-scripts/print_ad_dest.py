import time
import argparse
import urllib
import re
from BeautifulSoup import BeautifulSoup

count = 0


class print_ad_dest:

    def __init__(self):
        # primarily used for DataXu urls (https://i.w55c.net/*)
        self.regex1 = re.compile('rurl%3Dhttp.*?\\\\x26')
        self.regex2 = re.compile('adurl=http.*?\"')
        self.regex3 = re.compile("adurl\\\\x3dhttp.*?(?:\'|\"|\\\\x22)")

    def response(self, flow):
        global count
        try:
            if ("https://pubads.g.doubleclick.net/gampad/ads" in flow.request.pretty_url or
                    "https://googleads.g.doubleclick.net/mads/gma" in flow.request.pretty_url or
                    "https://ad.doubleclick.net/ddm/adj" in flow.request.pretty_url) \
                    and len(flow.response.content) > 0:
                print(
                    flow.request.method + " " + urllib.unquote(flow.request.pretty_url) + "\n")
                raw_html = flow.response.content
                soup = BeautifulSoup(
                    raw_html.replace("\\x3d", "=").replace("\\x22", '"'))
                m1 = self.regex1.search(raw_html)
                m2 = self.regex2.search(raw_html)
                m3 = self.regex3.search(raw_html)
                if m1:
                    print(urllib.unquote(m1.group(0)[7:-4]) + '\n')
                elif m2:
                    print(urllib.unquote(m2.group(0)[6:-1]) + '\n')
                elif m3:
                    if m3.group(0)[-1] == "\'" or m3.group(0)[-1] == '\"':
                        print(urllib.unquote(m3.group(0)[9:-1]) + '\n')
                    else:
                        print(urllib.unquote(m3.group(0)[9:-4]) + '\n')
                else:
                    if "new HybridAds(" in raw_html:
                        print("Cannot support Hybrid Ads for now\n")
                    print("NO MATCH!!!!\n")
                    with open("/tmp/" + str(count) + ".html.txt", "w") as f:
                        f.write(
                            "<!-- Original url: " + flow.request.pretty_url + " -->\n")
                        f.write(soup.prettify())
                    count += 1
        except KeyError:
            pass


def start():
    return print_ad_dest()
