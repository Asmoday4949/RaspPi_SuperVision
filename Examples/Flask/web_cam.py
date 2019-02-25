import cv2 as ocv
import time

class Camera(object):
    def __init__(self):
        self.cap = ocv.VideoCapture(0)
        if not self.cap.isOpened():
            raise Exception("Cannot open the camera")

    def get_frame(self):
        result, img = self.cap.read()
        return ocv.imencode('.jpg', img)[1].tobytes()

    def stop():
        self.cap.release()

class SharedCamera:
    _instance = None
    def __init__(self):
        if SharedCamera._instance != None:
            raise Exception("Singleton class")

    @staticmethod
    def get_instance():
        if SharedCamera._instance == None:
            SharedCamera._instance = SharedCamera()
        return SharedCamera._instance

    def print(self):
        print("CAMERA");

    def initialize():
        None

    def launch():
