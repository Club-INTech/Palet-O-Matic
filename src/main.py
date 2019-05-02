from Camera import Camera
from com.server import ServerThread
from data.data_handler import DataHandler

server = ServerThread()
data_handler = DataHandler()

server.run(data_handler)

camera = Camera()
camera.show_picture


