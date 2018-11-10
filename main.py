# coding: utf-8
import ipaddress as ip
from ping import Ping
from ports import scan_ports

list_ports = []
ip_available = []
ports = []

for end in ip.IPv4Network('192.168.15.0/30'):
    end = str(end)

    if Ping.ping(end) != -1:
        print("IP %s acessivel" % end)
        print('\nVerificando portas abertas do ip: %s' % end)

        ports = scan_ports(end, .1)
        ip_available.append(end)
        print(ports)
        list_ports.append(ports)
        print(list_ports)
        ports.clear()
    else:
        print("IP %s não funciona\n" % end)
        a = 1


dictionary = dict(zip(ip_available, list_ports))
print(dictionary)
# delay = float(input("Quanto tempo sera necessario esperar a resposta da porta para que ela seja descartada?"))

# for ips in ip_available:
#     print('\nVerificando portas abertas do ip: %s' % ips)
#     scan_ports(ips, .1)
