import unittest
import json
from flask import Flask, jsonify, Blueprint, request
from flask.testing import FlaskClient
from unittest.mock import patch, MagicMock
from blueprints.api.v1.sensors.temperature import temperature_bp
from controllers.api.v1.sensors.temperature import TemperatureController

class TestTemperatureBlueprint(unittest.TestCase):

    def setUp(self):
        # Create a Flask test client
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Mocking the TemperatureController methods
        self.mock_controller = MagicMock(spec=TemperatureController)
        self.mock_controller.get_all_records.return_value = [
            {'id': 1, 'temperature': 25.5},
            {'id': 2, 'temperature': 26.0}
        ]
        self.mock_controller.get_single_record.return_value = {'id': 1, 'temperature': 25.5}
        self.mock_controller.create_record.return_value = {'id': 1, 'temperature': 25.5}

        self.app.register_blueprint(temperature_bp)

    def test_index_route(self):
        # Test GET /temperature/
        response = self.client.get('/temperature/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'This endpoint should return a list of temperature sensor records')
        self.assertIn('data', data)
        self.assertEqual(len(data['data']), 2)

    def test_show_route(self):
        sensor_id = 1
        response = self.client.get(f'/temperature/{sensor_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['id'], sensor_id)
        self.assertIn('message', data)
        self.assertEqual(data['message'], f'This endpoint should return a sensor {sensor_id} record')

    def test_create_route(self):
        data = {'temperature': 25.5}
        response = self.client.post('/temperature/', json=data)
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'This endpoint should create a sensor record')
        self.assertIn('body', response_data)
        print(response_data)
        self.assertEqual(response_data['body']['id'], 1)

    def test_create_route_missing_data(self):
        response = self.client.post('/temperature/', json={})
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data.decode('utf-8'))
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Missing required data')

    # def test_error_handling(self):
    #     # Mocking an exception in TemperatureController methods
    #     self.mock_controller.get_all_records.side_effect = Exception('Mocked error')
    #
    #     # Test error handling in GET /temperature/
    #     response = self.client.get('/temperature/')
    #     self.assertEqual(response.status_code, 500)
    #     response_data = json.loads(response.data.decode('utf-8'))
    #     self.assertIn('error', response_data)
    #     self.assertEqual(response_data['error'], 'Mocked error')

if __name__ == '__main__':
    unittest.main()
