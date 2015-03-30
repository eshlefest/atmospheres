from flask import Flask, request, url_for, send_from_directory
from atmospheres.ingestion.mongoreader import MongoReader


app = Flask(__name__)
app.mongoreader = MongoReader()

@app.route('/')
def hello_world():
    f = open("server/static/geo.html")
    return f.read()


@app.route('/postdata/', methods=['POST'])
def store_post():
    # This method is expecting json object. When client sends the
    # json data, it should also sets the request header Content-Type 
    # to application/json.
    data = { "mypostdata": request.json }
    print data
    app.mongoreader.write(data)
    return 'Thank you for the data'


def main():
    
    app.run(debug=True)
