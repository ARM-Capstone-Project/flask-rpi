from flask import Flask
from flask import render_template
from flask_cors import CORS
from blueprints.api.v1.sensors import sensors_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(sensors_bp)


@app.route('/')
def home():
    return render_template(
        "home.html",
        user_name = "user",
        message = "Flask API is running in Raspberry Pi"
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
