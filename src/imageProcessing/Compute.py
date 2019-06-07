import os
from multiprocessing import Pipe, Process

import skimage
from skimage import io
from time import time, gmtime, strftime

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
    # image_palets_rouge = io.imread(
    # os.path.join(skimage.data_dir, "/home/yousra/2A/Cassiopée/Palet-O-Matic/tmp/image_palets_yellow.jpg"))
    traitrouge = Traitement_Rouge(image_palet, True)
    traitrouge.run()
    child_conn.send(centroids(redresser(traitrouge.image_rouge, coordonnee)))


@time_it
def compute_blue(coordonnee, child_conn, image_palet):
    # image_palets_rouge = io.imread(
    # os.path.join(skimage.data_dir, "/home/yousra/2A/Cassiopée/Palet-O-Matic/tmp/image_palets_yellow.jpg"))
    traitbleu = Traitement_Bleu(image_palet)
    traitbleu.run()
    child_conn.send(centroids(redresser(traitbleu.image_bleu, coordonnee)))


@time_it
def compute_vert(coordonnee, child_conn, image_palet):
    # image_palets_rouge = io.imread(
    # os.path.join(skimage.data_dir, "/home/yousra/2A/Cassiopée/Palet-O-Matic/tmp/image_palets_yellow.jpg"))
    traitvert = Traitement_Vert(image_palet)
    traitvert.run()
    child_conn.send(centroids(redresser(traitvert.image_vert, coordonnee)))


@time_it
def compute(image, image_palet):

    t1 = time()

    # image = io.imread(os.path.join(skimage.data_dir, '/home/yousra/2A/Cassiopée/Palet-O-Matic/tmp/image_cale_yellow_sans_palets.jpg'))
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
