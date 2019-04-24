from skimage import io, filters
from skimage import img_as_float, img_as_uint
import numpy as np
from threading import Thread
import skimage.morphology as mo


class Traitement_Rouge(Thread):

    def __init__(self, image):
        Thread.__init__(self)
        self.image = image

    def run(self):
        image_rouge = self.traitement_rouge_final(self.image)
        io.imsave("./tests_nouveau_tapis/tests_traitement_rouge/traitement_final_rouge_camera_couleurs_2.png",
                  image_rouge)

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

    def max_soustraction_rouge(self, im_grey):
        val = 0.5 * np.max(im_grey)
        n = im_grey.shape[1]
        p = im_grey.shape[0]
        for i in range(p):
            for j in range(n):
                if (im_grey[i][j] < val):
                    im_grey[i, j] = val
        return im_grey

    def traitement_rouge(self, image_orig):
        image_rouge = self.canal_rouge(image_orig)
        image_vert = self.canal_vert(image_orig)
        image_bleu = self.canal_bleu(image_orig)
        image_vert_bleu = self.moyenne_deux_images_gris(image_vert, image_bleu)
        image_soustr = self.soustraction_deux_images_gris(image_rouge, image_vert_bleu)
        image_soustr_max = self.max_soustraction_rouge(image_soustr)
        return image_soustr_max

    def opening_rouge(self, im_in):
        cercle = mo.disk(1)
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

    def removing_holes_rouge(self, im_in):
        im_in_seuillee = self.filtre_otsu(im_in)
        # im_in_seuillee = filtrage_image(im_in,118)
        im_out = img_as_float(mo.remove_small_holes(im_in_seuillee, 750))
        return im_out

    def traitement_rouge_final(self, im):
        image_rouge = self.traitement_rouge(im)
        image_opening_rouge = self.opening_rouge(image_rouge)
        image_remove_holes = self.removing_holes_rouge(image_opening_rouge)
        return image_remove_holes





