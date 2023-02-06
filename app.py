from flask import Flask, render_template,request, Response, jsonify
import cv2
import time

from main import proceesor, motionDetect
import numpy as np
from flask_socketio import SocketIO, send, emit
from imutils.video import VideoStream

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
camTurn = True
process = 0

def checkCam():
    cam = cv2.VideoCapture(camera_text)
    outcome,_ = cam.read()
    cam.release()
    if outcome:
        return True
    else:
        return False

@socketio.on("model")
def model_handle(val):
    global process
    process = val
    print("model set")
    print(process)


@socketio.on("connect")
def handle_my_data():
    print("Connected!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

@socketio.on("cam")
def handle_my_data(cam):
    print("got")
    global camTurn
    if camTurn:
        val = False
        print("0")
    else:
        val = True
        print("1")
    camTurn = val



@socketio.on("url")
def url(url):
    global camera_text
    global current
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


camera_text = "http://80.32.125.254:8080/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER"
number = 0

textLog = []

def generateFrames():
    global camTurn
    global number
    global camera
    global current
    global process
    # maximum = 600
    # percentage = 0.3
    SetCam()
    frame_rate = 1
    prev = 0
    print("image requested")
    # while frame[1] > maximum or frame[0] > maximum:
    #     frame[1] = round(frame[1]*percentage)
    #     frame[0] = round(frame[0] * percentage)
    # width = frame[1] * percentage
    # height = frame[0] * percentage
    while True:
        if not camTurn:
            frame = cv2.imread("random.jpg")
            frame = cv2.resize(frame, (500, 320))
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        if camTurn:
            frame = camera.read()
            if frame is None:
                frame = cv2.imread("no_video.jpg")
                camera.release()
                # frame = np.zeros((500, 320, 3), dtype = np.uint8)
                frame = cv2.resize(frame, (500, 320))
            else:
                frame = cv2.resize(frame, (500, 320))
                if int(process) == 1:
                    frame,number = proceesor(frame)
                if int(process) == 2:
                    frame, number = motionDetect(frame)
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def SetCam():
    global camera_text
    global camera
    camera = video_stream = VideoStream(camera_text).start()

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
    while True:
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
        global process
        global number
        if process == 0:
            yield "Turn On Processor"
        else:
            yield str(number)
            print(number)
    return Response(generate(), mimetype='text')

if __name__ == "__main__":
    app.run(debug=True)


