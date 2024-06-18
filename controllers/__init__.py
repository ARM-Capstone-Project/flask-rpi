# from flask import Flask
# from blueprints.basic_endpoints import blueprint as basic_endpoint
#
# app = Flask(__name__)
#
# app.register_blueprint(basic_endpoint)
#
#
# from flask import Flask, render_template
# from data_model import RS485Sensor
#
# app = Flask(__name__)
#
# # Create a single sensor instance (can be modified for multiple sensors)
# sensor = RS485Sensor()
#
# @app.route("/")
# def index():
#     data = sensor.read_data()
#     interpreted_data = sensor.interpret_data(data)
#     return render_template("index.html", data=interpreted_data)
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", debug=True)  # Set debug=False for production
