import threading
import time




class ListerThread(threading.Thread):
    """"
    observer
    """

    def __init__(self, ip, port, clientsocket, data_handler):
        threading.Thread.__init__(self)
        self.data_handler = data_handler
        self.data_handler.register_observer(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):
        print("Connexion de %s %s" % (self.ip, self.port,))
        #self.send("Hello world")
        # on attend que le match commence
        while not self.data_handler.is_match_commmence:
            time.sleep(0.08)
            if self.recv() != "GO":
                print("recuuuuuuuuuuuuuuuuuuuu")
                self.data_handler.set_match_commence
        self.data_handler.image_processing()
        # self.send_palet_list(Table())
        # message = self.recv()
        # if message != "b''":
        #     print(message)

    def recv(self):
        header = ('\x21', '\x2D')
        return self.clientsocket.recv(2048).replace(header[0], "").replace(header[1], "")

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

    def notify(self, observable, *args, **kwargs):
        print('Got', args, kwargs, 'From', observable)
