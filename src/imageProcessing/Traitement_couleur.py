from skimage import img_as_uint
from skimage import filters
import numpy as np

"Cette classe dessine le squelette pour les différents traitements d'images pour les trois canaux"


class Traitement_couleur():

    def __init__(self, image):
        "Constructeur de la classe : on lui fournit l'image qu'on a pris "
        self.image = image

    def canal_rouge(self, img_orig):
        "Isolation du canal rouge"
        im_grey = img_orig[:, :, 0]
        return im_grey

    def canal_vert(self, img_orig):
        "Isolation du canal vert"
        im_grey = img_orig[:, :, 1]
        return im_grey

    def canal_bleu(self, img_orig):
        "Isolation du canal bleu"
        im_grey = img_orig[:, :, 2]
        return im_grey

    def moyenne_deux_images_gris(self, img_1, img_2):
        "Moyenne de deux images "
        return img_1 // 2 + img_2 // 2

    def soustraction_deux_images_gris(self, img_1, img_2):
        "Soustraction de deux images "
        n = img_1.shape[1]
        p = img_1.shape[0]
        im = img_as_uint(np.zeros((p, n)))
        for i in range(img_1.shape[0]):
            for j in range(img_1.shape[1]):
                im[i][j] = max(int(img_1[i][j]) - int(img_2[i][j]), 0)
        return im

    def filtre_otsu(self, im_grey):
        "Filtre otsu sur une image, cette fonction retroune une image en noir et en blanc "
        val = filters.threshold_otsu(im_grey)
        print(val)
        image_2 = im_grey.copy()
        mask_1 = image_2 > val
        mask_2 = image_2 < val
        # On met à blanc les pixels respectant le mask
        image_2[mask_1] = 255
        # On met à noir les pixels respectant le mask
        image_2[mask_2] = 0
        return image_2

    def filtrage_image(self, image, val):
        "Cette fonction filtre une image suivant un seuil, c'est comme la méthode filtre_otsu mais on spécifie la valeur de"
        " de filtrage"
        image_2 = image.copy()
        mask_1 = image_2 > val
        mask_2 = image_2 < val
        # On met à blanc les pixels respectant le mask
        image_2[mask_1] = 255
        # On met à noir les pixels respectant le mask
        image_2[mask_2] = 0
        return image_2

    def traitement_couleur(self, image_orig, couleur):
        n = image_orig.shape[1]
        p = image_orig.shape[0]
        im = img_as_uint(np.zeros((p, n)))
        for i in range(p):
            for j in range(n):
                im[i, j] = max(image_orig[i, j, couleur] - 0.5 * (image_orig[i, j, (couleur + 1) % 3] + image_orig[i, j, (couleur + 2) % 3]), 0)
        return im
