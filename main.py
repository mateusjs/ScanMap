# coding: utf-8
import ipaddress as ip
from ping import Ping

ip_available = []
for end in ip.IPv4Network('10.81.80.0/23'):
    end = str(end)

    if Ping.ping(end) != -1:
        print("IP %s funciona" % end)
        ip_available.append(end)
    else:
        print("IP %s não funciona" % end)
        a = 1
print(ip_available)
