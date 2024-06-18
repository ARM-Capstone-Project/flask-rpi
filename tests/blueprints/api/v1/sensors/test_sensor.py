import unittest
import json
from flask import Flask, jsonify, request
from flask.testing import FlaskClient
from blueprints.api.v1.sensors import sensors_bp

class TestSensorsBlueprint(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(sensors_bp)
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_index_route(self):
        response = self.client.get('/api/v1/sensors/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'This endpoint should return a list of sensor records')

    def test_show_route(self):
        sensor_id = 1
        response = self.client.get(f'/api/v1/sensors/{sensor_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['id'], sensor_id)
        self.assertIn('message', data)
        self.assertEqual(data['message'], f'This endpoint should return a sensor {sensor_id} record')

    def test_create_route(self):
        data = {
            'some_key': 'some_value'
        }
        response = self.client.post('/api/v1/sensors/', json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'This endpoint should create a sensor record')

if __name__ == '__main__':
    unittest.main()
