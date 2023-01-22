import paho.mqtt.client as mqtt
import argparse
from fifeutil.sqlite_data_store import SqliteDeviceDataStore, StoreTSResult
import json
import logging
from dotenv import load_dotenv
import os
import time

log = logging.getLogger(__name__)


class DataStore:
    """
    Meant to run on the EMCNet server.
    Launches MQTT client to watch for interval data messages and optionally device data messages.
    Writes them to a database (one for each site id)
    Received data records must be a JSON-formatted object with the following key-value pairs:
        "ts": timestamp in seconds since epoch
        "data: a separate JSON object containing a list of field-name value pairs
    If the message topic is emcnet/intervaldata/<site_id>, the database table will be <site_id>.sqlite3.
    The interval data will be placed into the database in a table named `interval`.
    Optionally, if messages are received on topics wit prefix emcnet/devicedata/<site_id>, they will also be
    stored in the database, but in a key-value table named `now`.
    """

    def __init__(self, mqttbrokeraddress='localhost', mqttbrokerport=1883, emcnetdir='./',
                 emcnetremotebrokerid='', emcnetremotebrokerpw=''):
        log.info("MQTT Server Data Store")
        log.info(f"Host: {mqttbrokeraddress + ':' + str(mqttbrokerport)}")
        self.interval_data_topic = 'emcnet/intervaldata/#'
        self.device_data_topic = 'emcnet/devicedata/#'
        self.database_path = emcnetdir.rstrip('/') + '/'
        db_fname = self.database_path + 'emcnet.sqlite3'
        log.info(f"Saving data to {db_fname}")
        self.database_manager = SqliteDeviceDataStore(db_fname)
        self.client = mqtt.Client(client_id='emcnet_server_data_store', clean_session=False)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        # set password
        self.client.username_pw_set(username=emcnetremotebrokerid, password=emcnetremotebrokerpw)
        # handle the case of not being able to make an initial connection
        connected = False
        while not connected:
            try:
                self.client.connect(mqttbrokeraddress, mqttbrokerport, 60)
            except ConnectionRefusedError:
                log.info(f"Error connecting to MQTT broker at "
                         f"{mqttbrokeraddress + ':' + str(mqttbrokerport)}. Waiting")
                time.sleep(10)
            else:
                connected = True

    def on_connect(self, client, userdata, flags, rc):
        log.info(f"Connected with result code {rc}")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        log.info(f"Subscribing to topic {self.interval_data_topic}")
        client.subscribe(self.interval_data_topic, qos=2)
        log.info(f"Subscribing to topic {self.device_data_topic}")
        client.subscribe(self.device_data_topic)

    def on_message(self, client, userdata, msg):
        log.debug(f"Received message on topic {msg.topic}: {str(msg.payload)}")
        # Messages topics should be structured as emcnet/devicedata/<site_id>/<device_id>
        # or emcnet/intervaldata/<site_id>
        msg_split = msg.topic.split('/')
        if 3 <= len(msg_split) <= 4:
            if msg_split[0] == 'emcnet':
                msg_type = msg_split[1]
                site_id = msg_split[2]
                if msg_type == 'intervaldata':
                    table = 'interval_' + site_id
                    try:
                        payload_dict = json.loads(msg.payload)
                    except json.decoder.JSONDecodeError:
                        log.error(f"Received a message on topic {msg.topic} that is not in JSON format: {msg.payload}")
                        return
                    if 'ts' in payload_dict and 'data' in payload_dict:
                        ts = payload_dict['ts']
                        log.info(f"storing interval data to table {table}: ts: {ts}, data: {payload_dict['data']}")
                        result = self.database_manager.store_new_tsdata(table, ts, payload_dict['data'])
                        if result != StoreTSResult.SUCCESS:
                            log.error(f"store_new_tsdata returned result {result}")
                if msg_type == 'devicedata':
                    table = 'now_' + site_id
                    try:
                        payload_dict = json.loads(msg.payload)
                    except json.decoder.JSONDecodeError:
                        log.error(f"Received a message on topic {msg.topic} that is not in JSON format: {msg.payload}")
                        return
                    if 'ts' in payload_dict and 'data' in payload_dict:
                        ts = payload_dict['ts']
                        payload_dict_with_ts = payload_dict["data"]
                        payload_dict_with_ts["ts"] = ts
                        log.debug(f"storing new key value data to table {table}: {payload_dict_with_ts}")
                        self.database_manager.store_new_kvdata(table, payload_dict_with_ts)

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
    parser = argparse.ArgumentParser(description='MQTT Subscriber and Device Database Recorder')
    parser.add_argument('--mqttbrokeraddress', help='MQTT broker address', type=str,
                        default=os.getenv("MQTT_BROKER_ADDRESS", 'localhost'))
    parser.add_argument('--mqttbrokerport', help='MQTT broker port', type=int,
                        default=os.getenv("MQTT_BROKER_PORT", 1883))
    parser.add_argument('--loglevel', help='logging level one of [DEBUG, INFO, WARNING, ERROR, CRITICAL]',
                        default=os.getenv("EMCNET_LOG_LEVEL", 'INFO'))
    parser.add_argument('--emcnetdir', dest='emcnetdir', default=emcnetdir, help='Path to emcnet files')
    parser.add_argument('--emcnetremotebrokerid', default=os.getenv("REMOTEBROKERID", 'INFO'),
                        help='EMCNET remote broker (server) user ID')
    parser.add_argument('--emcnetremotebrokerpw', default=os.getenv("REMOTESERVERPW", 'INFO'),
                        help='EMCNET remote broker (server) password')
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel.upper())
    ds = DataStore(mqttbrokeraddress=args.mqttbrokeraddress, mqttbrokerport=args.mqttbrokerport,
                   emcnetdir=args.emcnetdir, emcnetremotebrokerid=args.emcnetremotebrokerid,
                   emcnetremotebrokerpw=args.emcnetremotebrokerpw)
    ds.run()


if __name__ == "__main__":
    # execute only if run as a script
    main()
