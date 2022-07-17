import json
from sys import flags
from flask import Flask
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy
app = Flask('__name__', template_folder='./app/templates',static_folder='./app/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rozzos.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = "random string"


db  = SQLAlchemy(app)

from app.production import bp_production
from app.index import bp_index
from app.workers import bp_workers
from app.stats import bp_stats

app.register_blueprint(bp_production)
app.register_blueprint(bp_index)
app.register_blueprint(bp_workers)
app.register_blueprint(bp_stats)

with open('config.json') as config_file:
    config = json.load(config_file)
    
from app.models.inputs import *
from app.models.task import *
from app.models.worker import *

migrate = Migrate(app, db)



 
if __name__ == '__main__':
    app.run(debug=True)
