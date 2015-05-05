from flask import Flask
from atmospheres.db.datastore import DataStore

app = Flask(__name__)
app.db = DataStore()


from atmospheres import controller  # noqa

