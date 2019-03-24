import threading
from Imagery.Camera import *
from Imagery.MotionDetector import *

class CameraThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.camera = Camera.get_instance()
        self.motion_detector = MotionDetector()
        self.running = True
        self.current_processed_jpeg = None

    def run(self):
        motion_detector = self.motion_detector
        camera = self.camera
        while self.running:
            current_frame = camera.get_frame()[1]
            self.current_processed_jpeg = motion_detector.process_and_convert_jpeg(current_frame)

    def get_processed_jpeg(self):
        return self.current_processed_jpeg

    def stop(self):
        self.running = False
