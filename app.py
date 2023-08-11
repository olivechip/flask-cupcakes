from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, default_photo, Cupcake

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'apple_pie'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()

@app.route('/api/cupcakes')
def list_cupcakes():
    """Returns data on all cupcakes in JSON format"""
    cupcakes = Cupcake.query.all()
    serialized = [c.serialize_cupcake() for c in cupcakes]
    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
def cupcake_details(cupcake_id):
    """Returns data on a single cupcake in JSON format"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = [cupcake.serialize_cupcake()]
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Creates a cupcake from request body and displays its data in JSON format"""

    """good use of dictionary.get method below"""
    cupcake = Cupcake(flavor=request.json["flavor"], size=request.json["size"], rating=request.json["rating"], image=request.json.get("image"))
    db.session.add(cupcake)
    db.session.commit()

    serialized = [cupcake.serialize_cupcake()]
    return (jsonify(cupcake=serialized), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Updates a cupcake from request body and displays its data in JSON format"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json["size"]
    cupcake.rating = request.json["rating"]
    if not "image" in request.json:
        cupcake.image = default_photo
    else: 
        cupcake.image = request.json["image"]
    db.session.commit()

    serialized = [cupcake.serialize_cupcake()]
    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Deletes a cupcake and displays confirmation in JSON format"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    msg = f"Deleted {cupcake.flavor} cupcake"
    return jsonify(msg=msg)

@app.route('/')
def home():
    """Shows the home page"""
    return render_template('home.html')