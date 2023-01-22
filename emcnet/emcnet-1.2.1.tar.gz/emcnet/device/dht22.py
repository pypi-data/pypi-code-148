import sys
import time
from device.Adafruit_DHT_Em import DHT
import datetime
import argparse
from device.device_socket import DeviceSocket

gateway_address_default='localhost' # string containing address of gateway
gateway_port_default=10000          # string containing TCP port identifier for gateway
samples_per_hour_default = 60       # integer samples per hour to report to gatway


def run(device_id, pin=16, gateway_address='localhost', gateway_port=10000, samples_per_hour=60, emulate=False):
    ds = None
    try:
        print("Opening socket to gateway...")
        ds = DeviceSocket(device_id=device_id, gateway_address=gateway_address, gateway_port=gateway_port)

        print('Bringing up DHT22 device ID {}.'.format(device_id))
        dht = DHT(emulate=emulate)
        # tell_gateway('detach')
        # tell_gateway('attach')

        seconds_per_sample = 60.0 * 60.0 / samples_per_hour
        dt = datetime.datetime.now()
        last_interval = int((dt.hour * 60 * 60 + dt.minute * 60 + dt.second) / seconds_per_sample)
        while True:
            # Check if it time to do something
            dt = datetime.datetime.now()
            interval = int((dt.hour * 60 * 60 + dt.minute * 60 + dt.second) / seconds_per_sample)
            if interval != last_interval:
                # began a new time interval
                try:
                    h, t = dht.read_retry(22, pin)
                except RuntimeError as error:
                    print(error)
                    print('Did you specify the correct sensor pin? Did you run with root privileges to access GPIO?')
                    raise RuntimeError
                else:
                    h = "{:.1f}".format(h)
                    t = "{:.1f}".format(t)
                    data_to_send = {"ts": "{}".format(dt.replace(microsecond=0).isoformat()), "temperature": t,
                                    "humidity": h}
                    print(f"Pushing to gateway: {data_to_send}")
                    ds.message_gateway('event', data=data_to_send)
                    last_interval = interval
                    sys.stdout.flush()
            else:
                time.sleep(0.2)

    finally:
        print('Closing socket...')
        if ds is not None:
            ds.close()
        print('Stopped.')


def main():
    parser = argparse.ArgumentParser(description=(
        'DHT-22 weather device, e.g. https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf'))
    parser.add_argument('--pin', default=16, help='GPIO pin (default=16)')
    parser.add_argument('device_id', help='Cloud IoT Core device id (default=dh22)', default='dh22')
    parser.add_argument('--gateway_address', default=gateway_address_default, help='web address of IoT gateway',
                        type=str)
    parser.add_argument('--gateway_port', default=gateway_port_default, help='TCP port of IoT gateway',
                        type=int)
    parser.add_argument('--sph', default=60, help='samples per hour (default=False)', type=float)
    parser.add_argument('--emulate', action='store_true', help='emulate measurements (default=False)')
    args = parser.parse_args()
    run(args.device_id, pin=args.pin, gateway_address=args.gateway_address, gateway_port=args.gateway_port,
        samples_per_hour=args.sph, emulate=args.emulate)


if __name__ == '__main__':
    main()
