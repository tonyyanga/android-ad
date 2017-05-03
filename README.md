# android-ad

Run automated android testing scripts, reset "identity", and log network traffic for analysis

## Prerequisites

mitmproxy, appium on the test server

Any proxy app on the test android device that allows global proxy. 

## Steps to run before experiment

#### (Optional) Preparations for test device

Disable IPv6 on a rooted android device

`echo 1 > /proc/sys/net/ipv6/conf/wlan0/disable_ipv6`

#### Setup for mitmproxy

Run mitmdump, with a script (optional)

`mitmdump [--socks] -w <mitm_log.log> -s "<script.py> -d <db_location>" -p <port> [--quiet]`

#### Run appium

By default, just run:

`appium`

#### Configuration

Configure the android device to use the proxy server created by mitmdump.

## Write experiment scripts

See `appium-scripts/` for examples. APIs are in `appium_exec/`.

## Parse mitmproxy output

See `mitm-scripts/` for some inline scripts to run with `mitmdump -r` option. Output format is documented in every script.

