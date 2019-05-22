from skimage import img_as_float
import numpy as np
import skimage.morphology as mo
from skimage import io
import skimage.measure as me
from skimage import img_as_uint
from time import sleep
import matplotlib.pyplot as plt
import skimage.draw as dr
from skimage.color import gray2rgb

from config import DEBUG_PLOT, COULEUR
from imageProcessing.Traitement_couleur import Traitement_couleur

"Cette classe hérite de la classe Traitement_couleur et s'occupe du traitement des palets bleus"


class Traitement_Bleu(Traitement_couleur):

    def __init__(self, image):
        "Constructeur de la classe"
        Traitement_couleur.__init__(self, image)
        self.image_bleu = image
        self.center = []

    def run(self):
        self.image_bleu = self.traitement_bleu_final(self.image)
        self.centroids()
        # Enregistrer l'image après pour visualiiser le résultat : enregistrer aussi dans les différentes étapes de traitement

    def max_soustraction_bleu(self, im_grey):
        "Cette méthode renvoie une image en noir et en blanc en éliminant les pixels inférieurs à un seuil*max(image)"
        val = 0.3 * np.max(im_grey)
        image_2 = im_grey.copy()
        n = im_grey.shape[1]
        p = im_grey.shape[0]
        for i in range(p):
            for j in range(n):
                if (image_2[i][j] < val):
                    image_2[i, j] = val
        return image_2

    def traitement_bleu(self, image_orig):
        "Cette méthode regroupe les différents traitements qu'on fait pour isoler le canal bleu"
        image_rouge = self.canal_rouge(image_orig)
        image_vert = self.canal_vert(image_orig)
        image_bleu = self.canal_bleu(image_orig)
        if DEBUG_PLOT:
            io.imshow(image_bleu)
            plt.show()
        image_vert_rouge = self.moyenne_deux_images_gris(image_vert, image_rouge)
        image_soustr = self.soustraction_deux_images_gris(image_bleu, image_vert_rouge)
        if DEBUG_PLOT:
            io.imshow(image_soustr)
            plt.show()
        image_soustr_max = self.max_soustraction_bleu(image_soustr)
        if DEBUG_PLOT:
            io.imshow(image_soustr_max)
            plt.show()
        return image_soustr_max

    def opening_bleu(self, im_in):
        "Ouverture de l'image "
        cercle = mo.disk(2)
        im_out = mo.opening(im_in, cercle)
        return im_out

    def removing_holes_bleu(self, im_in_grey):
        "Suppression des trous noirs dus au palets "
        im_in_seuillee = self.filtre_otsu(im_in_grey)
        #im_in_seuillee = self.filtrage_image(im_in_grey, 123)
        im_out = img_as_float(mo.remove_small_holes(im_in_seuillee, 100))
        return im_out

    def traitement_bleu_final(self, im):
        "Traitement bleu final : regroupement des différentes méthodes : on a deux méthodes, traitement_bleu " \
        "et traitement_bleu_final pour faciliter le debug"
        image_bleu = self.traitement_bleu(im)
        image_opening_bleu = self.opening_bleu(image_bleu)
        if DEBUG_PLOT:
            io.imshow(image_opening_bleu)
            plt.show()
        image_remove_holes = self.removing_holes_bleu(image_opening_bleu)
        return image_remove_holes

    def centroids(self):
        "Cette méthode renvoit les sommets du carré de la cale utilisée pour le redressement"
        im = self.image_bleu
        label = me.label(im)
        regions = me.regionprops(label)
        im_centroids = img_as_uint(gray2rgb(im.copy()))
        j = 0
        count = 0
        for i in range(len(regions)):
            if regions[i].area > 1000:
                x, y = regions[i].centroid
                if COULEUR == "purple":
                    if y > 100 and x > 100 and y < 500:
                        count += 1
                        x_center = int(x)
                        y_center = int(y)
                        if DEBUG_PLOT:
                            x_draw, y_draw = dr.circle(int(x_center), int(y_center), 10)
                            im_centroids[x_draw, y_draw] = [255, 0, 0]
                        j += 1
                        self.center.append((x_center, y_center))

                else:
                    if y > 1000 and x > 300:
                        x_center = int(x)
                        y_center = int(y)
                        if DEBUG_PLOT:
                            x_draw, y_draw = dr.circle(int(x_center), int(y_center), 10)
                            im_centroids[x_draw, y_draw] = [255, 0, 0]
                        j += 1

        if DEBUG_PLOT:
            io.imshow(im_centroids)
            plt.show()
        return

image_depart = io.imread('/home/yousra/2A/Cassiopée/Palet-O-Matic/tmp/201905221852.jpg')
traitBleu = Traitement_Bleu(image_depart)
traitBleu.run()
print(traitBleu.center)
io.imshow(traitBleu.image_bleu)
plt.show()