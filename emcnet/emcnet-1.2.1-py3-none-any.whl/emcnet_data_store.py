# -*- coding: utf-8 -*-
""" Store EMCNET device data to InfluxDB.

This module reads lines of emcnet json-encoded device data from stdin and
stores them directly in the locally-running influx database.

Optionally the device + serial number may be specified at instantiation, in which case
it assumes all data is from a single device + serial number, and, therefore, stores it
in a single influxdb "measurement."

EMCNET always gives priority to key identifiers being specified in the payload rather than
MQTT topics or other sources.  Therfore, when a "measurement" name is included in
the root level object of the json payload, it will be preserved through the MQTT and 
InfluxDB chain, and the InfluxDB records will reflect that measurement string.

The messages are expected to be in json format.  

If the "measurement" field is missing from the message, then 
"measurement"="<measurement>" is added to
message.

Similarly, if id is specified via topic `emcnet/<measurement>[/<id>]`, and if the json
payload contains a "tag" element, and id is not specified within it, this module will create
an "id" tag within the payload.

Example:
    Piping streaming 5-sec data output from one service into emcnet-device-data-store,
    and override the model name::

        $ export EMCNET_INFLUX_ORG=flyinion
        $ export EMCNET_INFLUX_EDGE_URL=http://localhost:8086
        $ export EMCNET_INFLUX_EDGE_TOKEN=WHrHoIaR5MQnVcw52rTe7aKDc22U5_-wG_dQsSr14EjJWotyCJ4HbxDtSleXM4g4bXxFvKC_cjZ0AZeuwP6E4w==
        $ export EMCNET_SITE=test
        $ export EMCNET_LOG_LEVEL=info
        $ export EMCNET_MQTT_BROKER_ADDRESS=localhost
        $ export EMCNET_MQTT_BROKER_PORT=1883
        $ ../rpi-ina226/ina226_emulate | emcnet_device_data_store --device=ina226 --id=emulator

Attributes:

Todo:

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

import argparse
import json
import time
import sys
import logging
from dotenv import load_dotenv
import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import Point


log = logging.getLogger(__name__)

DEFAULT_DEVICE = "unknown_0"


class EMCNETDataStore:
    """ Intantiate an InfluxDB client and write 
    EMCNET device data to the database.

    Starts an InfluxDB client and writes EMCNET device data to
    bucket <bucket> and measurement <device>.  Sets tag "id" = <id>.

    Attributes:
            influxorg (str): org (typically "emcnet")
            influxedgeurl (str): typically http://localhost:8086
            influxedgetoken (str): secret token
            bucket (str): "st" or "lt"
            device (str): device name (e.g. vmppt or ina226)
            id (str): device id (e.g. camperbattery)
    """

    def __init__(self, influxorg, influxedgeurl, influxedgetoken, bucket="st", 
                 device=None, id=None):
        """ Instantiate
        Args:
            influxorg (str): org (typically "emcnet")
            influxedgeurl (str): typically http://localhost:8086
            influxedgetoken (str): secret token
            bucket (str): "st" or "lt"
            device (str): device name (e.g. vmppt or ina226)
            id (str): device id (e.g. camperbattery)
        """
        self.influxorg = influxorg
        self.influxedgeurl = influxedgeurl
        self.influxedgetoken = influxedgetoken
        self.bucket = "raw"
        self.device = device
        log.info(f"EMCNET Device Data Store Class Initialized - Capturing data")
        log.info(f"Influx Org: {influxorg}")
        log.info(f"Influx Edge URL: {influxedgeurl}")
        log.info(f"Bucket: raw")
        if self.device is not None:
            log.info(f"Device/Measurement: {self.device}")
        if self.id is not None:
            log.info(f"Device ID: {self.id}")
        self.client = influxdb_client.InfluxDBClient(
            url=influxedgeurl,
            token=influxedgetoken,
            org=influxorg
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)


    def store(self, payload):
        """
        Store device measurement in influx db.  In the database, the following mapping occurs:
        InfluxDB        EMCNET
        -----------     -------------
        bucket          raw and aggregated; aggregated is synchronized with the cloud bucket named 
                            EMCNET_SITE via InfluxDB task
        measurement     <device>
        tags            any device-provided key-value tags in the payload
        fields          any device-provided key-value fields in the payload

        Args:
            payload: json data record to publish. Special name-value pairs:
                "measurement": (str) measurement per influxdb definition.  In EMCNET, it's expected to be <device>_<serno> 
                                but may be anything unique. If <device> is provided on instantiation, it override this value.
                "time"       : (int64) (optional) measurement time - nanoseconds since epoch 
                "tags"       : (json object) (optional) any additional tags for this measurement point
                "fields"     : (json object) the list of field names and values
        """
        log.debug(f"Received: {payload}")
        if isinstance(payload, str):
            line = payload.strip()
            try:
                payload = json.loads(line)
            except json.decoder.JSONDecodeError:
                log.error(f"JSON decode error on {line}")
                return
        if isinstance(payload, dict):
            # If measurment has been provided on instantiation, override device payload
            if self.device is not None:
                payload["measurement"] = self.device

            if self.id is not None:
                if "tags" in payload:
                    payload["tags"]["id"] = self.id
                else:
                    payload["tags"] = dict()
                    payload["tags"]["id"] = self.id
 
            # write the measurement
            self.write_api.write(self.bucket, self.influxorg, payload)
            
            log.info(json.dumps(payload, separators=(',', ':')))
        else:
            log.error(f"Unsupported payload type: {payload!r}")

    def run(self):
        """ Continuously read data records from stdin in JSON format and store in influxdb
        """
        while True:
            # See see https://stackoverflow.com/questions/26677389/python-stdin-readline-blocks
            line = sys.stdin.readline()  # blocking
            if line is not None:
                if line:
                    self.store(line)
            time.sleep(0.1)


def main():
    # set the default path to the EMCNET directory - from the environment if set
    emcnetdir = os.getenv("EMCNET_DIR", '/etc/emcnet').rstrip('/')
    load_dotenv(emcnetdir + '/config.env', override=True)
    # read command-line arguments and override environment variables if given
    parser = argparse.ArgumentParser(description=(
        'EMCNET Device Data Store - stores stdin json measurements in the influx database'))
    parser.add_argument('--influxorg', type=str, default=os.getenv("EMCNET_INFLUX_ORG", 'emcnet'), 
                        help='InfluxDB org (usually emcnet)')
    parser.add_argument('--influxedgeurl', type=str, default=os.getenv("EMCNET_INFLUX_EDGE_URL", 'http://localhost:8086'), 
                        help='InfluxDB edge url (usually http://localhost:8086)')    
    parser.add_argument('--influxedgetoken', type=str, default=os.getenv("EMCNET_INFLUX_EDGE_TOKEN", 'unknown_token'), 
                        help='InfluxDB edge token')    
    parser.add_argument('--device', help='Override Unique Device Name (e.g. "ina226_12345", "dht22_45678", etc...)', type=str)
    parser.add_argument('--loglevel', help='logging level one of [DEBUG, INFO, WARNING, ERROR, CRITICAL]',
        default=os.getenv("EMCNET_LOG_LEVEL", 'INFO'))

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel.upper())
    log.info("EMCNET Device Data Store - stores stdin json measurements in the influx database")
    log.info(f"EMCNet directory: {emcnetdir}")
    log.info(f"Influx Org: {args.influxorg}")
    log.info(f"Influx Edge URL: {args.influxedgeurl}")
    if args.device is not None:
        log.info(f"Device/Measurement: {args.device}")
    dds = EMCNETDataStore(args.influxorg, args.influxedgeurl, args.influxedgetoken, device=args.device)
    dds.run()


if __name__ == '__main__':
    main()
