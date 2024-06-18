from flask import Blueprint
from flask import request
from flask import jsonify
from blueprints.api.v1.sensors.temperature import temperature_bp

sensors_bp = Blueprint('sensors', __name__, url_prefix='/api/v1/sensors')
sensors_bp.register_blueprint(temperature_bp)

@sensors_bp.route('/', methods=['GET'])
def index():
    return {
        'message': 'This endpoint should return a list of sensor records',
        'method': request.method
    }

@sensors_bp.route('/<int:sensor_id>', methods=['GET'])
def show(sensor_id):
    return {
        'id': sensor_id,
        'message': 'This endpoint should return a sensor {} record'.format(sensor_id),
        'method': request.method
    }

@sensors_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    return {
        'message': 'This endpoint should create a sensor record',
        'method': request.method,
        'body': data
    }

# @sensors_bp.route('/<int:sensor_id>', methods=['PUT'])
# def update(sensor_id):
#     data = request.get_json()
#     return {
#         'id': sensor_id,
#         'message': 'This endpoint should update a sensor {} record'.format(sensor_id),
#         'method': request.method,
#         'body': data
#     }

# @sensors_bp.route('/<int:sensor_id>', methods=['DELETE'])
# def destroy(sensor_id):
#     data = request.get_json()
#     return {
#         'id': sensor_id,
#         'message': 'This endpoint should delete a sensor {} record'.format(sensor_id),
#         'method': request.method
#     }
