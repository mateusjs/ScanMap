import ipaddress as ip
import networkx as nx
import matplotlib.pyplot as plt
import time
import pandas as pd
import socket
from pprint import pprint
from ping import Ping
from ports import scan_ports
from latency import IcmpRequest
from tkinter import *

latency = IcmpRequest()
list_ports = []
ip_available = []
latencys = []
ports = []
ip_cache = {}
ip_dict = {}
grafo = {}
addres = 0
mascara = 0
delay = 0


def scanMap():
    global addres
    global mascara
    global delay
    addres = e1.get()
    mascara = e2.get()
    delay = float(e3.get())


def graph(addres, ip_cache):
    global file
    data_frame = pd.DataFrame({'from': [addres] * len(ip_cache.keys()), 'to': [*ip_cache]})
    G = nx.from_pandas_edgelist(data_frame, 'from', 'to')
    nx.draw(G, with_labels=True)
    plt.show()

    with open("reachable.txt", "w+") as file:
        pprint(ip_cache, stream=file)


master = Tk()
master.geometry("300x100")
master.title("Trabalho de Redes")
Label(master, text="Endereço da Sub Rede").grid(row=0)
Label(master, text="Máscara").grid(row=1)
Label(master, text="Delay").grid(row=2)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

Button(master, text='Start ScanMap', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='OK', command=scanMap).grid(row=3, column=1, sticky=W, pady=4)

mainloop()


if mascara:
    start_time = time.time()
    for index, end in enumerate(ip.IPv4Network(addres + '/' + mascara)):
        end = str(end)
        if addres == end:
            continue
        if index == 0 or index == 2 ** (32 - int(mascara)) - 1:
            continue
        if Ping.ping(end) != -1:
            ms = latency.verbose_ping(end, delay, 1)
            ms = str(ms) + ' ms'
            print("\nIP %s acessivel    latencia = %s" % (end, ms))
            ports.clear()
            ports = scan_ports(end, .1)
            ip_cache[end] = {'latency': ms, 'ports': ports[:]}
            with open("sub_network_reachable.txt", "a+") as file:
                pprint(ip_dict, stream=file)
        else:
            print("IP %s não acessivel" % end)
            with open("unreachable.txt", "a+") as file:
                file.write("IP: %s is unreachable\n" % end)
    print("--- %s seconds ---" % (time.time() - start_time))
    graph(socket.gethostbyname(socket.gethostname()), ip_cache)

else:
    ip_teste = str(addres)
    ip_address = socket.gethostbyname(ip_teste)
    # ip_address = "".join(aux[2])

    if Ping.ping(ip_address) != -1:
        print(ip_address, ' acessível')
        ms = latency.verbose_ping(ip_address, delay, 1)
        ms = str(ms) + ' ms'
        ports = scan_ports(ip_address, 0.1)
        ip_dict[ip_address] = {'latency': ms, 'ports': ports}
        with open("direct_reachable.txt", "a+") as file:
            pprint(ip_dict, stream=file)
    else:
        print("Ip %s não acessivel" % ip_address)
