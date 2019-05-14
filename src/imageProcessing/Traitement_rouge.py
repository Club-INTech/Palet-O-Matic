from skimage import io
from skimage import img_as_float
import numpy as np
import skimage.morphology as mo

from imageProcessing.Traitement_couleur import Traitement_couleur

"Cette classe hérite de la classe Traitement_couleur et s'occupe du traitement des palets rouges"


class Traitement_Rouge(Traitement_couleur):

    def __init__(self, image, match_commence):
        "Constructeur de la classe"
        super.__init__(image)
        self.match_commence = match_commence

    def run(self):
        self.image_rouge = self.traitement_rouge_final(self.image)

    def max_soustraction_rouge(self, im_grey):
        "Cette méthode renvoie une image en noir et en blanc en éliminant les pixels inférieurs à un seuil*max(image)"
        val = 0.5 * np.max(im_grey)
        n = im_grey.shape[1]
        p = im_grey.shape[0]
        for i in range(p):
            for j in range(n):
                if (im_grey[i][j] < val):
                    im_grey[i, j] = val
        return im_grey

    def traitement_rouge(self, image_orig):
        "Cette méthode regroupe les différents traitements qu'on fait pour isoler le canal rouge"
        image_rouge = self.canal_rouge(image_orig)
        image_vert = self.canal_vert(image_orig)
        image_bleu = self.canal_bleu(image_orig)
        image_vert_bleu = self.moyenne_deux_images_gris(image_vert, image_bleu)
        image_soustr = self.soustraction_deux_images_gris(image_rouge, image_vert_bleu)
        image_soustr_max = self.max_soustraction_rouge(image_soustr)
        return image_soustr_max

    def opening_rouge(self, im_in):
        "Ouverture de l'image"
        cercle = mo.disk(1)
        im_out = mo.opening(im_in, cercle)
        return im_out

    def removing_holes_rouge(self, im_in):
        "Suppression des trous noirs dus au palets "
        im_in_seuillee = self.filtre_otsu(im_in)
        # im_in_seuillee = filtrage_image(im_in,118)
        im_out = img_as_float(mo.remove_small_holes(im_in_seuillee, 750))
        return im_out

    def traitement_rouge_final(self, im):
        "Regrougement des différentes méthodes de traitements"
        image_rouge = self.traitement_rouge(im)
        image_opening_rouge = self.opening_rouge(image_rouge)
        image_remove_holes = self.removing_holes_rouge(image_opening_rouge)
        return image_remove_holes
