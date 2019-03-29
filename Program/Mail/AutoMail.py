import time

class AutoMail():
    def __init__(self, mail_provider, mail_from, mail_to, timeout):
        self.mail_provider = mail_provider
        self.mail_from = mail_from
        self.mail_to = mail_to
        self.timeout = timeout
        self.images_bank = []
        self.start_time = None

    def add_image(self, img):
        self.images_bank.append(img)

    def process(self, img):
        # Launch timer and avoid sending email during x seconds
        if self.start_time is None:
            self.start_time = time.time()
            #self.add_image(img)
            self.mail_provider.send("AutoMail - Detection", self.mail_from, self.mail_to, "Catched something...", img)
        elapsed_time = time.time() - self.start_time
        # Reset
        if elapsed_time > self.timeout:
            self.start_time = None
