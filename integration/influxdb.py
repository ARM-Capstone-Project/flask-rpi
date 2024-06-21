from time import sleep
import datetime
import requests
import random
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

INFLUXDB_URL = os.getenv('INFLUXDB_URL')
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')

class InfluxDb:
	def __init__(self, url, token, org, bucket, precision="ms"):
		self.url = url
		self.token = token
		self.org = org
		self.bucket = bucket
		self.precision = precision

	def get_line_protocol(self, sensor, reading, value):
		line = "{} {}={} {}"
		timestamp = str(int(datetime.datetime.now().timestamp() * 1000))
		return line.format(sensor, reading, value, timestamp)

	def send_line(self, line):
		print(line)
		try:
			url = self._construct_url()
			headers = self._construct_headers()
			print("ThinRpi")
			print(url)
			requests.post(url, data=line, headers=headers)
			logging.info("Data sent successfully")
		except requests.exceptions.RequestException as e:
			logging.error(f"Failed to send data: {e}")

	def _construct_url(self):
		return "{}api/v2/write?org={}&bucket={}&precision={}".format(
			self.url,
			self.org,
			self.bucket,
			self.precision
		)

	def _construct_headers(self):
		return {"Authorization": "Token {}".format(self.token)}

# if __name__ == "__main__":
# 	reading_names = {
# 		"AT":"airTemp",
# 		"SM":"soilMoisture",
# 		"HU":"humidity",
# 		"ST":"soilTemp",
# 		"LI":"light"
# 	}
#
# 	sensor_names = {
# 		"AT":"temp",
# 		"SM":"moisture",
# 		"HU":"humidity",
# 		"ST":"temp",
# 		"LI":"light"
# 		}
#
# 	count = 0
# 	while count < 5:
# 		sensor_code = random.choice(list(reading_names.keys()))
# 		reading = reading_names[sensor_code]
# 		value = random.randint(20, 30)
# 		raw_input = f"b'b\'{sensor_code}:{reading}:{value}\'\r\n'"
#
# 		trimmed_input = raw_input[2:][:-5]
# 		sensor_code = trimmed_input[2:4]
# 		count += 1
# 		if sensor_code in reading_names:
# 			sensor = sensor_names[sensor_code]
# 			reading = reading_names[sensor_code]
# 			client = InfluxDb(
# 				url=INFLUXDB_URL,
# 				token=INFLUXDB_TOKEN,
# 				org=INFLUXDB_ORG,
# 				bucket=INFLUXDB_BUCKET
# 			)
#
# 		line = client.get_line_protocol(sensor, reading, value)
# 		client.send_line(line)
# 		sleep(1)
