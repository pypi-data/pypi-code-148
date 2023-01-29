import sys
import serial
import os
import re

##############################################################################
# Sentimentally define printf :'( because we can :D
##############################################################################
def printf(format, *args):
    sys.stdout.write(format % args)

##############################################################################
# Class for P1 data elements
##############################################################################
class P1:
    order  = 0
    floval = 0.0
    intval = -1
    strval = ""
    todb   = 0
    dbname = ""
    iden   = ""
    form   = ""
    unit   = ""
    desc   = ""

    def __init__(self, order, floval, intval, strval, todb, dbname, iden, form, unit, desc):
        self.order  = order
        self.floval = floval
        self.intval = intval
        self.strval = strval
        self.todb   = todb
        self.dbname = dbname
        self.iden   = iden  
        self.form   = form  
        self.unit   = unit  
        self.desc   = desc  

##############################################################################
# Array for P1 class objects
##############################################################################
P1D = []

####################################################################################################
standard_version = "v5.02"
standard_source  = "https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf"
####################################################################################################
#              <--value-->  DB DBname                   OBI            Format      Unit   Description
P1D.append(P1( 0, 0.0, -1, '', 1, "version             ",  '1-3:0.2.8',   'str',      '',    'Version information for P1 output'))
P1D.append(P1( 0, 0.0, -1, '', 1, "timestamp           ",  '0-0:1.0.0',   'datetime', '',    'Date-time stamp of the P1 message (YYMMDDhhmmss)'))
P1D.append(P1( 0, 0.0, -1, '', 0, "                    ",  '0-0:96.1.1',  'str',      '',    'Equipment identifier'))
P1D.append(P1( 0, 0.0, -1, '', 1, "totalusagenight     ",  '1-0:1.8.1',   'flo',      'kWh', 'Meter Reading electricity delivered to client (Tariff 1) in 0,001 kWh'))
P1D.append(P1( 0, 0.0, -1, '', 1, "totalusageday       ",  '1-0:1.8.2',   'flo',      'kWh', 'Meter Reading electricity delivered to client (Tariff 2) in 0,001 kWh'))
P1D.append(P1( 0, 0.0, -1, '', 1, "totaldeliverynight  ",  '1-0:2.8.1',   'flo',      'kWh', 'Meter Reading electricity delivered by client (Tariff 1) in 0,001 kWh'))
P1D.append(P1( 0, 0.0, -1, '', 1, "totaldeliveryday    ",  '1-0:2.8.2',   'flo',      'kWh', 'Meter Reading electricity delivered by client (Tariff 2) in 0,001 kWh'))
P1D.append(P1( 0, 0.0, -1, '', 1, "tarif               ",  '0-0:96.14.0', 'int',      '',    'Tariff indicator electricity (Tariff 1: low Tariff 2: normal).'))
P1D.append(P1( 0, 0.0, -1, '', 1, "actualusage         ",  '1-0:1.7.0',   'flo',      'kW',  'Actual electricity power delivered (+P) in 1 Watt resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "actualdelivery      ",  '1-0:2.7.0',   'flo',      'kW',  'Actual electricity power received (-P) in 1 Watt resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "failures            ",  '0-0:96.7.21', 'int',      '',    'Number of power failures in any phase'))
P1D.append(P1( 0, 0.0, -1, '', 1, "longfailures        ",  '0-0:96.7.9',  'int',      '',    'Number of long power failures in any phase'))
P1D.append(P1( 0, 0.0, -1, '', 0, "                    ",  '1-0:99.97.0', 'str',      '',    'Power Failure Event Log (long power failures)'))
P1D.append(P1( 0, 0.0, -1, '', 1, "voltagesagsL1       ",  '1-0:32.32.0', 'int',      '',    'Number of voltage sags in phase L1'))
P1D.append(P1( 0, 0.0, -1, '', 1, "voltagesagsL2       ",  '1-0:52.32.0', 'int',      '',    'Number of voltage sags in phase L2'))
P1D.append(P1( 0, 0.0, -1, '', 1, "voltagesagsL3       ",  '1-0:72.32.0', 'int',      '',    'Number of voltage sags in phase L3'))
P1D.append(P1( 0, 0.0, -1, '', 1, "voltageswellsL1     ",  '1-0:32.36.0', 'int',      '',    'Number of voltage swells in phase L1'))
P1D.append(P1( 0, 0.0, -1, '', 1, "voltageswellsL2     ",  '1-0:52.36.0', 'int',      '',    'Number of voltage swells in phase L2'))
P1D.append(P1( 0, 0.0, -1, '', 1, "voltageswellsL3     ",  '1-0:72.36.0', 'int',      '',    'Number of voltage swells in phase L3'))
P1D.append(P1( 0, 0.0, -1, '', 0, "                    ",  '0-0:96.13.0', 'str',      '',    'Text message max 1024 characters.'))
P1D.append(P1( 0, 0.0, -1, '', 1, "voltL1              ",  '1-0:32.7.0',  'flo',      'V',   'Instantaneous voltage L1 in V resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "voltL2              ",  '1-0:52.7.0',  'flo',      'V',   'Instantaneous voltage L2 in V resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "voltL3              ",  '1-0:72.7.0',  'flo',      'V',   'Instantaneous voltage L3 in V resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "ampsL1              ",  '1-0:31.7.0',  'flo',      'A',   'Instantaneous current L1 in A resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "ampsL2              ",  '1-0:51.7.0',  'flo',      'A',   'Instantaneous current L2 in A resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "ampsL3              ",  '1-0:71.7.0',  'flo',      'A',   'Instantaneous current L3 in A resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "usageL1             ",  '1-0:21.7.0',  'flo',      'kW',  'Instantaneous active power L1 (+P) in W resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "usageL2             ",  '1-0:41.7.0',  'flo',      'kW',  'Instantaneous active power L2 (+P) in W resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "usageL3             ",  '1-0:61.7.0',  'flo',      'kW',  'Instantaneous active power L3 (+P) in W resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "deliveryL1          ",  '1-0:22.7.0',  'flo',      'kW',  'Instantaneous active power L1 (-P) in W resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "deliveryL2          ",  '1-0:42.7.0',  'flo',      'kW',  'Instantaneous active power L2 (-P) in W resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "deliveryL3          ",  '1-0:62.7.0',  'flo',      'kW',  'Instantaneous active power L3 (-P) in W resolution'))
P1D.append(P1( 0, 0.0, -1, '', 1, "GasDeviceType       ",  '0-1:24.1.0',  'int',      '',    'GasDeviceType'))
P1D.append(P1( 0, 0.0, -1, '', 1, "GasEquipmentID      ",  '0-1:96.1.0',  'str',      '',    'GasEquipmentID'))
P1D.append(P1( 0, 0.0, -1, '', 1, "GasLastTimestamp    ",  '0-1:24.2.1',  'str',      '',  'GasLastFiveMinTime'))
P1D.append(P1( 1, 0.0, -1, '', 1, "GasLastValue        ",  '0-1:24.2.1',  'str',      'kW',  'GasLastFiveMinVal'))
# TODO add water

##############################################################################
# Serial read
##############################################################################

# Default config
ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize=serial.EIGHTBITS
ser.parity=serial.PARITY_NONE
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20

def serial_open(port):
    # Open COM port
    try:
        ser.port = port
        ser.open()
    except:
        sys.exit ("Cannot open serial device:" % ser.name)      

def serial_read():
    try:
        raw = ser.readline()
    except:
        sys.exit ("Cannot read serial device:" % ser.name )      
    line = str(raw)
    return line.strip()

##############################################################################
# Parse serial line to P1 data
##############################################################################

def parse_line(line):
   # Example data: b'1-0:62.7.0(00.000*kW)\r\n'
   # Example data: b'1-0:62.7.0(timeW)(value)\r\n'

   line=line.replace("b'","")
   line=line.replace("\\r\\n'","")

   # Split line obi from data #TODO regexp in perl were so much easier ;'(
   a=line.split("(")
   obi = a[0]

   # Get all data values
   val = re.findall(r'\(.*?\)', line)
   
   for i in range(len(val)):
       val[i] = val[i].replace("(","").replace(")","")
       if '*' in val[i]:
           val[i] = val[i].split("*")[0]

   # check if obi is recognized and update the object with data
   for item in P1D:
       if item.iden == obi:
           if item.form == "flo":
               item.floval = float(val[item.order])
           if item.form == "int":
               item.intval = int(val[item.order])
           if item.form == "datetime":
               item.strval = val[item.order]           # TODO convert to databse time format
           if item.form == "str":
               item.strval = val[item.order]



def read(port):
    if not hasattr(read, "open"):
        serial_open(port)
        read.open = True

    # read one full telegram
    while True:
        line = serial_read()
        if len(line) > 2 and line[2] == "!":
            break
        else:
            parse_line(line)
 

##############################################################################
# Print to stdout
##############################################################################

def dump():
   printf("%-20s%-15s%-10s%-80s\n\n", "P1 Monitor", "P1 Standard:", standard_version, standard_source)
   printf("%-20s%-15s%-10s%-80s\n", "=====","======","=====","============")
   printf("%-20s%-15s%-10s%-80s\n", "Item", "Value", "Unit", "Description")
   printf("%-20s%-15s%-10s%-80s\n", "=====","======","=====","============")
   for item in P1D:
       if item.todb:
           val = item.strval
           if item.form == "flo":
               val = str(item.floval)
           if item.form == "int":
               val = str(item.intval)
           if item.form == "datetime":
               val = item.strval

           # if string is > 14 characters, chop it by 10 and add 3 dots
           pval = (val[:10] + '...') if len(val) > 14 else val 
  
           printf("%-20s%-15s%-10s%-80s\n", item.dbname, pval, item.unit, item.desc)


