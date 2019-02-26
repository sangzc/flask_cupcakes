from flask import Flask, jsonify, request, render_template
from models import db, connect_db, DEFAULT_URL, Cupcake


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

    serialized_cupcake = {'id': new_cupcake.id,
                          'flavor': new_cupcake.flavor,
                          'size': new_cupcake.size,
                          'rating': new_cupcake.rating,
                          'image': new_cupcake.image}

    return jsonify(response=serialized_cupcake)


@app.route('/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    ''' update cupcake with id passed into URL; respond with dictionary
    cf. {"id": 1, "flave": text, "size": text, "rating": 10.3, "image":text}'''

    cupcake = Cupcake.query.get(cupcake_id)

    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json.get('image') or DEFAULT_URL

    db.session.commit()

    serialized_cupcake = {'id': cupcake.id,
                          'flavor': cupcake.flavor,
                          'size': cupcake.size,
                          'rating': cupcake.rating,
                          'image': cupcake.image}

    return jsonify(response=serialized_cupcake)


@app.route('/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_that_cupcake(cupcake_id):
    ''' delete cupcake with id passed into URL: respond with dict
    cf. {"message": "Deleted"}'''

    cupcake = Cupcake.query.get(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")


@app.route('/')
def show_list_of_cupcakes():

    return render_template('index.html')
