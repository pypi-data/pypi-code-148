"""
Usage:
------

    $ p1read [options]

Available options are:

    -h, --help          Show this help
    -d, --device        Name of serial device to read from
    -l, --loop          Endless loop
    -c, --clear         Clear screen during loop


Contact:
--------

- https://github.com/niels-sterrenburg

More information is available at:

- https://github.com/niels-sterrenburg/p1read
- https://www.netbeheernederland.nl
- https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf

"""
# Standard library imports
import sys
import serial
import os
import getopt
clear = lambda: os.system('clear')

# p1read
from p1read import p1

def usage():
    printf("Usage:\n\n\t %s [-d /dev/ttyUSBx -l] \n\n", os.path.basename(sys.argv[0]))
    printf("\t\t-d or --device\t\tSerial device to read from (default /dev/ttyUSB0\n")
    printf("\t\t-l or --loop\t\tContinues read in a loop\n")
    printf("\t\t-c or --clear\t\tClear the screen in the loop\n")
    printf("\n")


def main() -> None:
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hlcd:", ["help", "device="])
    except getopt.GetoptError as err:
        print(err) 
        usage()
        raise SystemExit()

    # Parse options
    serial_port="/dev/ttyUSB0"
    optloop=False
    optclear=False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            raise SystemExit()
        elif opt in ("-l", "--loop"):
            optloop = True
        elif opt in ("-c", "--clear"):
            optclear = True
        elif opt in ("-d", "--device"):
            serial_port = arg
        else:
            assert False, "unhandled option"

    # read
    if optloop:
        while True:
            p1.read(serial_port)
            if optclear:
                clear()
            p1.dump()
    else:
        p1.read(serial_port)
        p1.dump()


if __name__ == "__main__":
    main()

