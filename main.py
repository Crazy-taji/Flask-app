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


@app.route('/')
def index():
    ret, __ = cv2.VideoCapture(1).read()
    if not ret:
        return render_template("index.html", val = "ret not worked")
    else:
        return render_template("index.html", val = "ret worked")

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
