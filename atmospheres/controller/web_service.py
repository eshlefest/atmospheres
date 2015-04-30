import os

from flask import render_template, request, send_from_directory, Response

from atmospheres import app
from atmospheres.db.datastore import DataStore
from atmospheres.controller.geo_json import sf_geo_json
from atmospheres.aggregator.sentiment_aggregator import SentimenetAgrregator
from atmospheres.resources.sentiment import SentimentType
from datetime import timedelta, datetime
import random
import json

from plotly.graph_objs import *
import plotly.plotly as py

app.db = DataStore()
aggregator = SentimenetAgrregator(app)

@app.route('/')
def home():
    #import pdb; pdb.set_trace()
    #result = render_template('geo_new.html') 
    return render_template('geo_new.html')
    #return result

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/about.css')
def about_css():
    r = render_template('about.css')
    return Response(r, mimetype='text/css')

@app.route('/old')
def home_old():
    return render_template('geo.html')


@app.route('/geo.js')
def geo_js():
    r = render_template('geo.js')
    return Response(r, mimetype='text/javascript')

@app.route('/geo.css')
def geo_css():
    r = render_template('geo.css')
    return Response(r, mimetype='text/css')


@app.route('/angular.min.js')
def geo_angular():

    return render_template('angular.min.js')

@app.route('/bootstrap.min.css')
def geo_bootstrap():

    return render_template('bootstrap.min.css')

@app.route('/angular.min.js.map')
def geo_angular_map():

    return render_template('angular.min.js.map')

@app.route('/static/sf_zips.topo.json')
def get_topo_json():
   return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'sf_zips.topo.json',
    )

@app.route('/data/sentiments')
def get_live_sentiments_json():
   return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'demo_sentiments.json',
    )

@app.route('/data/random')
def get_random_sentiments_json():
    data = sf_geo_json
    aggregator = SentimenetAgrregator(app)
    for item in sf_geo_json["features"]:
        zipcode = item['id']
        positive_count =  aggregator.get_sentiment_count(SentimentType.positive, zipcode, datetime.now() - timedelta(days=10) ,datetime.now())

        negative_count =  aggregator.get_sentiment_count(SentimentType.negative, zipcode, datetime.now() - timedelta(days=10) ,datetime.now())

        if positive_count == 0 and negative_count == 0:
            item["sentiment"] = 1
        else:
            item["sentiment"] = float(positive_count - negative_count) / float(positive_count + negative_count)
        print "zipcode:" + zipcode + "positive" + str(positive_count), str(negative_count),  str(item["sentiment"])   
    aggregated_result = json.dumps(data)
    return aggregated_result

@app.route('/postdata/', methods=['POST'])
def store_post():
    # This method is expecting json object. When client sends the
    # json data, it should also sets the request header Content-Type
    # to application/json.
    data = { "mypostdata": request.json }  # { 'mypostdata': { 'fname': 'kumari', 'lname': 'sweta'}}
    print data
    app.db.write(data)
    return 'Thank you for the data'

# place holder for later
@app.route('/data/zipcode/<zipcode>')
def get_graph_url(zipcode):
    return "https://plot.ly/~ryaneshleman/46.embed"



def getTimeSeries_tmp(zipcode,range_of_days,time_delta_hours):
    """
        this generates a random time series for testing
    """
    now = datetime.now()
    start = now - timedelta(days=range_of_days)
    datetimes = []

    while start < now:
        start += timedelta(hours=time_delta_hours)
        datetimes.append(start)

    sentiments = [random.random() for i in datetimes]

    return datetimes,sentiments


def getTimeSeries(zipcode,range_of_days,time_delta_hours):
    """
        generates a timeseries for a given zipcode from [now - range_of_days] to now
        at intervals of time_delta_hours
    """
    now = datetime.now()
    start = now - timedelta(days=range_of_days)
    datetimes = []
    sentiments = []

    # generates time intervals
    while start < now:
        start += timedelta(hours=time_delta_hours)
        datetimes.append(start)

    
    # for each interval, get positive and negative tweets
    # sentiment = positive - negative / (positive + negative)
    # store sentiment in sentiments array
    for i in range(len(datetimes)-1):
        positive_count =  aggregator.get_sentiment_count(SentimentType.positive, zipcode, datetimes[i],datetimes[i+1])
        negative_count =  aggregator.get_sentiment_count(SentimentType.negative, zipcode, datetimes[i],datetimes[i+1])
        if positive_count == 0 and negative_count == 0:
            sentiment = 0
        else:
            sentiment = float(positive_count - negative_count) / float(positive_count + negative_count)

        sentiments.append(sentiment)

    return datetimes,sentiments



def getPlotlyURL(x,y):
    
    data = Data([
                 Scatter(
                         x=x,
                         y=y
                         )
                 ])
    plot_url = py.plot(data, filename='atmospheres-time-series')
    return plot_url



def main():
    app.run(debug=True)



if __name__=="__main__":
    main()
