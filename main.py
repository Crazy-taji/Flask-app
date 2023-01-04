from flask import Flask, render_template, Response, Request
import os
import func
import cv2

app = Flask(__name__)

number = 13

@app.route('/')
def index():
    ret, __ = cv2.VideoCapture(0).read()
    if not ret:
        return render_template("index.html", val = "ret not worked")
    else:
        return render_template("index.html", val = "ret worked")


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
