from flask import Flask, render_template, Response
from Imagery.Camera import *
from Imagery.MotionDetector import *
from Mail.MailService import *
from Mail.AutoMail import *
from Web.AppThread import *
import time

app = AppThread()
web_server = Flask(__name__)

@web_server.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        processed_img = app.get_last_processed_image()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + processed_img + b'\r\n')

@web_server.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def execute_server():
    # Launch thread for all the security stuff
    app.start()
    # Warm up
    time.sleep(1)
    # Execute webserver
    web_server.run(host='0.0.0.0', debug=True, use_reloader=False)
    app.stop()
