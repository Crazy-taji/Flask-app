from flask import Flask, render_template, Response, Request
import os
from func import processor
import cv2
import numpy as np

app = Flask(__name__)

camera_text = 1
number = 0

textLog = []
current = ""
cancel = False

def generateFrames():
    global number
    global camera
    global current
    global cancel
    
    if not cancel:
        camera = cv2.VideoCapture(camera_text)
        
    while True:
        if not canccel:
            current = "camera capturing properly"
            outcome, frame = camera.read()
            
            if not outcome:
                current = "camera not capturing"
                camera.release()
                frame = np.zeros((500, 320, 3), dtype = np.uint8)
                frame = cv2.resize(frame, (500, 320))
                
            else:
                frame = cv2.resize(frame, (500, 320))
                frame,number = proceesor(frame)
                
        if cancel:
            camera.release()
            frame = np.ones((500, 320, 3), dtype = np.uint8) * 230
            frame = cv2.resize(frame, (500, 320))

        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/')
def index():
    global cancel
    cancel = False
    ret, __ = cv2.VideoCapture(1).read()
    if not ret:
        return render_template("index.html", val = "ret not worked")
    else:
        return render_template("index.html", val = "ret worked")

@app.route('/video')
def video():
    return Response(generateFrames(x),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/cancel", methods = ["POST", "GET"])
def cam():
    global camera
    global cancel
    result = request.form.to_dict()
    value = result["post"]
    if value is "cancel":
        cancel = True
    return ""

    
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
