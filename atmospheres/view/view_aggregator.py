from atmospheres import app
from atmospheres.db.datastore import DataStore
from atmospheres.aggregator.sentiment_aggregator import SentimenetAgrregator
from atmospheres.resources.sentiment import SentimentType
from atmospheres.controller.geo_json import sf_geo_json
from datetime import timedelta, datetime

import random
import json

from plotly.graph_objs import *
import plotly.plotly as py


aggregator = SentimenetAgrregator(app)

def get_sentiment_graph_url_by_zipcode(zipcode):
    x, y = get_time_series(zipcode,10,6)

    filename = "Sentiment-Graph-%s  %s"%(zipcode, datetime.now().ctime())
    url = get_plotly_time_series_url(x,y,filename)
    return url


def get_sf_graph_url():
    location = "sf"
    x, y = get_time_series(location,10,6)

    filename = "Sentiment-Graph-%s  %s"%(location,datetime.now().ctime())
    url = get_plotly_time_series_url(x,y,filename)
    return url


def get_time_series(zipcode,range_of_days,time_delta_hours):
    """
        generates a timeseries for a given zipcode from [now - range_of_days] to now
        at intervals of time_delta_hours
    """
    now = datetime.now()
    start = now - timedelta(days=range_of_days)
    datetimes = []
    sentiments = []
    zipcode = str(zipcode) if zipcode != "sf" else None

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



def get_sf_bar_graph_url():
    y = []

    now = datetime.now()
    five_days_ago = now - timedelta(days=5)
    for _zip in sf_zipcode_array:
        positive_count =  aggregator.get_sentiment_count(SentimentType.positive, _zip, five_days_ago,now)
        negative_count =  aggregator.get_sentiment_count(SentimentType.negative, _zip, five_days_ago,now)
        if positive_count == 0 and negative_count == 0:
            sentiment = 0
        else:
            sentiment = float(positive_count - negative_count) / float(positive_count + negative_count)

        y.append(sentiment)

    x = neighborhoods


    filename = "Zipcode-Bar-Graph  %s"%(datetime.now().ctime())
    url = get_plotly_zip_sentiment_series_url(x,y,filename)
    return url

def get_sentiments_json():
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

def get_plotly_time_series_url(x, y, filename):
    """
        This inputs data and spits out a scatter graph
        :param x: coordinates are datetimes
        :param y: coordinates are sentiments
    """
    data = Data([
                Scatter(
                         x=x,
                         y=y,
                         name='Average Sentiment Value',
                )
    ])

    # Adding legends, coordinate names, and titles to graph
    layout = Layout(
        title = filename,
        xaxis = XAxis(
            title = 'Dates',
            titlefont = Font(
                family = 'Courier New, monospace',
                size = 18
            )
        ),
        yaxis = YAxis(
            title = 'Sentiments',
            titlefont = Font(
                family = 'Courier New, monospace',
                size = 18
            )
        ),
    )

    figure = Figure(data=data, layout=layout)
    plot_url = py.plot(figure, filename=filename, auto_open=False)
    return plot_url 


    #This inputs data and spits out a bar graph
def get_plotly_zip_sentiment_series_url(x,y,filename):
    # x coordinates are Zipcodes
    # y coordinates are sentiments
    data = Data([
                Bar(
                    x=x,
                    y=y,
                    name='Sentiment Value by Zip')])
                #adding legends, coordinate names, and titles to graph
    layout = Layout(
                    title = filename,
                    xaxis = XAxis(
                        title = 'Zipcodes',
                        titlefont = Font(
                        family = 'Courier New, monospace',
                        size = 18)),
                    yaxis = YAxis(
                            title = 'Sentiments',
                            titlefont = Font(
                                family = 'Courier New, monospace',
                                size = 18)))
                 
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='atmospheres-Zip-Sentiment-series',auto_open=False)
    return plot_url  

