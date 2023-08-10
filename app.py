from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'apple_pie'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()