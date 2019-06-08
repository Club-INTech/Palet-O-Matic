import os
from Camera import Camera
from com.server import ServerThread
from data.data_handler import DataHandler



print("Ajuster le filtre polarisant")
os.system("sh src/direct.sh")
input("filtre ajusté ? ")

camera = Camera()

input("prendre photo recalage ?")

camera.take_picture_recalage

input("prendre photo palet ?")

camera.take_picture_palet

input("lancement !")

server = ServerThread()
data_handler = DataHandler(camera)

server.run(data_handler)