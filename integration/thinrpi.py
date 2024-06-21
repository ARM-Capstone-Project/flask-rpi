import time
import json
import os
import board
# import adafruit_dht
from influxdb import InfluxDb
from dotenv import load_dotenv
import random

load_dotenv()

INFLUXDB_URL = os.getenv('INFLUXDB_URL')
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')


class ThinRpi:
    def __init__(self):
        print("init")
        #   self.dhtDevice = adafruit_dht.DHT11(board.D4)

    def run(self):
        client = InfluxDb(
            INFLUXDB_URL,
            INFLUXDB_TOKEN,
            INFLUXDB_ORG,
            INFLUXDB_BUCKET
        )
        while True:
            try:
                # temperature_c = 300 # self.dhtDevice.temperature
                # temperature_f = temperature_c * (9 / 5) + 32
                # humidity = 200 # self.dhtDevice.humidity
                #
                # data = {
                #             "sensors": {
                #             "temperature_f": round(temperature_f, 1),
                #             "temperature_c": round(temperature_c, 1),
                #             "humidity": humidity,
                #         },
                #     "status": "online",
                # }

                data = [
                    {"reading": "temperature", "value": random.randint(20, 30)},
                    {"reading": "light", "value": random.randint(20, 30)},
                    {"reading": "humidity", "value": random.randint(20, 30)},
                    {"reading": "moisture", "value": random.randint(20, 30)}
                ]

                # Loop through each sensor data point
                for sensor_data in data:
                    reading = sensor_data["reading"]
                    value = sensor_data["value"]

                    line_protocol = client.get_line_protocol(
                        "sensor", reading, value)
                    client.send_line(line_protocol)
            except RuntimeError as error:
                print(error.args[0])
                time.sleep(5)
                continue

            except Exception as error:
                raise error

            time.sleep(5)


if __name__ == "__main__":
    thin_rpi = ThinRpi()
    thin_rpi.run()
