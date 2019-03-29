from flask import Flask, render_template, Response
from Imagery.Camera import *
from Imagery.MotionDetector import *
from Mail.MailService import *
from Mail.AutoMail import *
import time

app = Flask(__name__)

camera = Camera.get_instance()
motion_detector = MotionDetector()
mail_provider = MailService("Gerard@MonMail", "TasRellementCru?", 'smtp.gmail.com', 465)
auto_mail = AutoMail(mail_provider, "Gerard@MonMail", "Germaine@SonMail", 10)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()[1]
        detection, processed_frame = motion_detector.process(frame)
        processed_img = motion_detector.convert_jpeg(processed_frame)
        if detection:
            auto_mail.process(processed_img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + processed_img + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

def execute_server():
    app.run(host='0.0.0.0', debug=True)
