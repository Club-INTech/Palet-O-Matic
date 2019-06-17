import threading

from data.table import Table
from imageProcessing import Traitement_bleu
from imageProcessing import Traitement_vert
from imageProcessing import Traitement_rouge


class DataHandler(threading.Thread):
    """
    Processus qui s'occupe de mettre à jour les coordonnées des palets en appelant les méthodes du
    package imageProcessing.
    observable.
    """

    def __init__(self, camera):
        self.table = Table()
        self.match_commence = False
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

    # def image_processing(self):
    #     """
    #     Appelle les méthodes de imageProcessing et met à jour les palets.
    #     Notifie les listener pour qu'ils envoient les infos aux robot
    #     """
    #     thread_rouge = Traitement_rouge(self.camera.picture, self.match_commence)
    #     thread_bleu = Traitement_bleu(self.camera.picture)
    #     thread_vert = Traitement_vert(self.camera.picture)
    #     if self.match_commence:
    #         thread_bleu.start()
    #         thread_vert.start()
    #         thread_rouge.start()
    #         self.notify_pallet_list()
    #     else :
    #         thread_rouge.start()

    def match_commence(self):
        return self.match_commence

    def set_match_commence(self):
        self.match_commence = True
