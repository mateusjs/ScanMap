import ipaddress as ip
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
grafo = {}
addres = 0
mascara = 0
delay = 0


def scanMap():
    addres = e1.get()
    mascara = e2.get()
    delay = float(e3.get())
    for end in ip.IPv4Network(addres + '/' + mascara):
        end = str(end)

        if Ping.ping(end) != -1:
            ms = latency.verbose_ping(end, delay, 1)
            print("\nIP %s acessivel    latencia = %s" % (end, ms))
            print('\nVerificando portas abertas do ip: %s' % end)

            ports = scan_ports(end, .1)
            ip_available.append(end)
            list_ports.append(ports)
            latencys.append(ms)
            ip_cache[end] = {'latency': ms, 'ports': ports}

        else:
            print("IP %s não funciona\n" % end)
    print(ip_cache)
    return
    # grafo[addres] = {ip_cache}


master = Tk()
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

Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=W, pady=4)
Button(master, text='OK', command=scanMap).grid(row=3, column=1, sticky=W, pady=4)

mainloop()
