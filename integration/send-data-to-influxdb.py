import argparse
from time import sleep
import datetime
import requests
import random

parser = argparse.ArgumentParser(description='Send data to influxdb')
parser.add_argument('--port', required=False,  help='USB port to use, defaults to /dev/ttyUSB0')
parser.add_argument('--wait', required=False, default=0, type=int, help='Second to wait after opening the connection. Useful for devices like arduino that are rest when the serial connection is opened.')
parser.add_argument('--baud', required=False, default=9600, type=int, help='Desired baud rate. Defaults to 9600.')
parser.add_argument('--token', required=True, type=str, help='Your InfluxDB REST token. This argument is required.')
parser.add_argument('--org', required=False, type=str, default="Raspberry Pi", help='Your InfluxDB organization name. This argument is required.')
parser.add_argument('--url', required=False, type=str, default="http://localhost:8086/", help="defaults to localdb")
parser.add_argument('--bucket', required=False, type=str, default="Integration Test", help="the bucket to write to")
args = parser.parse_args()

#variables related to reading from the USB port
port = vars(args)["port"]
wait = vars(args)["wait"]
baud = vars(args)["baud"]

#mapping to turn info from the arduino to something readable
reading_names = {
	"AT":"airTemp",
	"SM":"soilMoisture",
	"HU":"humidity",
	"ST":"soilTemp",
	"LI":"light"
}

sensor_names = {
	"AT":"temp",
	"SM":"moisture",
	"HU":"humidity",
	"ST":"temp",
	"LI":"light"
}

#variables related to using the REST API
influx_url = vars(args)["url"]
influx_token = vars(args)["token"]
organization = vars(args)["org"]
bucket = vars(args)["bucket"]
precision = "ms"

#port defaults to /dev/ttyUSB0
#TODO: do a query and pick a sensible and non-platform specific default
# if port is None or port == "":
# 	port = "/dev/ttyUSB0"
#
# ser = serial.serial_for_url(port, do_not_open=True)
# ser.baudrate = baud
# ser.open()

if wait > 0:
	sleep(wait)

def get_line_protocol(sensor, reading, value):
    line = "{} {}={} {}"
    timestamp = str(int(datetime.datetime.now().timestamp() * 1000))
    return line.format(sensor, reading, value, timestamp)

def send_line(line):
    try:
        url = "{}api/v2/write?org={}&bucket={}&precision={}".format(influx_url, organization, bucket, precision)
        headers = {"Authorization": "Token {}".format(influx_token)}
        r = requests.post(url, data=line, headers=headers)
        print(line)
    except:
		# this is terrible
		# any time there is a problem with the server, data will be lost
		# this is a job for Telegraf
	    print("oops")

count = 0
random_int = random.randint(10, 50)

while count < random_int:
	sensor_code = random.choice(list(reading_names.keys()))
	reading = reading_names[sensor_code]
	value = random.randint(20, 30)
	raw_input = f"b'b\'{sensor_code}:{reading}:{value}\'\r\n'"

	trimmed_input = raw_input[2:][:-5]
	sensor_code = trimmed_input[2:4]
	count += 1
	if sensor_code in reading_names:
		sensor = sensor_names[sensor_code]
		reading = reading_names[sensor_code]
		line = get_line_protocol(sensor, reading, value)
		send_line(line)
