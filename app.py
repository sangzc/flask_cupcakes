from flask import Flask, jsonify
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

