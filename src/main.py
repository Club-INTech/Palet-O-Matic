import os
from Camera import Camera
from com.server import ServerThread
from data.data_handler import DataHandler
from imageProcessing.Compute import compute

print("Ajuster le filtre polarisant")
os.system("sh src/direct.sh")
input("filtre ajusté ? ")

camera = Camera()
data_handler = DataHandler(camera)


input("prendre photo recalage ?")

camera.take_picture_recalage

input("prendre photo palet ?")

camera.take_picture_palet

# input("afficher photos")
# camera.show_picture_palet
# camera.show_picture_recalage

input("lancer compute")

# image_cale = "/home/sam/INTech/Palet-O-Matic/tmp/2019-06-17_14:16:57.jpg"
# image_palets = "/home/sam/INTech/Palet-O-Matic/tmp/2019-06-17_14:17:21.jpg"

# compute(image_cale, image_palets, data_handler)
compute(camera.get_picture_recalage, camera.get_picture_palet, data_handler)

print(data_handler.table.to_json())

server = ServerThread()
server.run(data_handler)
