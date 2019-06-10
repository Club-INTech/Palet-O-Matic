import os
from Camera import Camera
from imageProcessing.Compute import compute_without_multiprocess, compute_redressement
from imageProcessing.Traitement_rouge import Traitement_Rouge
from skimage import io


print("Ajuster le filtre polarisant")
os.system("sh src/direct.sh")
input("filtre ajusté ? ")

camera = Camera()

input("prendre photo recalage ?")

camera.take_picture_recalage

input("prendre photo palet ?")

camera.take_picture_palet

# input("afficher photos")
# camera.show_picture_palet
# camera.show_picture_recalage

input("lancer compute")
image = io.imread(camera.get_picture_recalage)
rouge = Traitement_Rouge(image, False)
compute_redressement(rouge)
coordonnee = rouge.coordonnee
print("coordonnee", coordonnee)
compute_without_multiprocess(coordonnee, camera.get_picture_palet, None, True)