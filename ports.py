import socket
import threading
from concurrent.futures import ThreadPoolExecutor

open_ports = []


def TCP_connect(ip, ports, delay):
    s = socket.socket()
    s.settimeout(delay)
    try:
        s.connect((ip, ports))
        open_ports.append(ports)
        s.close()
    except:
        pass


def scan_ports(host_ip, delay):
    threads = []

    thread_pool = ThreadPoolExecutor(max_workers=100)
    for i in range(65536):
        thread_pool.submit(TCP_connect, host_ip, i, delay)
        t = threading.Thread(target=TCP_connect, args=(host_ip, i, delay))
        threads.append(t)
    thread_pool.shutdown(wait=True)
    return open_ports
