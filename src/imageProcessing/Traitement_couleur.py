from threading import Thread
from skimage import img_as_uint
from skimage import filters
import numpy as np
import skimage.measure as me
import math
from skimage.transform import rotate
"Cette classe dessine le squelette pour les différents traitements d'images pour les trois canaux"
class Traitement_couleur(Thread):

    "Constructeur de la classe : on lui fournit l'image qu'on a pris "
    def __init__(self, image):
        Thread.__init__(self)
        self.image = image

    "Isolation du canal rouge"
    def canal_rouge(self, img_orig):
        im_grey = img_orig[:, :, 0]
        return im_grey

    "Isolation du canal vert"
    def canal_vert(self, img_orig):
        im_grey = img_orig[:, :, 1]
        return im_grey

    "Isolation du canal bleu"
    def canal_bleu(self, img_orig):
        im_grey = img_orig[:, :, 2]
        return im_grey

    "Moyenne de deux images "
    def moyenne_deux_images_gris(self, img_1, img_2):
        return img_1 // 2 + img_2 // 2

    "Soustraction de deux images "
    def soustraction_deux_images_gris(self, img_1, img_2):
        n = img_1.shape[1]
        p = img_1.shape[0]
        im = img_as_uint(np.zeros((p, n)))
        for i in range(img_1.shape[0]):
            for j in range(img_1.shape[1]):
                im[i][j] = max(int(img_1[i][j]) - int(img_2[i][j]), 0)
        return im

    "Filtre otsu sur une image, cette fonction retroune une image en noir et en blanc "
    def filtre_otsu(self, im_grey):
        val = filters.threshold_otsu(im_grey)
        image_2 = im_grey.copy()
        mask_1 = image_2 > val
        mask_2 = image_2 < val
        # On met à blanc les pixels respectant le mask
        image_2[mask_1] = 255
        # On met à noir les pixels respectant le mask
        image_2[mask_2] = 0
        return image_2
    "Cette fonction filtre une image suivant un seuil, c'est comme la méthode filtre_otsu mais on spécifie la valeur de"
    " de filtrage"
    def filtrage_image(self, image, val):
        image_2 = image.copy()
        mask_1 = image_2 > val
        mask_2 = image_2 < val
        # On met à blanc les pixels respectant le mask
        image_2[mask_1] = 255
        # On met à noir les pixels respectant le mask
        image_2[mask_2] = 0
        return image_2

    "Cette méthode calcule les centroids d'une image en noir et en blanc,elle retourne l'angle de rotation, " \
    "les centroids, ainsi que le centre de rotation utilisée par la méthode rotate"
    def centroids(self, image):
        label = me.label(image)
        regions = me.regionprops(label)
        count = 0
        x_max, y_max = 0, 0
        x_min, y_min = 0, 0
        first = True
        centroids = []
        for i in range(len(regions)):
            if (regions[i].area > 1000):
                count = count + 1
                x, y = regions[i].centroid
                centroids.append((x, y))
                if (first):
                    y_min = y
                    x_min = x
                    first = False
                if (y < y_min):
                    y_min = y
                    x_min = x
                if (y > y_max):
                    y_max = y
                    x_max = x
        angle_rotate = math.degrees(np.arctan((x_max - x_min) / (y_max - y_min)))
        return angle_rotate, centroids, (x_min, y_min)

    "Cette méthode fait la rotation d'image suivant un angle et un centre de rotation"
    def rotate(self,image):
        image_rotate = rotate(image, self.centroids(0), self.centroids(2))
        return image_rotate

