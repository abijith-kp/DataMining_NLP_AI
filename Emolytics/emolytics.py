from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from maps import Maps
from tweeter import tweeter
from sentiment import Sentiment

consumer_key=""
consumer_secret=""

access_token = ""
access_token_secret = ""

X_train = None
Y_train = None
tweet_map = None

def load_dataset():
    # dataset in csv file format
    data_file = ""
    # give the required colomn here
    RATING = 1
    TEXT = 3
    f = open(data_file)
    content = f.readlines()
    f.close()
    content = content[1:]
    X = []
    Y = []
    for c in content:
        t = c.split(",")
        X.append(t[TEXT])
        Y.append(int(t[RATING]))
    return (X, Y)


def create_classifier():
    dataset = load_dataset()
    X_train, Y_train = dataset
    classifier = Sentiment()
    classifier.fit(X_train, Y_train)
    return classifier


class StdOutListener(StreamListener):
    def __init__(self, tweet_map):
        self.tweet_map = tweet_map

    def on_data(self, status):
        self.tweet_map.fit(status)
        return True

    def on_error(self, error_code):
        print "Error: ", error_code

if __name__ == "__main__":
    classifier = create_classifier()
    tweet_map = Maps(classifier, tweeter)
    l = StdOutListener(tweet_map)
    
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    while True:
        try:
            stream.disconnect()
            stream.filter(locations=[-180,-90,180,90], languages=['en'])
        except Exception, e:
            print "Error: ", e
