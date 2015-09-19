from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import string
import matplotlib.cm as cm
import random
import json
import pprint
import time

class Maps:
    def __init__(self, classifier, tweet_processer):
        self.x = []
        self.y = []
        self.px = None
        self.py = None
        self.color_map = {0: "red", 1: "green"}

        self.datapoint = []
        self.classifier = classifier
        self.tweet_processer = tweet_processer
        self.m = Basemap(projection='robin',lon_0=-50,lat_0=60,resolution='l')
        plt.title("Emolytics")
        self.m.drawmapboundary(fill_color='black') # fill to edge
        self.m.drawcountries()
        self.m.fillcontinents(color='white',lake_color='black',zorder=0)
        plt.plot()
        plt.pause(0.0001)

    def _update_map():
        pass

    def fit(self, T):
        t = json.loads(T)
        pprint.pprint(t)
        lat, lon = self.tweet_processer(T)
        print "Coordinates: ", lat, lon
        dp = self.classifier.predict(t["text"])
        print "(", t["text"], ", ", dp, ")"
        self.x.append(lat)
        self.y.append(lon)
        self.datapoint.append(dp)
        tmp = self.m(lat, lon)

        self.x.append(tmp[0])
        self.y.append(tmp[1])

        color_name = [self.color_map.get(i[0])    for i in self.datapoint]
        print color_name[-1]
        self.m.scatter(self.x, self.y, marker="o", c=color_name, alpha=0.7)
        self.m.drawmapboundary(fill_color='black') # fill to edge
        self.m.drawcountries()
        self.m.fillcontinents(color='white',lake_color='black',zorder=0)
        plt.draw()
        plt.pause(0.0001)
