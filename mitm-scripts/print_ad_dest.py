import time
import argparse
import urllib
import re
from BeautifulSoup import BeautifulSoup

count = 0


class print_ad_dest:

    def response(self, flow):
        global count
        try:
            if (flow.request.headers['Host'] == "pubads.g.doubleclick.net" or
                    "https://googleads.g.doubleclick.net/mads/gma" in flow.request.pretty_url) and len(flow.response.content) > 0:
                print(
                    flow.request.method + " " + urllib.unquote(flow.request.pretty_url) + "\n")
                raw_html = flow.response.content
                soup = BeautifulSoup(
                    raw_html.replace("\\x3d", "=").replace("\\x22", '"'))
                m1 = re.search('buildAdSlot\(.*?\)', raw_html)
                m2 = re.search('adurl=http.*?\"', raw_html)
                m4 = re.search("adurl\\\\x3dhttp.*?\\\\x22", raw_html)
                m3 = re.search("adurl\\\\x3dhttp.*?\'", raw_html)
                if m1:
                    print(m1.group(0) + '\n')
                elif m2:
                    print(urllib.unquote(m2.group(0)[6:-1]) + '\n')
                elif m4:
                    print(urllib.unquote(m4.group(0)[9:-4]) + '\n')
                elif m3:
                    print(urllib.unquote(m3.group(0)[9:-1]) + '\n')
                else:
                    if "new HybridAds(" in raw_html:
                        print("Cannot support Hybrid Ads for now\n")
                    print("NO MATCH!!!!\n")
                    with open("/tmp/" + str(count) + ".html.txt", "w") as f:
                        f.write(
                            "<!-- Original url: " + flow.request.pretty_url + "-->\n")
                        # f.write(soup.prettify())
                        f.write(flow.response.content)
                    count += 1
        except KeyError:
            pass


def start():
    return print_ad_dest()
