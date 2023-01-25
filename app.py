from flask import Flask, render_template,request, Response, jsonify
import cv2
import time


from main import proceesor
import numpy as np
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

camTurn = True

def checkCam():
    camera = cv2.VideoCapture(camera_text)
    outcome,_ = camera.read()
    camera.release()
    if outcome:
        return True
    else:
        return False


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
    global camera
    global camera_text
    global current
    print(url)
    cam = cv2.VideoCapture(url)
    ret,_ = cam.read()
    if ret:
        camera_text = url
        camera = cv2.VideoCapture(camera_text)
        emit("response", "successfully loaded " + url)
        current = True

    else:
        current = False
        emit("response", "failed to load " + url)


camera_text = "http://86.34.190.86:88/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER"
number = 0

textLog = []

def generateFrames():
    global camTurn
    global number
    global camera
    global current
    # maximum = 600
    # percentage = 0.3
    camera = cv2.VideoCapture(camera_text)
    camera.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    frame_rate = 30
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
            outcome,frame = camera.read()
            if not camTurn:
                frame = cv2.imread("random.jpg")
                frame = cv2.resize(frame, (500, 320))
            if not outcome:
                frame = cv2.imread(camera_text)
                camera.release()
                # frame = np.zeros((500, 320, 3), dtype = np.uint8)
                frame = cv2.resize(frame, (500, 320))
            else:
                frame = cv2.resize(frame, (500, 320))
                frame,number = proceesor(frame)
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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


@app.route("/cam", methods = ["POST", "GET"])
def cam():
    result = request.form.to_dict()
    camNum = result["name"]
    print(camNum)
    cam_change(camNum)
    return render_template("index.html")

# @app.route("/photo")
# def photo():
#     if checkCam() is True:
#         return Response("working",mimetype='text' )
#     else:
#         return Response("not working",mimetype='text' )

@app.route('/send_text')
def send_text():
    def generate():
        yield str(number)
    return Response(generate(), mimetype='text')

if __name__ == "__main__":
    app.run(debug=True)


