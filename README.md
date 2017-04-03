# android-ad
Run automated android testing scripts, reset "identity", and log network traffic for analysis

### Cheatsheet for test device

Disable IPv6 on a rooted android device

`echo 1 > /proc/sys/net/ipv6/conf/wlan0/disable_ipv6`

### Cheatsheet for mitmproxy

Run mitmdump with a script

`mitmdump [--socks] -w <mitm_log.log> -s "<script.py> -d <db_location>" -p <port> [--quiet]`
