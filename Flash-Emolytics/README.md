Flash-Emolytics
================

Collects tweets using Tweepy library. There is a provision to give the keywords
and start a new search. The tweet stream is stored in MongoDB. The server API's
are implemented using flask framework, which gets th etweets from the database
at fixed time intervels and classify it using the sklearn library into positive
or negative sentiment. Later its mapped with the help of leaflet.js, and Mapbox.

Requirements:

* Python2.7

* Flask

* Leaflet.js

* MongoDB

* Tweepy

* Twitter Bootstrap

* Sklearn

* Mapbox
