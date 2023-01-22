""" Publish EMCNET device data to MQTT.

Publish device data to MQTT topic `emcnet/<measurement>[/<id>]`.  
`measurement` is the name of the service or device that generated 
the data (i.e. the "producer."). But `measurement` will not
override a "measurement" field within the root object of the json payload
unless overridemeasurment=True.
Similarly, id` can be included if 
one wishes to further denote a mesaurement id, but it will not
override an "id" field within the "tag" object or the json payload 
unless overridemeasurment=True.  
ID may be a serial number or a location.  Examples could be "vmppt/0001",
"vmppt/vanbattery."

Typical usage example:

  $ ../rpi-ina226/ina226_emulate | emcnet_data_publisher ina226_emulate --id=0001

"""

import argparse
import paho.mqtt.client as mqtt
import json
import time
import sys
import logging
from dotenv import load_dotenv
import os

log = logging.getLogger(__name__)


class MQTTDataPublisher:
    """Publish EMCNET device data to MQTT.

    Starts an MQTT client and writes EMCNET device data to
    MQTT topic `emcnet/<measurement>[/<id>]`.  
    `measurement` is the name of the service or device that generated 
    the data (i.e. the "producer."). But `measurement` will not
    override a "measurement" field within the root object of the json payload
    unless overridemeasurment=True.
    Similarly, id` can be included if 
    one wishes to further denote a mesaurement id, but it will not
    override an "id" field within the "tag" object or the json payload 
    unless overridemeasurment=True.  
    ID may be a serial number or a location.  Examples could be "vmppt/0001",
    "vmppt/vanbattery."

    Attributes:
            mqttbrokeraddress (str): MQTT broker address
            mqttbrokerport (int): MQTT broker port
            measurement (str): data producer (e.g. vmppt, ina226, vmppt_a, ina226_a)
            id (str): device id (e.g. 0001 or camperbattery)
            topic (str): <measurement>/<id>
            overridemeasurement (bool): override the measurement and id fields
    """

    def __init__(self, measurement, id=None, overridemeasurement=False, 
                 mqttbrokeraddress='localhost', mqttbrokerport=1883):
        """ Instantiate an MQTT client and start it

        Args:
            measurement (str): data producer (e.g. vmppt, ina226, vmppt_a, ina226_a)
            id (str): (optional) device id (e.g. 0001 or camperbattery)
            mqttbrokeraddress (str): MQTT broker address
            mqttbrokerport (int): MQTT broker port
        """
        self.client = mqtt.Client()
        self.client.connect(mqttbrokeraddress, mqttbrokerport, 60)
        self.client.loop_start()
        self.measurement = measurement
        self.id = id
        self.overridemeasurement = overridemeasurement
        if isinstance(measurement, str):
            self.topic = "emcnet/" + measurement.strip()
            if id:
                if isinstance(id, str):
                    self.topic = self.topic + "/" + id.strip()
                else:
                    log.error("id is not a string")
                    raise Exception("id must be a string")
            else:
                # could look for ID in the payload but not sure this is the best design
                pass
        else:
            log.error("measurement must be a string")
            raise Exception("Measurement must be a string")
            
        log.info(f"MQTT Device Data Publisher to {mqttbrokeraddress}:{mqttbrokerport}, Topic: {self.topic}")


    def publish(self, payload):
        """
        Publish device data to MQTT broker on self.topic.
        This method publishes a record that conforms to the EMCNet standard, payload should be a JSON-formatted string.

        Args:
            payload: json data record to publish. Special name-value pairs:
                "measurement": (str) measurement per influxdb definition.  In EMCNET, it's expected to be <device>_<serno> 
                                but may be anything unique. If <device> is provided on instantiation, it override this value.
                "time"       : (int64) (optional) measurement time - nanoseconds since epoch.  If not present, this routine will generate it.
                "tags"       : (json object) (optional) any additional tags for this measurement point
                "fields"     : (json object) the list of field names and values
        """
        log.debug(f"Received: {payload}")
        if isinstance(payload, str):
            line = payload.strip()
            try:
                payload = json.loads(line)
            except json.decoder.JSONDecodeError:
                log.error("JSON decode error.")
                return
        if isinstance(payload, dict):
            if not "time" in payload:
                payload["time"] = time.time_ns()
            if self.overridemeasurement:
                payload["measurement"] = self.measurement
                if self.id:
                    if not "tags" in payload:
                        payload["tags"] = dict()
                    payload["tags"]["id"] = self.id
            payload_str = json.dumps(payload, separators=(',', ':'))
            self.client.publish(self.topic, payload_str)
            log.debug(f"Sent on topic {self.topic}: {payload_str}")
        else:
            log.error(f"Unsupported payload type: {payload!r}")

    def run(self):
        """ Continuously read data records from stdin in JSON format and publish to MQTT broker
        """
        while True:
            # See see https://stackoverflow.com/questions/26677389/python-stdin-readline-blocks
            line = sys.stdin.readline()  # blocking
            if line is not None:
                if line:
                    self.publish(line)
            time.sleep(0.1)


def main():
    # set the default path to the EMCNET directory - from the environment if set
    emcnetdir = os.getenv("EMCNET_DIR", '/etc/emcnet').rstrip('/')
    load_dotenv(emcnetdir + '/config.env', override=True)
    # read command-line arguments and override environment variables if given
    parser = argparse.ArgumentParser(description=(
        'MPPT Publisher - listens for device messages (lines) on stdin and sends them to the MQTT broker'))
    parser.add_argument('measurement', help='source or producer of the data', type=str)
    parser.add_argument('--id', help='ID to further distinguish this data', type=str)
    parser.add_argument('--mqttbrokeraddress', help='MQTT broker address', type=str,
                        default=os.getenv("MQTT_BROKER_ADDRESS", 'localhost'))
    parser.add_argument('--mqttbrokerport', help='MQTT broker port', type=int,
                        default=os.getenv("MQTT_BROKER_PORT", 1883))
    parser.add_argument('--loglevel', help='logging level one of [DEBUG, INFO, WARNING, ERROR, CRITICAL]',
                        default=os.getenv("EMCNET_LOG_LEVEL", 'INFO'))
    parser.add_argument('-o', '--overridemeasurement', help='overwrite measurement and id fields in payload',
                        action = "store_true")

    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel.upper())
    log.info("MPPT Publisher - listens for messages (lines) on stdin and sends them to the MQTT broker")
    log.info(f"EMCNet directory: {emcnetdir}")
    log.info(f"Broker: {args.mqttbrokeraddress}:{args.mqttbrokerport}")
    log.info(f"Measurement: {args.measurement}")
    if args.id is not None:
        log.info(f"ID: {args.id}")
    ddp = MQTTDataPublisher(args.measurement, id=args.id, overridemeasurement=args.overridemeasurement, 
                            mqttbrokeraddress=args.mqttbrokeraddress, mqttbrokerport=args.mqttbrokerport)
    ddp.run()


if __name__ == '__main__':
    main()
