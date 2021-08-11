from flask import Response, render_template, current_app as app, request, flash
from config import *
from src.camera import *
from pprint import pprint

# Gobal variable to store losses
LOSSES = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/done")
def done():
    return render_template("done.html")