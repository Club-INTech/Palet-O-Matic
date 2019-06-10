import os
from multiprocessing import Pipe, Process, Array

import skimage
from skimage import io
from time import time, gmtime, strftime

from config import COULEUR
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
def compute_red(coordonnee, child_conn, traitrouge, redtab):
    traitrouge.run()
    centroids(redresser(traitrouge.image_rouge, coordonnee), redtab)


@time_it
def compute_blue(coordonnee, child_conn, traitbleu, bluetab):
    traitbleu.run()
    centroids(redresser(traitbleu.image_bleu, coordonnee), bluetab)


@time_it
def compute_vert(coordonnee, child_conn, traitvert, greentab):
    traitvert.run()
    centroids(redresser(traitvert.image_vert, coordonnee), greentab)


@time_it
def compute_redressement(rouge):

    t1 = time()


    rouge.run()

    t2 = time()
    print("Compute redressement : rouge.coordonne", rouge.coordonnee)
    return rouge.coordonnee


def compute(coordonnee, image_palet, table, test):
    parent_conn, child_conn = Pipe()
    image_palets_rouge = io.imread(image_palet)
    traitrouge = Traitement_Rouge(image_palets_rouge, True)
    redtab = Array('d', 4)
    p_red = Process(target=compute_red, args=(coordonnee, child_conn, traitrouge, redtab))
    p_red.start()

    parent_conn_b, child_conn_b = Pipe()
    image_palets_bleu = io.imread(image_palet)
    traitbleu = Traitement_Bleu(image_palets_bleu)
    bluetab = Array('d', 4)
    p_blue = Process(target=compute_blue, args=(coordonnee, child_conn_b, traitbleu, bluetab))
    p_blue.start()

    parent_conn_v, child_conn_v = Pipe()
    image_palets_vert = io.imread(image_palet)
    traitvert = Traitement_Vert(image_palets_vert)
    greentab = Array('d', 4)
    p_green = Process(target=compute_vert, args=(coordonnee, child_conn_v, traitvert, greentab))
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

    # red = changement_repere(red_position)
    # blue = changement_repere(blue_position)
    # green = changement_repere(green_position)
    red = redtab
    blue = bluetab
    green = greentab

    print("R : positions sur la table en mm", red)
    print("B : positions sur la table en mm", blue)
    print("V : positions sur la table en mm", green)

    if not test:
        if COULEUR == "purple":
            table.purple_chaos[0].x, table.purple_chaos[0].y = red[0], red[2]
            table.purple_chaos[1].x, table.purple_chaos[1].y = red[1], red[3]
            table.purple_chaos[2].x, table.purple_chaos[2].y = green[0], green[2]
            table.purple_chaos[3].x, table.purple_chaos[3].y = blue[0], blue[2]
        else:
            table.yellow_chaos[0].x, table.yellow_chaos[0].y = red[0][0], red[0][1]
            table.yellow_chaos[1].x, table.yellow_chaos[1].y = red[1][0], red[1][1]
            table.yellow_chaos[2].x, table.yellow_chaos[2].y = green[0][0], green[0][1]
            table.yellow_chaos[3].x, table.yellow_chaos[3].y = blue[0][0], blue[0][1]

def compute_without_multiprocess(coordonnee, image_palet, table, test):
    image_palets_rouge = io.imread(image_palet)
    traitrouge = Traitement_Rouge(image_palets_rouge, True)
    traitrouge.run()

    image_palets_bleu = io.imread(image_palet)
    traitbleu = Traitement_Bleu(image_palets_bleu)
    traitbleu.run()

    image_palets_vert = io.imread(image_palet)
    traitvert = Traitement_Vert(image_palets_vert)
    traitvert.run()

    green = centroids(redresser(traitvert.image_vert, coordonnee))
    traitbleu.join()

    blue = centroids(redresser(traitbleu.image_bleu, coordonnee))
    traitrouge.join()

    red = centroids(redresser(traitrouge.image_rouge, coordonnee))

    print("R : positions sur la table en mm", red)
    print("B : positions sur la table en mm", blue)
    print("V : positions sur la table en mm", green)

    if not test:
        if COULEUR == "purple":
            table.purple_chaos[0].x, table.purple_chaos[0].y = red[0][0], red[0][1]
            table.purple_chaos[1].x, table.purple_chaos[1].y = red[1][0], red[1][1]
            table.purple_chaos[2].x, table.purple_chaos[2].y = green[0][0], green[0][1]
            table.purple_chaos[3].x, table.purple_chaos[3].y = blue[0][0], blue[0][1]

        else :
            table.yellow_chaos[0].x, table.yellow_chaos[0].y = red[0][0], red[0][1]
            table.yellow_chaos[1].x, table.yellow_chaos[1].y = red[1][0], red[1][1]
            table.yellow_chaos[2].x, table.yellow_chaos[2].y = green[0][0], green[0][1]
            table.yellow_chaos[3].x, table.yellow_chaos[3].y = blue[0][0], blue[0][1]

