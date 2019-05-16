import os
from time import sleep, time

import skimage
from skimage import io

import math
import numpy as np
import matplotlib.pyplot as plt
import skimage.measure as me
import skimage.draw as dr

from skimage import transform as tf

from imageProcessing.Traitement_bleu import Traitement_Bleu
from imageProcessing.Traitement_vert import Traitement_Vert
from imageProcessing.Traitement_rouge import Traitement_Rouge

filename = []
filename.append(os.path.join(skimage.data_dir, '/home/sam/INTech/Palet-O-Matic/tmp/2019-05-14_15:27:50.jpg'))
filename.append(os.path.join(skimage.data_dir, '/home/sam/INTech/Palet-O-Matic/tmp/2019-05-14_14:59:35.jpg'))
# filename.append(os.path.join(skimage.data_dir, '/home/sam/INTech/Palet-O-Matic/tmp/2019-05-13_15:33:37.jpg'))
# filename.append(os.path.join(skimage.data_dir, '/home/sam/INTech/Palet-O-Matic/tmp/2019-05-13_15:31:29.jpg'))

cote_calle_mm = 330
cote_calle_px = 1080
x_chaos = 500
y_chaos = 1050


def px_to_mm(len_px):
    """
    Converti une longueur en pixel en mm.
    :param len_px:
    :return:
    """
    return len_px * cote_calle_mm / cote_calle_px


def changement_repere(positions):
    """
    Permet le changement du repère de la zone de chaos à celui de la table.
    :param positions:
    :return:
    """
    positions_mm = []
    for x, y in positions:
        x, y = y, cote_calle_px - x
        x -= cote_calle_px / 2
        y -= cote_calle_px / 2
        x = px_to_mm(x) + x_chaos
        y = px_to_mm(y) + y_chaos
        positions_mm.append([x, y])
    return positions_mm


def centroids(image):
    """
    Revoie les centres des palets sur une image binaire redressée.
    :param image:
    :return:
    """
    label = me.label(image)
    regions = me.regionprops(label)
    count = 0
    centroids = []
    for i in range(len(regions)):
        if (regions[i].area > 10000):
            count = count + 1
            x, y = regions[i].centroid
            if x > 200 and x <900:
                centroids.append((x, y))
                x_draw, y_draw = dr.circle(x, y, 20)
                print(centroids)
                image[x_draw, y_draw] = 0
    io.imshow(image)
    plt.show()
    return centroids


def redresser(image, dst):
    """
    Redresse une image prise avec la cale.
    :param image:
    :param dst: vecteur des coordonnées des points répérés grace à la cale.
    :return: image redréssée
    """
    text = image

    # width=1880
    # height=1913
    width = len(image)
    height = len(image)
    src = np.array([[0, 0], [0, height], [width, height], [width, 0]])
    print("dst : ", dst)
    print(len(image))
    # dst = np.array([[1137, 448], [1173, 693], [1537, 683], [1441, 449]])

    tform3 = tf.ProjectiveTransform()
    tform3.estimate(src, dst)
    warped = tf.warp(text, tform3, output_shape=(height, width))
    # name = "./" + str(i) + ".jpg"
    # io.imsave(name, warped)

    fig, ax = plt.subplots(nrows=2, figsize=(8, 3))
    # centroids(warped)
    ax[0].imshow(text, cmap=plt.cm.gray)
    ax[0].plot(dst[:, 0], dst[:, 1], '.r')
    ax[1].imshow(warped, cmap=plt.cm.gray)

    for a in ax:
        a.axis('off')

    plt.tight_layout()

    plt.show()

    return warped


t1 = time()
image = io.imread("/home/yousra/2A/Cassiopée/tests_nouveau_tapis/image_camera/image_cale_sans_palets.jpg")
rouge = Traitement_Rouge(image, False)
rouge.start()
rouge.join()

t2 = time()
rouge.join()
image_palets_rouge = io.imread("/home/yousra/2A/Cassiopée/tests_nouveau_tapis/image_camera/2019-05-14_14_59_35.jpg")
image_palets_vert = io.imread("/home/yousra/2A/Cassiopée/tests_nouveau_tapis/image_camera/2019-05-14_14_59_35.jpg")
image_palets_bleu = io.imread("/home/yousra/2A/Cassiopée/tests_nouveau_tapis/image_camera/2019-05-14_14_59_35.jpg")
traitvert = Traitement_Vert(image_palets_vert)
traitbleu = Traitement_Bleu(image_palets_bleu)
traitrouge = Traitement_Rouge(image_palets_rouge, True)
traitvert.start()
traitbleu.start()
traitrouge.start()
traitvert.join()


green_position = centroids(redresser(traitvert.image_vert, rouge.coordonnee))
traitbleu.join()
blue_position = centroids(redresser(traitbleu.image_bleu, rouge.coordonnee))
traitrouge.join()
red_position = centroids(redresser(traitrouge.image_rouge, rouge.coordonnee))
t3 = time()

print("Le temps d'exécution avant un match", t2-t1)
print("Le temps d'exécution pendant un match", t3-t2)
#sleep(20)
#print("positions dans la zone de chaos en px", green_position)
print("R : positions sur la table en mm", changement_repere(red_position))
#print("positions dans la zone de chaos en px", red_position)
print("G : positions sur la table en mm", changement_repere(green_position))
#print("positions dans la zone de chaos en px", blue_position)
print("B : positions sur la table en mm", changement_repere(blue_position))





# redresser(bleu.image_bleu, 1)