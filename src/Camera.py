import os
import time

from matplotlib import pyplot as plt
from skimage import io
# os.system("ffmpeg -f video4linux2 -s 640x480 -i /dev/video0 -vframes 1 $(date +\%Y\%m\%d\%H\%M).jpg")
# os.system("ffmpeg -f video4linux2 -i /dev/video0 -vframes 1 ./tmp/$(date +\%Y\%m\%d\%H\%M%S).jpg")


class Camera:

    def __init__(self):
        self.picture = self.take_picture()

    def take_picture(self):
        """
        Prend une image que l'on peut récupérer avec la méthode get_picture().
        Les images sont stockées dans le répertoire tmp/
        """

        ts = time.gmtime()
        date = time.strftime("%Y-%m-%d_%H:%M:%S", ts)
        os.system("sh src/picture.sh " + date)
        self.picture = io.imread("./tmp/"+date+".jpg")
        return self.picture

    @property
    def get_picture(self):
        return self.picture

    @property
    def show_picture(self):
        """
        Affiche l'image capturée.
        """
        io.imshow(self.picture)
        plt.show()