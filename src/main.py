import os
from Camera import Camera
from com.server import ServerThread
from data.data_handler import DataHandler

# server = ServerThread()
# data_handler = DataHandler()
#
# server.run(data_handler)
from imageProcessing.Compute import compute

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

compute(camera.get_picture_recalage, camera.get_picture_palet)
