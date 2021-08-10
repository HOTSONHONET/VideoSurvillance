from flask import Flask, render_template, redirect, current_app as app, request, flash
from config import *


@app.route("/")
def home():
    return render_template("index.html")