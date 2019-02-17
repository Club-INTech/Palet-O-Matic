import threading


class ListerThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port,))
        self.send("Hello world")

        message = self.recv()
        if message != "b''":
            print(message)

    def recv(self):
        return self.clientsocket.recv(2048)

    def send(self, message):
        self.clientsocket.send(message.encode())

    def close(self):
        self.clientsocket.close()
