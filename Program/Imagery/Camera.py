from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time

class Camera():
    ''' Camera class which represent one of the several camera that you can use.
        This class cannot be used directly. You must implement methods into a child class.
     '''
    _instance = None

    def __init__(self):
        if Camera._instance != None:
            raise Exception("You can't create it, it's a singleton")

    @staticmethod
    def get_instance():
        if Camera._instance == None:
            Camera._instance = WebCam()
        return Camera._instance

    def get_frame(self, size):
        raise NotImplementedError("Must be implemented into child class")

    def get_jpeg(self):
        result, frame = self.get_frame()
        return cv2.imencode('.jpg', frame)[1].tobytes()

    def stop(self):
        raise NotImplementedError("Must be implemented into child class")

class PiCam(Camera):
    ''' Specific camera for Raspberry PI'''
    def __init__(self):
        super(PiCamera, self).__init__()
        self.video_stream = PiCamera()
        self.frame = PiRGBArray(video_stream)

    def get_frame(self, size):
        return self.video_stream.capture(self.frame, format="bgr").array

    def stop(self):
        None


class WebCam(Camera):
    ''' Standard Webcam '''

    def __init__(self):
        super(WebCamera, self).__init__()
        video_stream = cv2.VideoCapture(0)
        time.sleep(1)   # Warm up
        if not video_stream.isOpened():
            raise Exception("Cannot open the camera")
        self.video_stream = video_stream

    def get_frame(self):
        video_stream = self.video_stream
        return video_stream.read()

    def stop(self):
        video_stream = self.video_stream
        video_stream.release()

if __name__ == "__main__":
    camera = WebCamera.get_instance()
    frame = camera.get_frame()[1]
    cv2.imshow("test", frame)
    camera.stop()
