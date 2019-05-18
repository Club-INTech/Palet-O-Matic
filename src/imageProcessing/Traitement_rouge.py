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


class Traitement_Rouge(Traitement_couleur):

    def __init__(self, image, match_commence):
        "Constructeur de la classe"
        Traitement_couleur.__init__(self, image)
        self.match_commence = match_commence
        self.image_rouge = image
        self.coordonnee = None
        self.x_center, self.y_center = 0, 0

    def run(self):
        if self.match_commence:
            self.image_rouge = self.traitement_rouge_final(self.image)
        else:
            self.coordonnee = self.centroids_redressement()

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
        #im_in_seuillee = self.filtre_otsu(im_in)
        im_in_seuillee = self.filtrage_image(im_in, 120)
        im_out = img_as_float(mo.remove_small_holes(im_in_seuillee, 750))
        return im_out

    def traitement_rouge_final(self, im):
        "Regrougement des différentes méthodes de traitements"
        image_rouge = self.traitement_rouge(im)
        image_opening_rouge = self.opening_rouge(image_rouge)
        image_remove_holes = self.removing_holes_rouge(image_opening_rouge)
        return image_remove_holes

    def centroids_redressement(self):
        "Cette méthode renvoit les sommets du carré de la cale utilisée pour le redressement"
        im = self.traitement_rouge_final(self.image_rouge)
        self.image_rouge = im
        label = me.label(im)
        regions = me.regionprops(label)
        centers = np.array([[0, 0], [0, 0], [0, 0], [0, 0]])
        im_centroids = img_as_uint(gray2rgb(im.copy()))
        j = 0
        count = 0
        for i in range(len(regions)):
            if (regions[i].area > 1000):
                x, y = regions[i].centroid
                if(COULEUR == "purple"):
                    if (y < 1000 and x > 300):
                        count += 1
                        x_center = int(x)
                        y_center = int(y)
                        centers[j][1] = x_center
                        centers[j][0] = y_center
                        if DEBUG_PLOT:
                            x_draw, y_draw = dr.circle(int(x_center),int(y_center),10)
                            im_centroids[x_draw, y_draw] = [255,0,0]
                        j += 1

                else:
                    if (y > 1000 and x > 300):
                        x_center = int(x)
                        y_center = int(y)
                        centers[j][1] = x_center
                        centers[j][0] = y_center
                        if DEBUG_PLOT:
                            x_draw, y_draw = dr.circle(int(x_center),int(y_center),10)
                            im_centroids[x_draw, y_draw] = [255,0,0]
                        j += 1
        print(centers)
        sum_x = 0
        sum_y = 0
        for point in centers :
            x,y = point
            sum_x = x + sum_x
            sum_y = y + sum_y
        self.x_center = sum_x / 4
        self.y_center = sum_y / 4
        if DEBUG_PLOT:
            x_draw, y_draw = dr.circle(int(self.x_center), int(self.y_center), 10)
            im_centroids[x_draw, y_draw] = [255, 0, 0]
        centers = self.points_redressement(centers)
        print(centers)
        if DEBUG_PLOT:
            io.imshow(im_centroids)
            plt.show()
        return centers


    def points_redressement(self, tab):
        redressement = []
        tab = tab.tolist()
        for point in tab:
            x, y = point
            if x - self.x_center > 0 and y - self.y_center > 0:
                redressement.insert(2, point)
            elif x - self.x_center > 0 and y - self.y_center < 0:
                redressement.insert(1, point)
            elif x - self.x_center  < 0 and y - self.y_center > 0:
                redressement.insert(3, point)
            else:
                redressement.insert(0, point)
        print("redressement", np.asarray(redressement))
        return np.asarray(redressement)



def swap(tab, i, j):
    x, y = tab[i][0], tab[i][1]
    tab[i][0], tab[i][1] = tab[j][0], tab[j][1]
    tab[j][0], tab[j][1] = x, y


