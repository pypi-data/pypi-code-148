# -*- coding: utf-8 -*-
""" Monitor the emcnet MQTT topic and record all valid emcnet data packets to InfluxDB

EMCNET always gives priority to key identifiers being specified in the payload rather than
MQTT topics or other sources.  Therfore, when a "measurement" name is included in
the root level object of the json payload, it will be preserved through the MQTT and 
InfluxDB chain, and the InfluxDB records will reflect that measurement string.

The messages are expected to be in json format.  

If the "measurement" field is missing from the message, then 
"measurement"="<measurement>" is added to message, where `measurement` is
the second-level topic: `emcnet/<measurement>[/<id>].

Similarly, if id is specified via topic `emcnet/<measurement>[/<id>]`, and if the json
payload "tag" element does not contain an 'id' field, this module will create
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
        $ emcnet_record

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
import paho.mqtt.client as mqtt


log = logging.getLogger(__name__)

DEFAULT_DEVICE = "unknown_0"


class EMCNETDataStore:
    """ Intantiate an InfluxDB client and write 
    EMCNET device data to the database.

    Starts an InfluxDB client and writes EMCNET device data to
    bucket "st."

    If the "measurement" field is missing from the message, then 
    "measurement"="<measurement>" is added to message, where `measurement` is
    the second-level topic: `emcnet/<measurement>[/<id>].

    Similarly, if id is specified via topic `emcnet/<measurement>[/<id>]`, and if the json
    payload "tag" element does not contain an 'id' field, this module will create
    an "id" tag within the payload.
    """

    def __init__(self, influxorg, influxedgeurl, influxedgetoken, 
                 mqttbrokeraddress='localhost', mqttbrokerport=1883):
        """ Instantiate
        Args:
            influxorg (str): org (typically "emcnet")
            influxedgeurl (str): typically http://localhost:8086
            influxedgetoken (str): secret token
            mqttbrokeraddress (str): MQTT broker address, e.g. "localhost"
            mqttbrokerport (str): MQTT broker port, e.g. "8086"
        """
        self.influxorg = influxorg
        self.influxedgeurl = influxedgeurl
        self.influxedgetoken = influxedgetoken
        self.bucket = "st"
        log.info(f"EMCNET Recorder Class Initialized - Capturing data")
        log.info(f"MQTT Broker: {mqttbrokeraddress + ':' + str(mqttbrokerport)}")
        log.info(f"Influx Org: {influxorg}")
        log.info(f"Influx Edge URL: {influxedgeurl}")
        log.info(f"Bucket: {self.bucket}")
        
        # Set up InfluxDB Client
        self.database_client = influxdb_client.InfluxDBClient(
            url=influxedgeurl,
            token=influxedgetoken,
            org=influxorg
        )
        self.database_write_api = self.database_client.write_api(write_options=SYNCHRONOUS)
        
        # Set up MQTT Client
        self.mqtt_client = mqtt.Client(client_id='emcnet_recorder', clean_session=True)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        # set password
        # self.mqtt_client.username_pw_set(username=emcnetremotebrokerid, password=emcnetremotebrokerpw)
        # handle the case of not being able to make an initial connection
        connected = False
        while not connected:
            try:
                self.mqtt_client.connect(mqttbrokeraddress, mqttbrokerport, 60)
            except ConnectionRefusedError:
                log.info(f"Error connecting to MQTT broker at "
                         f"{mqttbrokeraddress + ':' + str(mqttbrokerport)}. Waiting...")
                time.sleep(10)
            else:
                connected = True        

    def on_connect(self, client, userdata, flags, rc):
        log.info(f"Connected with result code {rc}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        log.info(f"Subscribing to topic emcnet/#")
        client.subscribe("emcnet/#")

    def on_message(self, client, userdata, msg):
        log.debug(f"Received message on topic {msg.topic}: {str(msg.payload)}")
        # Messages topics should be structured as emcnet/<measurement>[/<id>]
        msg_split = msg.topic.split('/')
        if len(msg_split) >= 2:
            measurement = msg_split[1]
            if len(msg_split) >= 3:
                id = msg_split[2]
            else:
                id = None
            self.store(msg.payload, measurement, id)
        else:
            log.error("No measurement in emcnet topic string.")

    def run(self):
        """ Continuously watch emcnet MQTT topic and respond on message 
        """
        while True:
            # Blocking call that processes network traffic, dispatches callbacks and
            # handles reconnecting.
            # Other loop*() functions are available that give a threaded interface and a
            # manual interface.
            self.mqtt_client.loop_forever()
            
    def store(self, payload, measurement, id):
            """
            Store device measurement in influx db.  In the database, the following mapping occurs:
            InfluxDB        EMCNET
            -----------     -------------
            bucket          raw and aggregated; aggregated is synchronized with the cloud bucket named 
                                EMCNET_SITE via InfluxDB task
            measurement     Source of data e.g. "vmppt", "ina226", or "soc_kalman"
            tags            any device-provided key-value tags in the payload
            id           Specific ID of the measurement, e.g. 0001 or vanbattery 
            fields          any device-provided key-value fields in the payload

            Args:
                payload (str): json data record to publish. Special name-value pairs:
                    "measurement": (str) measurement per influxdb definition.  In EMCNET, it's expected to be <device>_<serno> 
                                    but may be anything unique. If <device> is provided on instantiation, it override this value.
                    "time"       : (int64) (optional) measurement time - nanoseconds since epoch 
                    "tags"       : (json object) (optional) any additional tags for this measurement point
                    "fields"     : (json object) the list of field names and values
                measurement (str)   : Source of the data, e.g. "vmppt" or "ina226"
                id (str):           : Specific ID of the measurement, e.g. 0001 or vanbattery
            """
            log.debug(f"Received: {payload}")
            try:
                payload_dict = json.loads(payload)
            except json.decoder.JSONDecodeError:
                log.error(f"JSON decode error on {payload}")
                return
            if isinstance(payload_dict, dict):
                if "fields" in payload_dict:
                    # if no measurement element is found in the payload, add it based on the topic
                    if not "measurement" in payload_dict:
                        payload_dict["measurement"] = measurement
                    # if an ID was included in the topic string, check if we need to insert it into the payload
                    if id:
                        if not "tags" in payload_dict:
                            payload_dict["tags"] = dict()
                        if not "id" in payload_dict["tags"]:
                            payload_dict["tags"]["id"] = id
                    # write the measurement
                    self.database_write_api.write(self.bucket, self.influxorg, payload_dict)
                    log.debug("Wrote: "+json.dumps(payload_dict, separators=(',', ':')))
                else:
                    log.error(f"No fields in payload.")
            else:
                log.error(f"Unsupported payload type: {payload!r}")

def main():
    # set the default path to the EMCNET directory - from the environment if set
    emcnetdir = os.getenv("EMCNET_DIR", '/etc/emcnet').rstrip('/')
    load_dotenv(emcnetdir + '/config.env', override=True)
    # read command-line arguments and override environment variables if given
    parser = argparse.ArgumentParser(description=(
        'EMCNET Recorder - streams EMCNET MQTT data packets to the influx database'))
    parser.add_argument('--mqttbrokeraddress', help='MQTT broker address', type=str,
                        default=os.getenv("MQTT_BROKER_ADDRESS", 'localhost'))
    parser.add_argument('--mqttbrokerport', help='MQTT broker port', type=int,
                        default=os.getenv("MQTT_BROKER_PORT", 1883))    
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
    ds = EMCNETDataStore(args.influxorg, args.influxedgeurl, args.influxedgetoken, 
                          mqttbrokeraddress=args.mqttbrokeraddress, mqttbrokerport=args.mqttbrokerport)
    ds.run()


if __name__ == '__main__':
    main()
