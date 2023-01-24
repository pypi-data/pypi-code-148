from SentioApi import SentioApi
from SentioApi.SentioTypes import *
import time
import logging

logging.basicConfig(format='[%(levelname)8s] [%(asctime)s] | %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %H:%M:%S')
logging.info("Starting Tests")

class TestClass:
    def init(self):
        returnValue = 0
        logging.debug("Initialize")
        #self.sentio_api = SentioApi.SentioModbus("192.168.188.14", _ModbusType = SentioApi.ModbusType.MODBUS_TCPIP)
        #self.sentio_api = SentioApi.SentioModbus("10.31.229.59", SentioApi.ModbusType.MODBUS_TCPIP)
        self.sentio_api = SentioApi.SentioModbus("/dev/ttyS5", SentioApi.ModbusType.MODBUS_RTU, 19200, 1, _loglevel=logging.DEBUG)
        #self.sentio_api = SentioApi.SentioModbus("192.168.188.14")
        if self.sentio_api.connect() == 0:
            #logging.error("---- Initializing device data start")
            if self.sentio_api.initializeDeviceData() == 0:
                logging.debug("Succesfully initialized Sentio device")
            else:
                returnValue = -1
        else:
            logging.error("Failed to connect!")
            returnValue = -1
        return returnValue

    def detectGlobalPeripherals(self):
        status = self.sentio_api.detectDHW()
        if status:
            logging.info("DHW device active")
        else:
            logging.info("DHW device not active")
        status = self.sentio_api.detectCMV()
        if status:
            logging.info("CMV device active")
        else:
            logging.info("CMV device not active")
        status = self.sentio_api.detectDehumidifiers()
        i = 0
        for s in status:
            i = i + 1
            if s == True:
                logging.info("Dehumidification {0} device active".format(i))
            else:
                logging.info("Dehumidification {0} device inactive".format(i))
        
    def readData(self):
        self.sentio_api.readDeviceData()
        #self.sentio_api.readCMVDeviceData()

    def cleanup(self):
        self.sentio_api.disconnect()
    
    def showRooms(self):
        rooms = self.sentio_api.getRooms()
        logging.info("-- available rooms:")
        for room in rooms:
            logging.info("-- {0}".format(room))
            logging.info("-- {0}".format(self.sentio_api.getRoomMode(room.index)))
            logging.info("-- Setpoint {0} °C".format(self.sentio_api.getRoomSetpoint(room.index)))
            logging.info("-- CurrTemp {0} °C".format(self.sentio_api.getRoomActualTemperature(room.index)))
            logging.info("-- RelHumid {0}%".format(self.sentio_api.getRoomRelativeHumidity(room.index)))
            logging.info("-- FloorTmp {0} °C".format(self.sentio_api.getRoomFloorTemperature(room.index)))
            logging.info("-- DewPoint {0} °C".format(self.sentio_api.getRoomCalculatedDewPoint(room.index)))
            logging.info("-- HeatingState = {0}".format(self.sentio_api.getRoomHeatingState(room.index)))
            
    def getoutdoorTemp(self):
        logging.info("Outdoor temp = {0}".format(self.sentio_api.getOutdoorTemperature()))

    def getRoomHeatingState(self, roomIndex):
        heatingState = self.sentio_api.getRoomHeatingState(roomIndex)
        logging.info("Room {0} state {1}".format(roomIndex, heatingState))
        return heatingState

    def getRoomMode(self, roomIndex):
        roomMode = self.sentio_api.getRoomMode(roomIndex)
        logging.info("Room {0} state {1}".format(roomIndex, roomMode))
        return roomMode

    def setRoomToSchedule(self, roomIndex):
        self.sentio_api.setRoomMode(roomIndex, SentioRoomMode.SCHEDULE)
        pass
    
    def setRoomToManual(self, roomIndex):
        self.sentio_api.setRoomMode(roomIndex, SentioRoomMode.MANUAL)
        pass

    def setRoomTemperature(self, roomIndex, temperatureSetpoint):
        self.sentio_api.setRoomSetpoint(roomIndex, temperatureSetpoint)



#Execute Tests
testInstance = TestClass()
assert testInstance.init() == 0, "Failed to connect"
testInstance.readData()
testInstance.detectGlobalPeripherals()

#Show rooms
testInstance.getoutdoorTemp()
testInstance.showRooms()
roomToSet = 0
testInstance.setRoomToSchedule(roomToSet)
assert testInstance.getRoomMode(roomToSet) == SentioRoomMode.SCHEDULE, "ERROR -  Failing to set to schedule"
testInstance.showRooms()
testInstance.setRoomTemperature(roomToSet, 19.5)

testInstance.setRoomToManual(roomToSet)
time.sleep(0.2)
assert testInstance.getRoomMode(roomToSet) == SentioRoomMode.MANUAL, "ERROR -  Failing to set to Manual"
testInstance.showRooms()

#set back
logging.info("========= CLEANUP ==============")
testInstance.setRoomToSchedule(3)
testInstance.setRoomToManual(0)
testInstance.showRooms()

#cleanup
testInstance.cleanup()