from app import app
from models import db, connect_db, Cupcake, DEFAULT_URL
from unittest import TestCase

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db_test'
app.config['SQLALCHEMY_ECHO'] = False

db.create_all()

class CupcakesTestCase(TestCase):

    def setUp(self):
        """Things needed before every test"""

        Cupcake.query.delete()

        self.client = app.test_client()
        new_cupcake = Cupcake(id=10000,flavor='banana',size='smol',rating=8)
        db.session.add(new_cupcake)
        db.session.commit()

    def test_get_all_cupcakes(self):
        """Test to see if we can get all of the cupcakes"""
        response = self.client.get("/cupcakes")
        response_data = response.json['response']
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['flavor'], 'banana')
        self.assertEqual(response_data[0]['size'], 'smol')
        self.assertEqual(response_data[0]['rating'], 8)
        self.assertEqual(response_data[0]['image'], DEFAULT_URL)
        self.assertEqual(response.status_code, 200)

    def test_create_new_cupcake(self):
        """Test to see if we can create a new cupcake"""
        response = self.client.post("/cupcakes",
                                    json={"flavor":"sesame",
                                          "size":"large",
                                          "rating":7,
                                          })
        response_data = response.json['response']
        self.assertEqual(response_data['flavor'], 'sesame')
        self.assertEqual(response_data['size'], 'large')
        self.assertEqual(response_data['rating'], 7)
        self.assertEqual(response_data['image'], DEFAULT_URL)
        self.assertEqual(response.status_code, 200)

        get_response = self.client.get("/cupcakes")
        response_data = get_response.json['response']
        self.assertEqual(len(response_data), 2)
        self.assertEqual(get_response.status_code, 200)

    def test_update_all_cupcakes(self):
        """Test to see if we can update a cupcake"""
        response = self.client.patch("/cupcakes/10000",
                                     json={"flavor":"mint",
                                          "size":"tuple",
                                          "rating":6,
                                          })
        response_data = response.json['response']
        self.assertEqual(response_data, {"flavor":"mint",
                                          "size":"tuple",
                                          "rating":6,
                                          "id":10000,
                                          "image":DEFAULT_URL})
        self.assertEqual(response.status_code, 200)

        get_response = self.client.get("/cupcakes")
        response_data = get_response.json['response']
        self.assertEqual(len(response_data), 1)
        self.assertEqual(get_response.status_code, 200)

    def test_delete_all_cupcakes(self):
        """Test to see if we can delete a cupcake"""
        response = self.client.delete("/cupcakes/10000")
        response_data = response.json['message']
        self.assertEqual(response_data, 'Deleted')
        self.assertEqual(response.status_code, 200)

        get_response = self.client.get("/cupcakes")
        response_data = get_response.json['response']
        self.assertEqual(len(response_data), 0)
        self.assertEqual(get_response.status_code, 200)
