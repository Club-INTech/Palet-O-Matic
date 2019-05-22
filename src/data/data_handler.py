import threading

from data.Table_Zone_Depart import Table_Zone_Depart
from imageProcessing import Traitement_rouge_zone_depart

class DataHandler(threading.Thread):
    """
    Processus qui s'occupe de mettre à jour les coordonnées des palets en appelant les méthodes du
    package imageProcessing.
    observable.
    """

    def __init__(self, camera):
        self.table = Table_Zone_Depart()
        self.__observers = []
        self.camera = camera

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
        thread_rouge = Traitement_rouge_zone_depart(self.camera.picture)
        thread_rouge.start()
        self.notify_pallet_list()


