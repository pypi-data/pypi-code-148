import argparse
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

devicename_default = 'vmppt'
serial_port_default = '/dev/serial/by-id/usb-FTDI_FT232EX-if00-port0'


class VMPPTMonitor:

    def __init__(self, influxorg, influxedgeurl, influxedgetoken, port, device=None, emulate='', every=1):
        if emulate:
            emulate = 'MPPT'
        else:
            emulate = ''
        log.info(f"Instantiating Victron Direct Device Monitor")
        self.victrondirectdevicemonitor = VEDirect(port, emulate=emulate)
        log.info(f"Instantiating InfluxDB Device Data Store")
        self.dds = EMCNETDataStore(influxorg, influxedgeurl, influxedgetoken, device)
        self.every = every
        self.sequence_number = 0

    def handle_record(self, datarecord: dict):
        self.sequence_number = self.sequence_number + 1
        if (self.sequence_number % self.every) == 0:
            fieldday.rename_keys(datarecord, vedirect_types.keyName)
            newrecord = dict()
            newrecord["time"] = time.time_ns()
            newrecord["fields"] = datarecord            
            log.debug(f"Storing: {newrecord}")
            # store data
            self.dds.store(newrecord)
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
        'Victron MPPT device interface - stores json measurements in the influx database'))
    parser.add_argument('--influxorg', type=str, default=os.getenv("EMCNET_INFLUX_ORG", 'emcnet'), 
                        help='InfluxDB org (usually emcnet)')
    parser.add_argument('--influxedgeurl', type=str, default=os.getenv("EMCNET_INFLUX_EDGE_URL", 'http://localhost:8086'), 
                        help='InfluxDB edge url (usually http://localhost:8086)')    
    parser.add_argument('--influxedgetoken', type=str, default=os.getenv("EMCNET_INFLUX_EDGE_TOKEN", 'unknown_token'), 
                        help='InfluxDB edge token')    
    parser.add_argument('--device', help='Override Unique Device Name (e.g. "ina226_12345", "dht22_45678", etc...)', type=str)
    parser.add_argument('--loglevel', help='logging level one of [DEBUG, INFO, WARNING, ERROR, CRITICAL]',
        default=os.getenv("EMCNET_LOG_LEVEL", 'INFO'))
    parser.add_argument('--port', default=serial_port_default, help='Serial port to listen for VEDirect MPPT messages')
    parser.add_argument('--emulate', action='store_true', help='emulate measurements (default=False)')
    parser.add_argument('--every', default=1, help='transmit every <every> record', type=int)
    parser.add_argument('--n', default=-1, help='number of raw records to read and print', type=int)
 
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel.upper())
    log.info("Victron MPPT device interface - stores json measurements in the influx database")
    if args.emulate:
        log.info("EMULATION MODE")
    log.info(f"VMPPT port: {args.port}")
    log.info(f"EMCNet directory: {emcnetdir}")
    log.info(f"Influx Org: {args.influxorg}")
    log.info(f"Influx Edge URL: {args.influxedgeurl}")
    if args.device is not None:
        log.info(f"Device/Measurement: {args.device}")
    vm = VMPPTMonitor(args.influxorg, args.influxedgeurl, args.influxedgetoken, args.port, device=args.device, 
                      emulate=args.emulate, every=args.every)
    vm.run(args.n)


if __name__ == '__main__':
    main()
