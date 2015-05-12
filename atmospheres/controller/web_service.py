import os
from flask import render_template, request, send_from_directory, Response
from atmospheres import app
from atmospheres.view.view_aggregator import (
    get_sentiment_graph_url_by_zipcode,
    get_sentiments_json,
    get_sf_bar_graph_url,
    get_sf_graph_url,
)

@app.route('/')
def home():
    return render_template('geo_new.html')

# Get images from static folder
@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

@app.route('/old')
def home_old():
    return render_template('geo.html')

@app.route('/geo.js')
def geo_js():
    r = render_template('geo.js')
    return Response(r, mimetype='text/javascript')

@app.route('/leaflet-button.js')
def leaflet_button_js():
    r = render_template('leaflet-button.js')
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


@app.route('/data/live')
def get_sentiments_json_wrapper():
    return get_sentiments_json()


@app.route('/postdata/', methods=['POST'])
def store_post():
    # This method is expecting json object. When client sends the
    # json data, it should also sets the request header Content-Type
    # to application/json.
    # { 'mypostdata': { 'fname': 'kumari', 'lname': 'sweta'}}
    data = {"mypostdata": request.json}
    print data
    app.db.write(data)
    return 'Thank you for the data'


# place holder for later
@app.route('/data/zipcode/<zipcode>')
def get_sentiment_graph_url_by_zipcode_wrapper(zipcode):
    return get_sentiment_graph_url_by_zipcode(zipcode)


@app.route('/data/sf/timeseries')
def get_sf_graph_url_wrapper():
    return get_sf_graph_url()


@app.route('/data/sf/bar')
def get_sf_bar_graph_url_wrapper():
    return get_sf_bar_graph_url()


def main():
    app.run(debug=False)


if __name__ == "__main__":
    main()
