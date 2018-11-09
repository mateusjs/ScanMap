import socket
import threading
from concurrent.futures import ThreadPoolExecutor

class Ports:
    def TCP_connect(self, ip, ports, delay, output):
        # TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # print(delay)
        # # print('ta na funcao')
        # for port in range(1, 2**16):
        #     try:
        #         TCPsock = socket.socket()
        #         TCPsock.settimeout(delay)
        #         TCPsock.connect(('10.81.81.20', port))
        #         output[port] = 'Listening'
        #         TCPsock.close()
        #     except Exception as e:
        #         output[port] =
        s = socket.socket()
        s.settimeout(delay)
        try:
            s.connect((ip, ports))
            print('conectado na porta: ', ports)
        except:
            pass
    def scan_ports(self, host_ip, delay):
        threads = []  # To run TCP_connect concurrently
        output = ['' for _ in range(65536)]  # For printing purposes

        thread_pool = ThreadPoolExecutor(max_workers=300)
        for i in range(65536):
            thread_pool.submit(self.TCP_connect, host_ip, i, delay, output)
            t = threading.Thread(target=self.TCP_connect, args=(host_ip, i, delay, output))
            threads.append(t)

        thread_pool.shutdown(wait=True)