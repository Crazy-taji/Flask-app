from flask import Flask, render_template, Response, Request
import os
import cv2

app = Flask(__name__)

number = 13

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/send_text')
def send_text():
    def generate():
        global number
        yield str(number)
    return Response(generate(), mimetype='text')


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
