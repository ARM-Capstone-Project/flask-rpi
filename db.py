class InfluxDB:
    def send_line(line):
        url = "{}api/v2/write?org={}&bucket={}&precision={}".format(influx_url, organization, bucket, precision)
        headers = {"Authorization": "Token {}".format(influx_token)}
        r = requests.post(url, data=line, headers=headers)
