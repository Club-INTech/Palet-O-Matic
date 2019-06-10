from skimage import io

import numpy as np
import matplotlib.pyplot as plt
import skimage.measure as me
import skimage.draw as dr

from skimage import transform as tf

from config import COTE_CALE_MM, COTE_CALE_PX, X_CHAOS_YELLOW, COULEUR, X_CHAOS_PURPLE, Y_CHAOS_YELLOW, Y_CHAOS_PURPLE, \
    DEBUG_PLOT, DEBUG


def px_to_mm(len_px):
    """
    Converti une longueur en pixel en mm.
    :param len_px:
    :return:
    """
    return len_px * COTE_CALE_MM / COTE_CALE_PX


def changement_repere(positions):
    """
    Permet le changement du repère de la zone de chaos à celui de la table.
    :param positions:
    :return:
    """
    positions_mm = []
    x_chaos = X_CHAOS_PURPLE if COULEUR is "purple" else X_CHAOS_YELLOW
    y_chaos = Y_CHAOS_PURPLE if COULEUR is "purple" else Y_CHAOS_YELLOW

    for x, y in positions:
        x, y = y, COTE_CALE_PX - x
        x -= COTE_CALE_PX / 2
        y -= COTE_CALE_PX / 2
        x = px_to_mm(x) + x_chaos
        y = px_to_mm(y) + y_chaos
        positions_mm.append([x, y])
    return positions_mm


def centroids(image, centroids):
    """
    Revoie les centres des palets sur une image binaire redressée.
    :param image:
    :return:
    """
    label = me.label(image)
    regions = me.regionprops(label)
    count = 0
    for i in range(len(regions)):
        if regions[i].area > 10000:
            count = count + 1
            x, y = regions[i].centroid
            if x > 200 and x < 900:
                centroids[i], centroids[i+2] = x, y
                if DEBUG_PLOT:
                    x_draw, y_draw = dr.circle(x, y, 20)
                    print(centroids)
                    image[x_draw, y_draw] = 0
    if DEBUG_PLOT:
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
    if DEBUG:
        print("dst : ", dst)
        print(len(image))
    # dst = np.array([[1137, 448], [1173, 693], [1537, 683], [1441, 449]])

    tform3 = tf.ProjectiveTransform()
    tform3.estimate(src, dst)
    warped = tf.warp(text, tform3, output_shape=(height, width))
    # name = "./" + str(i) + ".jpg"
    # io.imsave(name, warped)

    if DEBUG_PLOT:
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

