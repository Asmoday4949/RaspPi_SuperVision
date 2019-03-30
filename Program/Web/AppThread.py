from threading import Thread
from Imagery.Camera import *
from Imagery.MotionDetector import *
from Mail.AutoMail import *
from Mail.MailService import *
from Web.Server import *

class AppThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.processed_img = None

    def prepare(self, user_data, detection_data, mail_to, timeout):
        self.camera = Camera.get_instance()
        blur_size = (detection_data["blur"], detection_data["blur"])
        self.motion_detector = MotionDetector(detection_data["min_threshold"], detection_data["max_threshold"], blur_size)
        self.mail_provider = MailService(user_data["email"], user_data["password"], user_data["address"], user_data["port"])
        self.auto_mail = AutoMail(self.mail_provider, user_data["email"], mail_to, timeout)

    def run(self):
        camera = self.camera
        motion_detector = self.motion_detector
        auto_mail = self.auto_mail
        while(self.running):
            frame = camera.get_frame()[1]
            detection, processed_frame = motion_detector.process(frame)
            processed_img = motion_detector.convert_jpeg(processed_frame)
            self.processed_img = processed_img
            if detection:
                auto_mail.process(processed_img)

    def get_last_processed_image(self):
        return self.processed_img

    def stop(self):
        self.running = False
