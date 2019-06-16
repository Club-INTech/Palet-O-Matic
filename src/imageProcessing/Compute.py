import os
from multiprocessing import Pipe, Process

from skimage.color import rgb2gray
from skimage import io
from time import time, gmtime, strftime
import skimage.draw as dr
import matplotlib.pyplot as plt


from config import DEMO
from imageProcessing.Redressement import centroids, redresser, changement_repere
from imageProcessing.Traitement_bleu import Traitement_Bleu
from imageProcessing.Traitement_rouge import Traitement_Rouge
from imageProcessing.Traitement_vert import Traitement_Vert



def time_it(func):
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        elapsed = time()-start
        readable = strftime("%H:%M:%S", gmtime(elapsed))
        print('Func "{}": {} sec'.format(func.__name__, readable))
    return wrapper


@time_it
def compute_red(coordonnee, child_conn, image_palet):
    image_palets_rouge = io.imread(image_palet)
    # os.path.join(skimage.data_dir, "/home/yousra/2A/Cassiopée/Palet-O-Matic/tmp/image_palets_yellow.jpg"))
    traitrouge = Traitement_Rouge(image_palets_rouge, True)
    traitrouge.run()
    centroids_red = centroids(redresser(traitrouge.image_rouge, coordonnee))
    child_conn.send(centroids_red)


@time_it
def compute_blue(coordonnee, child_conn, image_palet):
    image_palets_rouge = io.imread(image_palet)
    # os.path.join(skimage.data_dir, "/home/yousra/2A/Cassiopée/Palet-O-Matic/tmp/image_palets_yellow.jpg"))
    traitbleu = Traitement_Bleu(image_palets_rouge)
    traitbleu.run()
    centroids_bleus = centroids(redresser(traitbleu.image_bleu, coordonnee))
    child_conn.send(centroids_bleus)


@time_it
def compute_vert(coordonnee, child_conn, image_palet):
    image_palets_rouge = io.imread(image_palet)
    # os.path.join(skimage.data_dir, "/home/yousra/2A/Cassiopée/Palet-O-Matic/tmp/image_palets_yellow.jpg"))
    traitvert = Traitement_Vert(image_palets_rouge)
    traitvert.run()
    centroids_verts = centroids(redresser(traitvert.image_vert, coordonnee))
    child_conn.send(centroids_verts)

def demonstration(image_org, coord, centroids_red, centroids_bleus, centroids_verts):
    #image_org = rgb2gray(image_org)
    image = redresser(image_org, coord)
    for point in centroids_red:
        x, y = point[0], point[1]
        x_cent, y_cent = dr.circle(x, y, 10)
        image[x_cent, y_cent] = [0, 255, 255]
    for point in centroids_bleus:
        x, y = point[0], point[1]
        x_cent, y_cent = dr.circle(x, y, 10)
        image[x_cent, y_cent] = [255, 255, 0]
    for point in centroids_verts:
        x, y = point[0], point[1]
        x_cent, y_cent = dr.circle(x, y, 10)
        image[x_cent, y_cent] = [255, 0, 255]

    io.imshow(image)
    plt.show()




@time_it
def compute(image, image_palet):

    t1 = time()

    image = io.imread(image)
    rouge = Traitement_Rouge(image, False)
    rouge.run()

    t2 = time()

    parent_conn, child_conn = Pipe()
    p_red = Process(target=compute_red, args=(rouge.coordonnee, child_conn, image_palet))
    p_red.start()

    parent_conn_b, child_conn_b = Pipe()
    p_blue = Process(target=compute_blue, args=(rouge.coordonnee, child_conn_b, image_palet))
    p_blue.start()

    parent_conn_v, child_conn_v = Pipe()
    p_green = Process(target=compute_vert, args=(rouge.coordonnee, child_conn_v, image_palet))
    p_green.start()

    p_red.join()
    red_position = parent_conn.recv()

    p_blue.join()
    blue_position = parent_conn_b.recv()

    p_green.join()
    green_position = parent_conn_v.recv()

    t3 = time()

    print("Le temps d'exécution avant un match", t2 - t1)
    print("Le temps d'exécution pendant un match", t3 - t2)

    print("R : positions sur la table en mm", changement_repere(red_position))
    print("B : positions sur la table en mm", changement_repere(blue_position))
    print("V : positions sur la table en mm", changement_repere(green_position))

    if DEMO :
        image_palet = io.imread(image_palet)
        demonstration(image_palet, rouge.coordonnee, red_position, blue_position, green_position)
        io.imshow(image_palet)
        plt.show()

