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
    image_palets_rouge = io.imread(image_palet)
    # os.path.join(skimage.data_dir, "/home/yousra/2A/Cassiopée/Palet-O-Matic/tmp/image_palets_yellow.jpg"))
    traitrouge = Traitement_Rouge(image_palets_rouge, True)
    traitrouge.run()
    child_conn.send(centroids(redresser(traitrouge.image_rouge, coordonnee)))


@time_it
def compute_blue(coordonnee, child_conn, image_palet):
    image_palets_rouge = io.imread(image_palet)
    # os.path.join(skimage.data_dir, "/home/yousra/2A/Cassiopée/Palet-O-Matic/tmp/image_palets_yellow.jpg"))
    traitbleu = Traitement_Bleu(image_palets_rouge)
    traitbleu.run()
    child_conn.send(centroids(redresser(traitbleu.image_bleu, coordonnee)))


@time_it
def compute_vert(coordonnee, child_conn, image_palet):
    image_palets_rouge = io.imread(image_palet)
    # os.path.join(skimage.data_dir, "/home/yousra/2A/Cassiopée/Palet-O-Matic/tmp/image_palets_yellow.jpg"))
    traitvert = Traitement_Vert(image_palets_rouge)
    traitvert.run()
    child_conn.send(centroids(redresser(traitvert.image_vert, coordonnee)))


@time_it
def compute_redressement(rouge):

    t1 = time()


    rouge.run()

    t2 = time()
    print("Compute redressement : rouge.coordonne", rouge.coordonnee)
    return rouge.coordonnee


def compute(coordonnee, image_palet, table, test):
    parent_conn, child_conn = Pipe()
    p_red = Process(target=compute_red, args=(coordonnee, child_conn, image_palet))
    p_red.start()

    parent_conn_b, child_conn_b = Pipe()
    p_blue = Process(target=compute_blue, args=(coordonnee, child_conn_b, image_palet))
    p_blue.start()

    parent_conn_v, child_conn_v = Pipe()
    p_green = Process(target=compute_vert, args=(coordonnee, child_conn_v, image_palet))
    p_green.start()

    p_red.join()
    red_position = parent_conn.recv()

    p_blue.join()
    blue_position = parent_conn_b.recv()

    p_green.join()
    green_position = parent_conn_v.recv()

    t3 = time()

    # print("Le temps d'exécution avant un match", t2 - t1)
    # print("Le temps d'exécution pendant un match", t3 - t2)

    red = changement_repere(red_position)
    blue = changement_repere(blue_position)
    green = changement_repere(green_position)

    print("R : positions sur la table en mm", red)
    print("B : positions sur la table en mm", blue)
    print("V : positions sur la table en mm", green)

    if not test:
        table.purple_chaos[0].x, table.purple_chaos[0].y = red[0][0], red[0][1]
        table.purple_chaos[1].x, table.purple_chaos[1].y = red[1][0], red[1][1]
        table.purple_chaos[2].x, table.purple_chaos[2].y = green[0], green[1]
        table.purple_chaos[3].x, table.purple_chaos[3].y = blue[0], blue[1]

