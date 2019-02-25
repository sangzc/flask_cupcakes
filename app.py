from flask import Flask, jsonify, request
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/cupcakes')
def get_list_of_cupcakes():
    ''' retrieve data from cupcake db and return JSON resembling:
    {"id": 1, "flavor": chocolate, "size": Large, "rating": 4.3, "image": url}'''

    cupcakes_list = Cupcake.query.all()

    serialized_cupcakes = [
        {'id': cupcake.id,
         'flavor': cupcake.flavor,
         'size': cupcake.size,
         'rating': cupcake.rating,
         'image': cupcake.image}
        for cupcake in cupcakes_list
    ]

    return jsonify(response=serialized_cupcakes)


@app.route('/cupcakes', methods=["POST"])
def create_cupcake():
    ''' make a new cupcake record with incoming data. Return newly
        JSON string of the cupcake
        {"id": 1, "flavor": chocolate, "size": Large, "rating": 4.3, "image": url} '''

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json.get('image') or None

    new_cupcake = Cupcake(flavor=flavor,
                          size=size,
                          rating=rating,
                          image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    cupcake = Cupcake.query.get(new_cupcake.id)

    serialized_cupcake = {'id': cupcake.id,
                          'flavor': cupcake.flavor,
                          'size': cupcake.size,
                          'rating': cupcake.rating,
                          'image': cupcake.image}

    return jsonify(response=serialized_cupcake)

    