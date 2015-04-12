import os

from flask import render_template, request, send_from_directory

from atmospheres import app
from atmospheres.ingestion.mongoreader import MongoReader



app.mongoreader = MongoReader()

@app.route('/')
def home():
    return render_template('geo.html')

@app.route('/static/sf_zips.topo.json')
def get_topo_json():
   return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'sf_zips.topo.json',
    )

@app.route('/postdata/', methods=['POST'])
def store_post():
    # This method is expecting json object. When client sends the
    # json data, it should also sets the request header Content-Type 
    # to application/json.
    data = { "mypostdata": request.json }  # { 'mypostdata': { 'fname': 'kumari', 'lname': 'sweta'}}
    print data
    app.mongoreader.write(data)
    return 'Thank you for the data'


def main():
    app.run(debug=True)



if __name__=="__main__":
    main()
