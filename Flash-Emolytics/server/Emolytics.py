from server import db
from server import emolytics
from twitter import start_thread, start_classification

from flask import jsonify, render_template, request

import os
import random
from flask import jsonify

@emolytics.route("/", methods=["GET"])
def index():
    # return jsonify("Welcome to Flask-Emolytics")
    return "Welcome to Flask-Emolytics"

@emolytics.route("/analytics", methods=["POST", "GET"])
def analytics():
    try:
        track = request.get_json(force=True)
        track = map(unicode.strip, track["text"].split(","))
        start_thread(track=track)
        start_classification()
    except:
        pass
    return str(track)

@emolytics.route("/classify", methods=["POST"])
def classify():
    pass

@emolytics.route("/maps", methods=["GET"])
def maps():
    return render_template("emolytics.html")

# For testing purposes
@emolytics.route("/point", methods=["GET"])
def point():
    result = db.sentiment.find_one_and_update({'flag': {'$exists': False}}, {'$set': {'flag': True}})
    lat = 0.0
    lon = 0.0
    color = ""
    try:
        lat = result["pos"]["coordinates"][0]
        lon = result["pos"]["coordinates"][1]
        color = result["color"]
    except:
        pass
    return jsonify({"lat": lat, "lon": lon, "color": color})
