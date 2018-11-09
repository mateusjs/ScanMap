# coding: utf-8
import ipaddress as ip
from ping import Ping
from ports import Ports

port = Ports()

ip_available = ['10.81.81.20']
# for end in ip.IPv4Network('10.81.80.0/29'):
#     end = str(end)
#
#     if Ping.ping(end) != -1:
#         print("IP %s funciona" % end)
#         ip_available.append(end)
#     else:
#         print("IP %s não funciona" % end)
#         a = 1
delay = float(input("Quanto tempo sera necessario esperar a resposta da porta para que ela seja descartada?"))

for ips in ip_available:
    print(ips)
    port.scan_ports(ips, delay)
