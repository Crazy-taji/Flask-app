from flask import Flask, render_template, Response, Request
import os
import func

app = Flask(__name__)

number = 13

@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
