from server import db
from server import auth
from classifier import create_classifier

from tweepy import Stream
from tweepy.streaming import StreamListener

import json
import random
from multiprocessing import Process

process = None
clf_process = None
CLF = None

def get_document(status):
    status = json.loads(status)
    lat = 0.0
    lon = 0.0
    try:
        lon, lat = status["place"]["bounding_box"]["coordinates"][0][0]
    except:
        pass
    return {"tweet": status["text"], "pos": {"type": "Point", "coordinates": [lat, lon]}}

class StdOutListener(StreamListener):
    def on_data(self, status):
        try:
            doc = get_document(status)
            if doc["pos"]["coordinates"] != [0, 0]:
                db.tweets.insert_one(doc)
        except:
            pass
        return True

    def on_error(self, error_code):
        print "Error: ", error_code

def start_streaming(track=[""], locations=[-180,-90,180,90], languages=["en"]):
    l = StdOutListener()
    stream = Stream(auth, l)
    while True:
        try:
            stream.disconnect()
            stream.filter(track=track, locations=locations, languages=languages)
        except Exception, e:
            print "Exception: ", e

def classify():
    global CLF

    CLF = create_classifier()
    c = {0: "green", 1: "red"}

    while True:
        result = db.tweets.find_one_and_update({'flag': {'$exists': False}}, {'$set': {'flag': True}})
        try:
            r = CLF.predict(result["tweet"])
            result["color"] = c[r[0]]
            db.sentiment.insert_one(result)
        except Exception, e:
            pass

def start_thread(track):
    global process
    if process != None and process.is_alive():
        process.terminate()
    process = Process(target=start_streaming, kwargs={"track": track})
    process.start()
    print "Started the thread"

def start_classification():
    global clf_process

    if clf_process != None and clf_process.is_alive():
        clf_process.terminate()
    clf_process = Process(target=classify)
    clf_process.start()
    print "Started classification"
