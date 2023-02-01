from flask import Flask, render_template,request, Response, jsonify
import cv2
import time
import threading


from main import proceesor
import numpy as np
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

camTurn = True
process = 0
change = False

def checkCam():
    camera = cv2.VideoCapture(camera_text)
    outcome,_ = camera.read()
    camera.release()
    if outcome:
        return True
    else:
        return False

class VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.lock = threading.Lock()
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()

    # grab frames as soon as they are available
    def _reader(self):
        while True:
            with self.lock:
                ret = self.cap.grab()
            if not ret:
                break

    # retrieve latest frame
    def read(self):
        with self.lock:
            _, frame = self.cap.retrieve()
        return frame

@socketio.on("model")
def model_handle(val):
    global process
    process = val
    print("model set")


@socketio.on("connect")
def handle_my_data():
    print("Connected!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

@socketio.on("cam")
def handle_my_data(cam):
    print("got")
    global camTurn
    global change
    if camTurn:
        val = False
        print("0")
    else:
        val = True
        print("1")
    camTurn = val
    change = True



@socketio.on("url")
def url(url):
    global camera_text
    global current
    global change
    print(url)
    cam = cv2.VideoCapture(url)
    ret,_ = cam.read()
    cam.release()
    if ret:
        camera_text = url
        SetCam()
        emit("response", "successfully loaded " + url)
        current = True
    else:
        current = False
        emit("response", "failed to load " + url)
    change = True


camera_text = "http://80.32.125.254:8080/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER"
number = 0

textLog = []

def generateFrames():
    global camTurn
    global number
    global camera
    global current
    global change
    # maximum = 600
    # percentage = 0.3
    SetCam()
    frame_rate = 5
    prev = 0
    print("image requested")
    # while frame[1] > maximum or frame[0] > maximum:
    #     frame[1] = round(frame[1]*percentage)
    #     frame[0] = round(frame[0] * percentage)
    # width = frame[1] * percentage
    # height = frame[0] * percentage
    while True:
        time_elapsed = time.time() - prev
        if time_elapsed > 1. / frame_rate:
            prev = time.time()
            if not camTurn:
                if change:
                    camera.release()
                    change = False
                frame = cv2.imread("random.jpg")
                frame = cv2.resize(frame, (500, 320))
            if camTurn:
                if change:
                    SetCam()
                    change = False
                frame = camera.read()
                # frame = cv2.resize(frame, (500, 320))
                if process == 1:
                    frame,number = proceesor(frame)
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def SetCam():
    global camera_text
    global camera
    camera = VideoCapture(camera_text)

def cam_change(num):
    global camera
    global camera_text
    global textLog
    textLog.append(num)
    if num.isdigit():
        num = int(num)
    camera_text = num
    camera.release()



@app.route('/', methods=["GET"])
def index():
    return render_template("index.html", val="ret not worked")
    # ret, __ = cv2.VideoCapture(1).read()
    # if not ret:
    #     return render_template("index.html", val = "ret not worked")
    # else:
    #     return render_template("index.html", val = "ret worked")


@app.route('/video')
def video():
    return Response(generateFrames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/checking")
def checking():
    return Response(current, mimetype='text')

# @app.route('/time_feed')
# def time_feed():
#     def generate():
#         yield datetime.now().strftime("%Y.%m.%d|%H:%M:%S")  # return also will work
#     return Response(generate(), mimetype='text')

# @app.route("/photo")
# def photo():
#     if checkCam() is True:
#         return Response("working",mimetype='text' )
#     else:
#         return Response("not working",mimetype='text' )

@app.route('/send_text')
def send_text():
    def generate():
        if process == 0:
            yield "Turn On Processor"
        else:
            yield str(number)
    return Response(generate(), mimetype='text')

if __name__ == "__main__":
    app.run(debug=True)


