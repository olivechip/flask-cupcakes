from unittest import TestCase

from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5.0,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 1.0,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")
            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5.0,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_cupcake_details(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"

            resp = client.get(url)
            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcake": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5.0,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })
    
    def test_cupcake_details_404(self):
        with app.test_client() as client:
            bad_url = f"/api/cupcakes/0"
            bad_resp = client.get(bad_url)
            self.assertEqual(bad_resp.status_code, 404)

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"

            resp = client.post(url, json=CUPCAKE_DATA_2)
            self.assertEqual(resp.status_code, 201)

            # don't know what ID we'll get, make sure it's an int & normalize
            data = resp.json
            self.assertIsInstance(data["cupcake"][0]["id"], int)
            del data["cupcake"][0]["id"]

            self.assertEqual(data, {
                "cupcake": [{
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 1.0,
                    "image": "http://test.com/cupcake2.jpg"
                }]
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            
            resp = client.patch(url, json=CUPCAKE_DATA_2)
            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcake": [{
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 1.0,
                    "image": "http://test.com/cupcake2.jpg"
                }]
            })

    def test_update_cupcake_404(self):
        with app.test_client() as client:
            bad_url = f"/api/cupcakes/0"
            bad_resp = client.patch(bad_url, json=CUPCAKE_DATA_2)
            self.assertEqual(bad_resp.status_code, 404)

    def test_delete_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)
            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertIn("msg", data)

            bad_url = f"/api/cupcakes/0"
            bad_resp = client.get(bad_url)
            self.assertEqual(bad_resp.status_code, 404)

    def test_delete_cupcake_404(self):
        with app.test_client() as client:
            bad_url = f"/api/cupcakes/0"
            bad_resp = client.delete(bad_url)
            self.assertEqual(bad_resp.status_code, 404)