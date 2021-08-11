from flask import Response, render_template, current_app as app, request, flash
from werkzeug.utils import redirect, secure_filename
from config import *
from src.camera import *
from pprint import pprint
from glob import glob

# Gobal variable to store losses
LOSSES = []


"""
Cleaner helper functions

"""
def cleanPrevUpload():
    images = glob(SAVE_IMG_PATH + "/" + "*.jpg")
    for img in images:
        os.remove(img)
    print("[INFO]  Removed all previous images")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/done")
def done():
    return render_template("done.html")


@app.route("/handle-video", methods = ['POST'])
def handle_video():

    video = request.files['video']
    pprint(request.files)
    print(f"[INFO] Video : {video}")
    video_name = secure_filename(video.filename)

    print(f"[INFO] Video name : {video_name}")
    print("[INFO] Saving video...")
    video.save(os.path.join(UPLOAD_PATH, video_name))


    return redirect("/upload-done")


@app.route("/upload-done")
def upload_done():
    video_path = glob(UPLOAD_PATH + '/' + '*.mp4')[0]

    cleanPrevUpload()

    cam = VideoCamera(video_path)
    
    cam.predict()
    losses = cam.giveLosses()
    cam.generateVideo()
    print(losses)
    return redirect("/watch")

@app.route("/watch")
def watch():
    return render_template("watch.html", video_path = SAVE_IMG_PATH + "/" + "done.mp4")
