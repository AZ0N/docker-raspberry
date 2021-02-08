#!/usr/bin/env python3

import datetime
import psutil
from influxdb import InfluxDBClient

# influx configuration - edit these
ifuser = "grafana"
ifpass = "password"
ifdb   = "maindb"
ifhost = "influxdb"
ifport = 8086
measurement_name = "system"

# take a timestamp for this measurement
time = datetime.datetime.utcnow()

# collect some stats from psutil
disk = psutil.disk_usage('/')
mediadisk = psutil.disk_usage('/mnt/media')
mem = psutil.virtual_memory()
load = psutil.getloadavg()

# Get CPU temperature
temp = 0
for key, value in psutil.sensors_temperatures().items():
    if key == "cpu_thermal":
        temp = value[0]

# format the data as a single measurement for influx
body = [
    {
        "measurement": measurement_name,
        "time": time,
        "fields": {
            "load_1": load[0],
            "load_5": load[1],
            "load_15": load[2],
            "disk_percent": disk.percent,
            "disk_free": disk.free,
            "disk_used": disk.used,
            "disk_media_percent": mediadisk.percent,
            "disk_media_free": mediadisk.free,
            "disk_media_used": mediadisk.used,
            "mem_percent": mem.percent,
            "mem_free": mem.free,
            "mem_used": mem.used,
            "cpu_temp": temp.current,
        }
    }
]

# connect to influx
ifclient = InfluxDBClient(ifhost,ifport,ifuser,ifpass,ifdb)

# write the measurement
ifclient.write_points(body)