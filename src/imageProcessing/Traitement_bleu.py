from skimage import io, filters
from skimage.color import rgb2gray, rgb2hsv
from skimage import img_as_float, img_as_uint
import numpy as np
from threading import Thread
import skimage.morphology as mo


class Traitement_Bleu(Thread):

    def __init__(self, image):
        Thread.__init__(self)
        self.image = image

    def run(self):
        image_bleu = self.traitement_bleu_final(self.image)
        #Enregistrer l'image après pour visualiiser le résultat 

    def canal_rouge(self, img_orig):
        im_grey = img_orig[:, :, 0]
        return im_grey

    def canal_vert(self, img_orig):
        im_grey = img_orig[:, :, 1]
        return im_grey

    def canal_bleu(self, img_orig):
        im_grey = img_orig[:, :, 2]
        return im_grey

    def moyenne_deux_images_gris(self, img_1, img_2):
        return img_1 // 2 + img_2 // 2

    def soustraction_deux_images_gris(self, img_1, img_2):
        n = img_1.shape[1]
        p = img_1.shape[0]
        im = img_as_uint(np.zeros((p, n)))
        for i in range(img_1.shape[0]):
            for j in range(img_1.shape[1]):
                im[i][j] = max(int(img_1[i][j]) - int(img_2[i][j]), 0)
        return im

    def filtre_otsu(self, im_grey):
        val = filters.threshold_otsu(im_grey)
        image_2 = im_grey.copy()
        mask_1 = image_2 > val
        mask_2 = image_2 < val
        # On met à blanc les pixels respectant le mask
        image_2[mask_1] = 255
        # On met à noir les pixels respectant le mask
        image_2[mask_2] = 0
        return image_2 / 255

    def max_soustraction_bleu(self,im_grey):
        val = 0.7 * np.max(im_grey)
        image_2 = im_grey.copy()
        n = im_grey.shape[1]
        p = im_grey.shape[0]
        for i in range(p):
            for j in range(n):
                if (image_2[i][j] < val):
                    image_2[i, j] = val
        return image_2

    def traitement_bleu(self, image_orig):
        image_rouge = self.canal_rouge(image_orig)
        image_vert = self.canal_vert(image_orig)
        image_bleu = self.canal_bleu(image_orig)
        image_vert_rouge = self.moyenne_deux_images_gris(image_vert, image_rouge)
        image_bleu_rouge = self.moyenne_deux_images_gris(image_bleu, image_rouge)
        image_soustr = self.soustraction_deux_images_gris(image_bleu, image_vert_rouge)
        image_soustr_max = self.max_soustraction_bleu(image_soustr)
        return image_soustr_max

    def opening_bleu(self, im_in):
        cercle = mo.disk(2)
        im_out = mo.opening(im_in, cercle)
        return im_out

    def filtrage_image(self, image, val):
        image_2 = image.copy()
        mask_1 = image_2 > val
        mask_2 = image_2 < val
        # On met à blanc les pixels respectant le mask
        image_2[mask_1] = 255
        # On met à noir les pixels respectant le mask
        image_2[mask_2] = 0
        return image_2

    def removing_holes_bleu(self,im_in_grey):
        # im_in_seuillee = filtre_otsu(im_in_grey)
        im_in_seuillee = self.filtrage_image(im_in_grey, 118.5)
        im_out = img_as_float(mo.remove_small_holes(im_in_seuillee, 10000))
        return im_out

    def traitement_bleu_final(self, im):
        image_bleu = self.traitement_bleu(im)
        image_opening_bleu = self.opening_bleu(image_bleu)
        image_remove_holes = self.removing_holes_bleu(image_opening_bleu)
        return image_remove_holes


image_orig = io.imread("./tests_nouveau_tapis/image_camera/image_toutes_couleurs_2.jpg")

from time import time

t1 = time()
image_bleu = traitement_bleu_final(image_orig)
t2 = time()
print("le temps d'exécution", t2 - t1)
io.imsave("./tests_nouveau_tapis/tests_traitement_bleu/traitement_bleu_final_camera_couleurs_2.png", image_bleu)