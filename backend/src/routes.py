from flask import Response, render_template, current_app as app, request, flash
from config import *
from src.camera import *


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/video_feed')
def video_feed():
    return Response(VideoCamera("backend\schoolfight.mp4")(), mimetype='multipart/x-mixed-replace; boundary=frame')