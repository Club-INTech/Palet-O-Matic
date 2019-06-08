import os
import time

from matplotlib import pyplot as plt
from skimage import io
# os.system("ffmpeg -f video4linux2 -s 640x480 -i /dev/video0 -vframes 1 $(date +\%Y\%m\%d\%H\%M).jpg")
# os.system("ffmpeg -f video4linux2 -i /dev/video0 -vframes 1 ./tmp/$(date +\%Y\%m\%d\%H\%M%S).jpg")


class Camera:

    def __init__(self):
        self.picture_recalage = self.take_picture()
        self.picture_palet = self.take_picture()

    def take_picture(self):
        """
        Prend une image que l'on peut récupérer avec la méthode get_picture().
        Les images sont stockées dans le répertoire tmp/
        """

        ts = time.gmtime()
        date = time.strftime("%Y-%m-%d_%H:%M:%S", ts)
        os.system("sh src/picture.sh " + date)
        return "./tmp/"+date+".jpg"

    @property
    def take_picture_recalage(self):
        self.picture_recalage = self.take_picture()

    @property
    def take_picture_palet(self):
        self.picture_palet = self.take_picture()

    @property
    def get_picture_recalage(self):
        return self.picture_recalage

    @property
    def get_picture_palet(self):
        return self.picture_palet

    @property
    def show_picture_recalage(self):
        """
        Affiche l'image capturée.
        """
        io.imshow(self.picture_recalage)
        plt.show()

    @property
    def show_picture_palet(self):
        """
        Affiche l'image capturée.
        """
        io.imshow(self.picture_palet)
        plt.show()