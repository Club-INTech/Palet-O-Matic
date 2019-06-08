import threading

from data.table import Table
from imageProcessing import Traitement_bleu
from imageProcessing import Traitement_vert
from imageProcessing import Traitement_rouge
from imageProcessing.Compute import compute, compute_redressement


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
        self.coordonee = []

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

        if self.match_commence:
            compute(self.coordonee, self.camera.get_picture_palet, self.table)
            self.notify_pallet_list()
        else :
            self.coordonee = compute_redressement(self.camera.get_picture_recalage)

    @property
    def is_match_commence(self):
        return self.match_commence

    @property
    def set_match_commence(self):
        self.match_commence = True
