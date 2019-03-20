import threading

from data.table import Table


class ListerThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):
        #print("Connexion de %s %s" % (self.ip, self.port,))
        #self.send("Hello world")
        self.send_palet_list(Table())
        # message = self.recv()
        # if message != "b''":
        #     print(message)

    def recv(self):
        header=('\x21', '\x2D')
        return self.clientsocket.recv(2048)

    def send(self, message):
        header = ('\x21', '\x2D')
        # print(message)
        message = header[0]+header[1]+message+"\n"
        print(message)
        self.clientsocket.send(message.encode())

    def close(self):
        self.clientsocket.close()

    def send_palet_list(self, table):
        self.send(table.to_json().__str__().replace("'", "\""))
