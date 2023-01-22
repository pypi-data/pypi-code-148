from collections import OrderedDict
import paho.mqtt.client as mqtt
import argparse
from fifeutil.sqlite_data_store import SqliteDeviceDataStore
from fifeutil.intervalmgr import IntervalMgr
import json
import logging
from dotenv import load_dotenv
import os
import time

log = logging.getLogger(__name__)

intervalTypes = {
    'batteryVoltage': ["first", "last", "avg", "max", "min"],
    'panelVoltage': ["first", "last", "avg"],
    'panelPower': ["first", "avg"],
    'batteryCurrent': ["first", "avg", "max", "min"],
    'loadCurrent': [],
    'load': [],
    'yieldTotal': ["first", "last"],
    'yieldToday': ['first'],
    'maximumPowerToday': ['first'],
    'yieldYesterday': ["first"],
    'maximumPowerYesterday': ["first"],
    'daySequenceNumber': ["first"],
    'productId': [],
    'firmwareVersion': [],
    'serialNumber': [],
    'mode': ["first"],
    'trackerMode': ["first"],
    'offReason': ['first'],
    'error': ['first', 'lastnonzero'],
    'V': ['first', 'last', 'avg', "max", "min"],
    'I': ['first', 'avg', "max", "min"],
    'P': ['first', 'avg', "max", "min"]
}


class SiteDataProcessor:
    """
    Launches MQTT client to watch for device data messages, converts the device data messages into
    interval data, and updates a database.
    Received device data records must be a JSON-formatted object with the following key-value pairs:
        "ts": timestamp in seconds since epoch
        "data: a separate JSON object containing a list of field-name value pairs
    The device messages topics be in the format emcnet/devicedata/<site_id>/<device_id>.
    The database name will be <site_id>.sqlite3.
    The database tables generated will be:
        1. `interval` as a time-series of accumulated intervals, and
        2. `now` as a key-value table of the most recent instantaneous device data values
    Rules for Processing Data into Fixed Intervals:
        1. Interval values will be calculated by interval accumulator functions provided on a field-by-field basis.
        2. Previous intervals will be closed out when any measurement is received for a later interval.
        3. device data records for previous (closed out) intervals will be ignored.
    """

    def __init__(self, site_id='defaultsite', mqttbrokeraddress='localhost', mqttbrokerport=1883,
                 emcnetdir='./', intervals_per_hour=4):
        log.info("MQTT Site Data Processor")
        log.info(f"Host: {mqttbrokeraddress + ':' + str(mqttbrokerport)}")
        log.info(f"EMCNet directory: {emcnetdir}")
        self.site_id = site_id.lstrip('/').rstrip('/')
        log.info(f"Site ID: {self.site_id}")
        self.client = mqtt.Client(client_id='emcnet_'+self.site_id, clean_session=False)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.device_data_topic = 'emcnet/devicedata/#'
        self.interval_data_topic = 'emcnet/intervaldata/' + self.site_id
        self.database_path = emcnetdir.rstrip('/') + '/'
        db_fname = self.database_path + self.site_id + '.sqlite3'
        log.info(f"Saving data to {db_fname}")
        self.database_manager = SqliteDeviceDataStore(db_fname)
        self.im = IntervalMgr(self.database_manager, intervalTypes, self.on_interval,
                              intervals_per_hour=intervals_per_hour)
        # handle the case of not being able to make an initial connection
        connected = False
        while not connected:
            try:
                self.client.connect(host=mqttbrokeraddress, port=mqttbrokerport, keepalive=60)
            except ConnectionRefusedError:
                log.info("Error connecting - waiting")
                time.sleep(10)
            else:
                connected = True

    def on_connect(self, client, userdata, flags, rc):
        log.info("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        topics = self.device_data_topic
        log.info("Subscribing to topics " + topics)
        client.subscribe(topics)

    def on_message(self, client, userdata, msg):
        log.debug(f"Received message on topic {msg.topic}: {str(msg.payload)}")
        # Messages topics should be structured as emcnet/devicedata/<site_id>/<device_id>
        msg_split = msg.topic.split('/')
        if len(msg_split) == 4:
            if msg_split[0] == 'emcnet' and msg_split[1] == 'devicedata':
                try:
                    payload_dict = json.loads(msg.payload)
                except json.decoder.JSONDecodeError:
                    log.error(f"Received a message on topic {msg.topic} that is not in JSON format: {msg.payload}")
                    return
                if 'ts' in payload_dict and 'data' in payload_dict:
                    ts = payload_dict['ts']
                    self.im.process(ts, payload_dict['data'])

    def on_interval(self, ts, interval_payload_dict, **kwargs):
        """
        additional processing of an interval, e.g. publish to the cloud
        """
        payload_ordered = OrderedDict([('ts', ts), ('data', interval_payload_dict)])
        payload_str = json.dumps(payload_ordered)
        topic = self.interval_data_topic
        self.client.publish(topic, payload_str, qos=2)
        log.info(f"Sent on topic {topic}: {payload_str}")

    def run(self):
        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        self.client.loop_forever()


def main():
    # set the default path to the EMCNET directory - from the environment if set
    emcnetdir = os.getenv("EMCNETDIR", './').rstrip('/')
    load_dotenv(emcnetdir + '/config.env', override=True)
    # read command-line arguments and override environment variables if given
    parser = argparse.ArgumentParser(description='Subscribe to device data MQTT topics, accumulate interval data,'
                                                 + 'save, and re-publish')
    parser.add_argument('--site_id', type=str, default=os.getenv("SITE_ID", 'defaultsiteid'), help='Site ID')
    parser.add_argument('--mqttbrokeraddress', help='MQTT broker address', type=str,
                        default=os.getenv("MQTT_BROKER_ADDRESS", 'localhost'))
    parser.add_argument('--mqttbrokerport', help='MQTT broker port', type=int,
                        default=os.getenv("MQTT_BROKER_PORT", 1883))
    parser.add_argument('--loglevel', help='logging level one of [DEBUG, INFO, WARNING, ERROR, CRITICAL]',
                        default=os.getenv("EMCNET_LOG_LEVEL", 'INFO'))
    parser.add_argument('--emcnetdir', dest='emcnetdir', default=emcnetdir, help='Path to emcnet files')
    parser.add_argument('--iph', dest='intervals_per_hour', type=int,  default=os.getenv("INTERVALS_PER_HOUR", 4),
                        help='Number of intervals per hour')
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel.upper())
    bdp = SiteDataProcessor(site_id=args.site_id, mqttbrokeraddress=args.mqttbrokeraddress,
                            mqttbrokerport=args.mqttbrokerport,
                            emcnetdir=args.emcnetdir, intervals_per_hour=args.intervals_per_hour)
    bdp.run()
