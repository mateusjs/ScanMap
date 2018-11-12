import os
import select
import socket
import struct
import sys
import time


class IcmpRequest:

    def __init__(self):
        self.default_timer = 0
        if sys.platform == "win32":
            self.default_timer = time.clock
        else:
            self.default_timer = time.time
        self.ICMP_ECHO_REQUEST = 8
        self.delay = 0
        self.answer = 0

    def checksum(self, source_string):
        sum = 0
        countTo = (len(source_string) / 2) * 2
        count = 0
        while count < countTo:
            sum = sum + source_string[count + 1] * 256 + source_string[count]
            sum = sum & 0xffffffff
            count = count + 2

        if countTo < len(source_string):
            sum = sum + ord(source_string[len(source_string) - 1])
            sum = sum & 0xffffffff

        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)
        self.answer = ~sum
        self.answer = self.answer & 0xffff

        self.answer = self.answer >> 8 | (self.answer << 8 & 0xff00)

        return self.answer

    def receive_one_ping(self, my_socket, ID, timeout):
        """
        receive the ping from the socket.
        """
        timeLeft = timeout
        while True:
            startedSelect = self.default_timer()
            whatReady = select.select([my_socket], [], [], timeLeft)
            howLongInSelect = (self.default_timer() - startedSelect)
            if not whatReady[0]:  # Timeout
                return

            timeReceived = self.default_timer()
            recPacket, addr = my_socket.recvfrom(1024)
            icmpHeader = recPacket[20:28]
            type, code, checksum, packetID, sequence = struct.unpack(
                "bbHHh", icmpHeader
            )
            if type != 8 and packetID == ID:
                bytesInDouble = struct.calcsize("d")
                timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
                return timeReceived - timeSent

            timeLeft = timeLeft - howLongInSelect
            if timeLeft <= 0:
                return

    def send_one_ping(self, my_socket, dest_addr, ID):
        """
        Send one ping to the given >dest_addr<.
        """
        dest_addr = socket.gethostbyname(dest_addr)

        my_checksum = 0

        header = struct.pack("bbHHh", self.ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
        bytesInDouble = struct.calcsize("d")
        data = (192 - bytesInDouble) * "Q"
        data = struct.pack("d", self.default_timer()) + str.encode(data)

        my_checksum = self.checksum(header + data)

        header = struct.pack(
            "bbHHh", self.ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
        )
        packet = header + data
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        my_socket.sendto(packet, (dest_addr, 1))  # Don't know about the 1

    def do_one(self, dest_addr, timeout):
        """
        Returns either the delay (in seconds) or none on timeout.
        """
        icmp = socket.getprotobyname("icmp")
        try:
            my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except socket.error as errno:
            if errno == 1:
                # Operation not permitted
                msg = (
                    " - Note that ICMP messages can only be sent from processes"
                    " running as root."
                )
                raise socket.error(msg)
            raise  # raise the original error

        my_ID = os.getpid() & 0xFFFF

        self.send_one_ping(my_socket, dest_addr, my_ID)
        delay = self.receive_one_ping(my_socket, my_ID, timeout)

        my_socket.close()
        return delay

    def verbose_ping(self, dest_addr, timeout, count):
        median_delay = []
        for i in range(count):
            try:
                self.delay = self.do_one(dest_addr, timeout)
            except socket.gaierror:
                break

            if self.delay is not None:
                self.delay = self.delay * 1000
                median_delay.append(self.delay)
                return self.delay
        return None
