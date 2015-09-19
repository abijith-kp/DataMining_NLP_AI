import json

def tweeter(tweet):
    status = json.loads(tweet)
    lat = 0.0
    lon = 0.0
    #if status.coordinates is not None:
    #    lat, lon = status.coordinates['coordinates']
    #else:
    #    lat, lon = status["place"]["bounding_box"]["coordinates"][0][0]
    lat, lon = status["place"]["bounding_box"]["coordinates"][0][0]
    return (lat, lon)
