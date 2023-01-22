import argparse
from emcnet.emcnet_data_publisher import MQTTDataPublisher
import emcnet.device.vedirect_types as vedirect_types
from vedirect import VEDirect
import json
import sys
import logging
import fieldday
import time
from dotenv import load_dotenv
import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import Point
from emcnet.emcnet_data_store import EMCNETDataStore

# from bigbird.intervalmgr import IntervalMgr
log = logging.getLogger(__name__)

# load environment variables for package config
load_dotenv()

devicename_default = 'vmppt_0000'
serial_port_default = '/dev/serial/by-id/usb-FTDI_FT232EX-if00-port0'


class VMPPTMonitor:

    def __init__(self, port=serial_port_default, emulate=False, mqttbrokeraddress='localhost', mqttbrokerport=1883,
                 id=None, every=1):
        if emulate:
            emulate_str = 'MPPT'
        else:
            emulate_str = ''
        log.info(f"Instantiating Victron Direct Device Monitor")
        self.id = id
        self.victrondirectdevicemonitor = VEDirect(port, emulate=emulate_str)
        self.mqttbrokeraddress = mqttbrokeraddress
        if emulate:
            self.measurement = "vmppt_emulate"
        else:
            self.measurement = "vmppt"
        if self.mqttbrokeraddress:
            log.info(f"Instantiating MQTT Device Data Publisher")
            self.ddp = MQTTDataPublisher(self.measurement, id=id, 
                                         mqttbrokeraddress=mqttbrokeraddress, mqttbrokerport=mqttbrokerport)
        self.every = every
        self.sequence_number = 0
        self.topic = "emcnet/" + self.measurement
        if id:
            if isinstance(id, str):
                self.topic = self.topic + "/" + id.strip()
            else:
                log.error("id is not a string")
                raise Exception("id must be a string")
        else:
            # could look for ID in the payload but not sure this is the best design
            pass
        
    def handle_record(self, datarecord: dict):
        self.sequence_number = self.sequence_number + 1
        if (self.sequence_number % self.every) == 0:
            fieldday.rename_keys(datarecord, vedirect_types.keyName)
            newrecord = dict()
            newrecord["time"] = time.time_ns()
            newrecord["measurement"] = self.measurement
            newrecord["fields"] = datarecord
            if self.id:
                if not "tags" in newrecord:
                    newrecord["tags"] = dict()
                newrecord["tags"]["id"] = self.id                
            log.debug(f"Storing: {newrecord}")
            # publish the record
            if self.mqttbrokeraddress:
                # publish record to MQTT broker
                self.ddp.publish(newrecord)
            else:
                # print the data to stdout
                print(json.dumps(newrecord))
                sys.stdout.flush()  # important - otherwise when piping, Python may buffer this output for some reason
            pass
            self.sequence_number = 0            
            # restart the sequence
            self.sequence_number = 0

    def run(self, n):
        self.victrondirectdevicemonitor.read_data_callback(self.handle_record, n)


def main():
    # set the default path to the EMCNET directory - from the environment if set
    emcnetdir = os.getenv("EMCNET_DIR", '/etc/emcnet').rstrip('/')
    load_dotenv(emcnetdir + '/config.env', override=True)
    # read command-line arguments and override environment variables if given
    parser = argparse.ArgumentParser(description=(
        'Victron MPPT device interface - reveives and forwards MPPT charge controller data via MQTT or stdout'))
    parser.add_argument('--port', default=serial_port_default, help='Serial port to listen for VEDirect MPPT messages')
    parser.add_argument('--mqttbrokeraddress', help='MQTT broker address', type=str,
                        default=os.getenv("MQTT_BROKER_ADDRESS", 'localhost'))
    parser.add_argument('--mqttbrokerport', help='MQTT broker port', type=int,
                        default=os.getenv("MQTT_BROKER_PORT", 1883))
    parser.add_argument('--loglevel', help='logging level one of [DEBUG, INFO, WARNING, ERROR, CRITICAL]',
                        default=os.getenv("EMCNET_LOG_LEVEL", 'INFO'))
    parser.add_argument('--emulate', action='store_true', help='emulate measurements (default=False)')
    parser.add_argument('--every', default=1, help='transmit every <every> record', type=int)
    parser.add_argument('--n', default=-1, help='number of raw records to read and print', type=int)
    parser.add_argument('--id', help='Override id in the payload (e.g. "12345", "vanbattery", etc...)', type=str)
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel.upper())
    log.info("Victron MPPT device interface - stores json measurements in the influx database")
    if args.emulate:
        log.info("EMULATION MODE")
    log.info(f"VMPPT port: {args.port}")        
    log.info(f"EMCNet directory: {emcnetdir}")
    log.info(f"MQTT Broker: {args.mqttbrokeraddress}")
    log.info(f"Every: {args.every}")
    log.info(f"Device/Measurement: vmppt")
    if args.id:
        log.info(f"ID: {args.id}")
    vm = VMPPTMonitor(args.port, emulate=args.emulate, mqttbrokeraddress=args.mqttbrokeraddress,
                      mqttbrokerport=args.mqttbrokerport, id=args.id, every=args.every)
    vm.run(args.n)


if __name__ == '__main__':
    main()
