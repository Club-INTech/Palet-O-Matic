import threading

from data.table import Table
from skimage import io
from imageProcessing.Compute import compute, compute_redressement
from imageProcessing.Traitement_rouge import Traitement_Rouge


class DataHandler(threading.Thread):
    """
    Processus qui s'occupe de mettre à jour les coordonnées des palets en appelant les méthodes du
    package imageProcessing.
    observable.
    """

    def __init__(self, camera):
        self.table = Table()
        self.match_commence = False
        self.detection_done = False
        self.__observers = []
        self.camera = camera
        self.coordonnee = []
        self.rouge = None

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
            if not self.detection_done:
                compute(self.coordonnee, self.camera.get_picture_palet, self.table, False)
                self.detection_done = True
            self.notify_pallet_list()
        else:
            self.camera.take_picture_palet
            image = io.imread(self.camera.get_picture_recalage)
            self.rouge = Traitement_Rouge(image, False)
            compute_redressement(self.rouge)
            self.coordonnee = self.rouge.coordonnee

    @property
    def set_match_commence(self):
        self.match_commence = True
