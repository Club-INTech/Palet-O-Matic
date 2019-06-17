import socket
import threading

from com.listener import ListerThread


class ServerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.ip = "192.168.12.7"
        self.port = 42111
        self.connections = []
        self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpsock.bind((self.ip, self.port))

    def run(self, data_handler):
        while True:
            self.tcpsock.listen(10)
            print("Listening...")
            (clientsocket, (ip, port)) = self.tcpsock.accept()
            newthread = ListerThread(ip, port, clientsocket, data_handler)
            newthread.start()
            self.connections += [newthread]
            print("connections")
            print(self.connections)

    def close(self):
        self.tcpsock.close()
