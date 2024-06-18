from flask import Blueprint
from flask import request
from flask import jsonify
from controllers.api.v1.sensors.temperature import TemperatureController

temperature_bp = Blueprint('temperature', __name__, url_prefix='/temperature')

@temperature_bp.route('/', methods=['GET'])
def index():
    try:
        temperatures = TemperatureController.get_all_records()
        return jsonify(
            {
                'message': 'This endpoint should return a list of temperature sensor records',
                'method': request.method,
                'data': temperatures
            }
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@temperature_bp.route('/<int:sensor_id>', methods=['GET'])
def show(sensor_id):
    try:
        temperature = TemperatureController.get_single_record(sensor_id)
        if temperature is None:
            return jsonify({'error': 'Temperature sensor not found'}), 404
        return jsonify({
            'id': sensor_id,
            'message': 'This endpoint should return a sensor {} record'.format(sensor_id),
            'method': request.method,
            'data': temperature
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@temperature_bp.route('/', methods=['POST'])
def create():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Missing required data'}), 400

        new_temperature = TemperatureController.create_record(data)
        return jsonify({
            'message': 'This endpoint should create a sensor record',
            'method': request.method,
            'body': new_temperature
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
