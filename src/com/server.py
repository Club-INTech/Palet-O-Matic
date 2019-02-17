import socket
import threading

from src.com.listener import ListerThread


class ServerThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.ip = "127.0.0.1"
        self.port = 1111
        self.connections = []
        self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcpsock.bind((self.ip, self.port))

    def run(self):
        while True:
            self.tcpsock.listen(10)
            print("Listening...")
            (clientsocket, (ip, port)) = self.tcpsock.accept()
            newthread = ListerThread(ip, port, clientsocket)
            newthread.start()
            self.connections += [newthread]
            print("connections")
            print(self.connections)

    def close(self):
        self.tcpsock.close()
