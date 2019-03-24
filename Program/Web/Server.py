from flask import Flask, render_template, Response
from .CameraThread import *
import time

app = Flask(__name__)
#camera_thread = CameraThread()
camera = Camera.get_instance()
motion_detector = MotionDetector()

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()[1]
        processed_img = motion_detector.process_and_convert_jpeg(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + processed_img + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

def execute_server():
    app.run(host='0.0.0.0', debug=True)
