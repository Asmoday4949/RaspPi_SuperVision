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
        self.camera = Camera.get_instance()
        self.motion_detector = MotionDetector()
        self.mail_provider = MailService("malik.fleury@gmail.com", "Avantasia4949", 'smtp.gmail.com', 465)
        self.auto_mail = AutoMail(self.mail_provider, "malik.fleury@gmail.com", "malik.fleury@gmail.com", 10)
        self.processed_img = None

    def run(self):
        camera = self.camera
        motion_detector = self.motion_detector
        auto_mail = self.auto_mail
        while(self.running):
            frame = camera.get_frame()[1]
            detection, processed_frame = motion_detector.process(frame)
            processed_img = motion_detector.convert_jpeg(processed_frame)
            self.processed_img = processed_img
            #if detection:
            #    auto_mail.process(processed_img)

    def get_last_processed_image(self):
        return self.processed_img

    def stop(self):
        self.running = False
