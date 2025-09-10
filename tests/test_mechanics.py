from app import create_app
from app.models import Mechanics, db
import unittest
from werkzeug.security import check_password_hash, generate_password_hash
from app.util.auth import encode_token


#Run Script: python -m unittest discover tests

class TestMechanics(unittest.TestCase):


    def setUp(self): 
        self.app = create_app('TestingConfig') 
        self.mechanic = Mechanics(password=generate_password_hash('password123'), first_name = 'jon', last_name = 'doe', email = 'jon@doe.com', salary = 100, address = '123 main street') 
        with self.app.app_context(): 
            db.drop_all() 
            db.create_all() 
            db.session.add(self.mechanic)
            db.session.commit()
        self.token = "Bearer "+encode_token(1) 
        self.client = self.app.test_client() 
    
    #test creating a mechanic (IMPORTANT all test functions need to start with test)
    def test_create_mechanic(self):
        mechanic_payload = {
            "first_name": "jane",
            "last_name": "doe",
            "email": "jane@doe.com",
            "password": "password123",
            "salary": 100.0,
            "address": "123 main street"
        }
        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(response.json['first_name'], "jane") # type: ignore 
        self.assertTrue(check_password_hash(response.json['password'], "password123")) # type: ignore


    #Negative check: See what happens when we intentionally try and break an endpoint
    def test_invalid_create(self):
        mechanic_payload = {
            "first_name": "jane",
            "last_name": "doe",
            "password": "password123",
            "salary": 100.0,
            "address": "123 main street"
        }
        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code,400)
        self.assertNotIn('email', response.json) # type: ignore 

    def test_nonunique_email(self):
        mechanic_payload = {
            "first_name": "jon",
            "last_name": "doe",
            "email": "jon@doe.com",
            "password": "password123",
            "salary": 100.0,
            "address": "123 main street"
        }
        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertEqual(response.status_code, 400)


    def test_get_mechanics(self):
        response = self.client.get('/mechanics')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['first_name'], 'jon') # type: ignore

    def test_login(self):
        login_creds = {
            "email": "jon@doe.com",
            "password": "password123"
        }

        response = self.client.post('/mechanics/login', json=login_creds)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json) # type: ignore


    def test_delete(self):
        headers = {"Authorization": self.token}

        response = self.client.delete("/mechanics/1", headers=headers) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Successfully deleted mechanic 1') # type: ignore


    def test_unauthorized_delete(self):
        response = self.client.delete("/mechanics/1") 
        self.assertEqual(response.status_code, 401) #Should get an error response

    
    def test_update(self):
        headers = {"Authorization": self.token}
        update_payload = {
            "first_name": "jon",
            "last_name": "doe",
            "email": "NEW_EMAIL@email.com",
            "password": "password123",
            "salary": 110.0,
            "address": "123 main street"
        }
        response = self.client.put('/mechanics/1', headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'NEW_EMAIL@email.com') # type: ignore




       

    
   

 

