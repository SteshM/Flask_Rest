from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
# Init app
app = Flask(__name__)
 # Run Server
if __name__== '_main_':
  app.run(debug=True)

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path. join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init na
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
  id = db.Column(db.String(100), primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db. Integer)

  def __init__(self,name,description,price,qty):
     self.name = name
     self.deseription = description
     self.price = price
     self.qyt = qty

 



  
