from threading import Thread
from Imagery.Camera import *
from Imagery.MotionDetector import *
from Mail.AutoMail import *
from Mail.MailService import *
from Web.Server import *
import traceback

class AppThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.processed_img = None

    def prepare(self, user_data, detection_data, app_data, mail_to):
        self.camera = Camera.get_instance()
        blur_size = (detection_data["blur"], detection_data["blur"])
        self.motion_detector = MotionDetector(detection_data["min_threshold"], detection_data["max_threshold"], blur_size)
        self.mail_provider = MailService(user_data["email"], user_data["password"], user_data["address"], user_data["port"])
        self.auto_mail = AutoMail(self.mail_provider, user_data["email"], mail_to, app_data["timeout"])
        self.auto_mail_activation = app_data["auto_mail_activation"]

    def run(self):
        camera = self.camera
        motion_detector = self.motion_detector
        auto_mail = self.auto_mail
        while(self.running):
            frame = camera.get_frame()[1]
            if frame is not None:
                detection, processed_frame = motion_detector.process(frame)
                processed_img = motion_detector.convert_jpeg(processed_frame)
                self.processed_img = processed_img
                if self.auto_mail_activation and detection:
                    auto_mail.connect()
                    auto_mail.process(processed_img)

    def get_last_processed_image(self):
        return self.processed_img

    def stop(self):
        self.running = False
