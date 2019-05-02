import threading

from data.table import Table


class DataHandler(threading.Thread):
    """
    Processus qui s'occupe de mettre à jour les coordonnées des palets en appelant les méthodes du
    package imageProcessing.
    observable.
    """

    def __init__(self):
        self.table = Table()
        self.match_commence = False
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(self, *args, **kwargs)

    def notify_pallet_list(self):
        for observer in self.__observers:
            observer.send_palet_list(self.table)

    def image_processing(self):
        """
        Appelle les méthodes de imageProcessing et met à jour les palets.
        Notifie les listener pour qu'ils envoient les infos aux robot
        """
    #     todo
        self.notify_pallet_list()

    @property
    def match_commence(self):
        return self.match_commence

    @property
    def set_match_commence(self):
        self.match_commence = True
