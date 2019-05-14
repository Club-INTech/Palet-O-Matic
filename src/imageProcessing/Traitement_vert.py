from skimage import img_as_float
import numpy as np
import skimage.morphology as mo

from imageProcessing.Traitement_couleur import Traitement_couleur

"Cette classe hérite de la classe Traitement_couleur et s'occupe du traitement des palets rouges"


class Traitement_Vert(Traitement_couleur):

    def __init__(self, image):
        "Constructeur"
        super.__init__(image)

    def run(self):
        self.image_vert = self.traitement_vert_final(self.image)

    def traitement_vert_final(self, im):
        "Regrougement des différentes méthodes de traitements"
        image_vert = self.traitement_vert(im)
        image_opening_vert = self.opening_vert(image_vert)
        image_remove_holes = self.removing_holes_vert(image_opening_vert)
        return image_remove_holes

    def removing_holes_vert(self, im_in_grey):
        "Suppression des cercles noirs "
        im_in_seuillee = self.filtre_otsu(im_in_grey)  #: utiliser le filtre otsu pour avoir une idée du seuil
        # + tracer l'histogramme
        # im_in_seuillee = filtrage_image(im_in_grey,70)
        im_out = img_as_float(mo.remove_small_holes(im_in_seuillee, 1))
        return im_out

    def opening_vert(self, im_in):
        "OUverture de l'image"
        cercle = mo.disk(7)
        im_out = mo.opening(im_in, cercle)
        return im_out

    def traitement_vert(self, image_orig):
        "Cette méthode regroupe les différents traitements qu'on fait pour isoler le canal vert"
        image_rouge = self.canal_rouge(image_orig)
        image_vert = self.canal_vert(image_orig)
        image_bleu = self.canal_bleu(image_orig)
        image_bleu_rouge = self.moyenne_deux_images_gris(image_bleu, image_rouge)
        image_soustr = self.soustraction_deux_images_gris(image_vert, image_bleu_rouge)
        image_soustr_max = self.max_soustraction_vert(image_soustr)
        return image_soustr_max

    def max_soustraction_vert(self, im_grey):
        "Cette méthode renvoie une image en noir et en blanc en éliminant les pixels inférieurs à un seuil*max(image)"
        val = 0.3 * np.max(im_grey)
        n = im_grey.shape[1]
        p = im_grey.shape[0]
        for i in range(p):
            for j in range(n):
                if (im_grey[i][j] < val):
                    im_grey[i, j] = val
        return im_grey
