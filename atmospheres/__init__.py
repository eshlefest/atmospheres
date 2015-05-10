from flask import Flask
from atmospheres.db.datastore import DataStore
from atmospheres.controller.web_service import app

app = Flask(__name__)
app.db = DataStore()





