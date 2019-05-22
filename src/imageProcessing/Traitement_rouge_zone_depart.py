from skimage import img_as_float
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import skimage.morphology as mo
import skimage.measure as me
import skimage.draw as dr
from skimage.color import gray2rgb
from skimage import img_as_uint

from config import DEBUG_PLOT, COULEUR
from imageProcessing.Traitement_couleur import Traitement_couleur

"Cette classe hérite de la classe Traitement_couleur et s'occupe du traitement des palets rouges"


class Traitement_Rouge_Zone_Depart(Traitement_couleur):

    def __init__(self, image):
        "Constructeur de la classe"
        Traitement_couleur.__init__(self, image)
        self.image_rouge = image
        self.nb_rouges = 0


    def run(self):
        self.image_rouge = self.traitement_rouge_final(self.image)
        self.centroids()


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
        #im_in_seuillee = self.filtrage_image(im_in, 115)
        im_out = img_as_float(mo.remove_small_holes(im_in_seuillee, 750))
        return im_out

    def traitement_rouge_final(self, im):
        "Regrougement des différentes méthodes de traitements"
        image_rouge = self.traitement_rouge(im)
        image_opening_rouge = self.opening_rouge(image_rouge)
        image_remove_holes = self.removing_holes_rouge(image_opening_rouge)
        return image_remove_holes

    def centroids(self):
        "Cette méthode renvoit les sommets du carré de la cale utilisée pour le redressement"
        im = self.image_rouge
        label = me.label(im)
        regions = me.regionprops(label)
        im_centroids = img_as_uint(gray2rgb(im.copy()))
        j = 0
        count = 0
        for i in range(len(regions)):
            if regions[i].area > 1000:
                x, y = regions[i].centroid
                if COULEUR == "purple":
                    if y < 1000 and x > 100:
                        count += 1
                        x_center = int(x)
                        y_center = int(y)
                        if DEBUG_PLOT:
                            x_draw, y_draw = dr.circle(int(x_center), int(y_center), 10)
                            im_centroids[x_draw, y_draw] = [255, 0, 0]
                        j += 1

                else:
                    if y > 1500 and x > 200 and x<600:
                        x_center = int(x)
                        y_center = int(y)
                        count +=1
                        if DEBUG_PLOT:
                            x_draw, y_draw = dr.circle(int(x_center), int(y_center), 10)
                            im_centroids[x_draw, y_draw] = [255, 0, 0]
                        j += 1

        if DEBUG_PLOT:
            io.imshow(im_centroids)
            plt.show()
        self.nb_rouges = count
        return


image_depart = io.imread('/home/yousra/2A/Cassiopée/Palet-O-Matic/tmp/purple_rouge_rouge_vert.jpg')
traitrouge = Traitement_Rouge_Zone_Depart(image_depart)
traitrouge.run()
io.imshow(traitrouge.image_rouge)
plt.show()
print(traitrouge.nb_rouges)

