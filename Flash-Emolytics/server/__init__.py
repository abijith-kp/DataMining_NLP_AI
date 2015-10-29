from flask import Flask
from pymongo import MongoClient
from tweepy import OAuthHandler

consumer_key=""
consumer_secret=""

access_token = ""
access_token_secret = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

emolytics = Flask("emolytics", template_folder="/path/to/templates/", static_folder="/path/to/static/", static_url_path="")

client = MongoClient()
db = client.emolytics
