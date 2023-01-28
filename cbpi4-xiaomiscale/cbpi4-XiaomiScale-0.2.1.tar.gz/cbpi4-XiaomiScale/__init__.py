# -*- coding: utf-8 -*-
import asyncio
import logging

import scapy.all as scapy

from cbpi.api import *
from cbpi.api import parameters, Property, action
from cbpi.api.step import StepResult, CBPiStep
from cbpi.api.timer import Timer
from cbpi.api.dataclasses import NotificationType

logger = logging.getLogger(__name__)

TIMOUT_INTERVAL = 0.5


def extract_unit(data):
    ### Xiaomi V1 Scale ###
    measunit = data[4:6]
    unit = "fault"
    if data.startswith('1d18'):
        if measunit.startswith(('03', 'a3')):
            unit = 'lbs'
        if measunit.startswith(('12', 'b2')):
            unit = 'jin'
        if measunit.startswith(('22', 'a2', '02')):
            unit = 'kg'

    ### Xiaomi V2 Scale ###
    if data.startswith('1b18'):
        if measunit == "03":
            unit = 'lbs'
        if measunit == "02":
            unit = 'kg'

    return unit


def extract_weight(data):
    ### Xiaomi V1 Scale ###
    measured = -1
    if data.startswith('1d18'):
        measured = int((data[8:10] + data[6:8]), 16) * 0.01

    ### Xiaomi V2 Scale ###
    if data.startswith('1b18'):
        measured = int((data[28:30] + data[26:28]), 16) * 0.01

    return measured / 2


class BluetoothListener(scapy.BluetoothHCISocket):
    def __init__(self, dev_mac):
        super(BluetoothListener, self).__init__(0)
        self.dev_mac = dev_mac
        self.__sr_hci_msg(scapy.HCI_Cmd_LE_Set_Scan_Parameters(type=1))

    def __sr_hci_msg(self, msg):
        return self.sr(scapy.HCI_Hdr() / scapy.HCI_Command_Hdr() / msg, timeout=0.001)

    def __ble_listen(self):
        self.__sr_hci_msg(scapy.HCI_Cmd_LE_Set_Scan_Enable(enable=True, filter_dups=False))
        adverts = self.sniff(lfilter=lambda p: scapy.HCI_LE_Meta_Advertising_Reports in p, timeout=TIMOUT_INTERVAL)
        # todo change timeout to min
        self.__sr_hci_msg(scapy.HCI_Cmd_LE_Set_Scan_Enable(enable=False))
        return adverts

    def __get_clean_packet(self, report):
        if report.addr == self.dev_mac.lower():
            for pkt in report.data:
                if pkt.type == 0x16:  # 0x16 == svc_data_16_bit_uuid
                    yield scapy.hexdump(pkt[1], True).replace(" ", "").lower()[
                          4:34]  # pkt[1] is the layer containing the data
                continue

    def read_unit(self):
        data = self.__ble_listen()

        for pkt in data:
            reports = pkt[scapy.HCI_LE_Meta_Advertising_Reports].reports
            for report in reports:
                for pkt_data in self.__get_clean_packet(report):
                    return extract_unit(pkt_data)

    def read_info(self):
        data = self.__ble_listen()

        for pkt in data[::-1]:
            reports = pkt[scapy.HCI_LE_Meta_Advertising_Reports].reports
            for report in reports[::-1]:
                for pkt_data in self.__get_clean_packet(report):
                    return extract_weight(pkt_data)


@parameters([Property.Text(label="Scale mac", configurable=True, default_value="",
                           description="The mac address of the Xiaomi scale."),
             Property.Number(label="Offset", configurable=True, default_value=0,
                             description="The difference between the measured 0 and actual 0."),
             Property.Number(label="Gravity", configurable=True, default_value=1.000,
                             description="The Gravity of the liquid."),
             Property.Select(label="Display type", options=["Volume", "Weight"],
                             description="The desired unit type to display (default=Volume)"),
             Property.Select(label="Disable Sensor", options=["Enable", "Disable"],
                             description="The desired unit type to display (default=Volume)")])
class XiaomiScale(CBPiSensor):

    def __init__(self, cbpi, id, props):
        super(XiaomiScale, self).__init__(cbpi, id, props)
        self.enabled = self.props.get("Disable Sensor", "Enable") == "Enable"
        self.scale_mac = self.props.get("Scale mac", "XX:XX:XX:XX:XX:XX")
        self.orig_offset = self.props.get("Offset", 0)
        self.gravity = float(self.props.get("Gravity", 1))
        if self.gravity == 0:
            logging.warning(f"{self.gravity} is an illegal gravity value, setting gravity to 1")
            self.gravity = 1
        self.disp_unit = self.cbpi.config.get("Water volume unit", "L")
        self.disp_vol = self.props.get("Display type", "Volume") == "Volume"

        self.weight = 0
        self.value = 0
        self.offset = float(self.orig_offset)

        if self.enabled:
            self.bt_soc = BluetoothListener(self.scale_mac)
            self.weight_unit = self.bt_soc.read_unit()

    @action(key="Tare", parameters=[])
    async def tare(self, offset=None, **kwargs):
        logging.info("Tare")
        if offset is not None:
            logging.info(f"Offset {offset} was given")
            self.offset += float(offset)
        else:
            self.offset += self.weight
        logger.info("Tare Performed")

    @action(key="Change Gravity", parameters=[Property.Number(label="gravity", configurable=True, default_value=1,
                                                              description="Gravity in SG")])
    async def change_gravity(self, gravity=1, **kwargs):
        if gravity == 0:
            logger.warning(f"Illegal gravity value, gravity remained {self.gravity}")
            return
        self.gravity = float(gravity)
        logger.info(f"Gravity Changed to {self.gravity}")

    @action(key="Reset", parameters=[])
    async def reset(self):
        logging.info("reset")
        self.offset = float(self.orig_offset)
        if self.enabled:
            self.bt_soc = BluetoothListener(self.scale_mac)

    @action(key="Toggle State", parameters=[])
    async def toggle_state(self):
        if self.enabled:
            logging.info("Disabled")
        else:
            logging.info("Enabled")
        self.enabled = not self.enabled
        await self.reset()

    def get_unit(self):
        return self.weight_unit

    def weight2kg(self):
        if self.weight_unit == "lbs":
            return self.weight * 0.4535924
        if self.weight_unit == "jin":
            return self.weight * 0.5
        return self.weight

    def convert(self, weight):
        vol = weight / self.gravity
        if self.disp_unit == "gal(us)":
            vol *= 0.264172052
        elif self.disp_unit == "gal(uk)":
            vol *= 0.219969157
        elif self.disp_unit == "qt":
            vol *= 1.056688
        return vol

    async def run(self):
        while self.running:
            if self.enabled:
                reading = self.bt_soc.read_info()
                if reading is not None:
                    self.weight = float(reading) - self.offset
                    if self.disp_vol:
                        volume = self.convert(self.weight2kg())
                        self.value = float(volume)
                    else:
                        self.value = self.weight
                    self.push_update(self.value)
            await asyncio.sleep(0.5)

    def get_state(self):
        return dict(value=self.value)


@parameters([Property.Number(label="Volume", description="Volume limit for this step", configurable=True),
             Property.Actor(label="Actor", description="Actor to switch media flow on and off"),
             Property.Sensor(label="Sensor"),
             Property.Select(label="Reset", options=["Yes", "No"], description="Reset Sensor when done")])
class FillStep(CBPiStep):

    async def on_timer_done(self, timer):
        self.summary = ""
        self.cbpi.notify(self.name,
                         'Step finished. Transferred {} {}.'.format(round(self.current_volume, 2), self.unit),
                         NotificationType.SUCCESS)
        if self.resetsensor == "Yes":
            self.sensor.instance.reset()

        if self.actor is not None:
            await self.actor_off(self.actor)
        await self.next()

    async def on_timer_update(self, timer, seconds):
        await self.push_update()

    async def on_start(self):
        self.unit = self.cbpi.config.get("Water volume unit", "L")
        self.actor = self.props.get("Actor", None)
        if self.actor is not None:
            await self.actor_off(self.actor)

        self.target_volume = float(self.props.get("Volume", 0))
        self.vol_sensor = self.props.get("Sensor", None)
        self.sensor = self.get_sensor(self.vol_sensor)
        self.resetsensor = self.props.get("Reset", "Yes")
        self.sensor.instance.reset()
        self.start_weight = self.sensor.instance.value
        if self.timer is None:
            self.timer = Timer(1, on_update=self.on_timer_update, on_done=self.on_timer_done)

    async def on_stop(self):
        if self.timer is not None:
            await self.timer.stop()
        self.summary = ""
        if self.actor is not None:
            await self.actor_off(self.actor)
        await self.push_update()

    async def reset(self):
        self.timer = Timer(1, on_update=self.on_timer_update, on_done=self.on_timer_done)
        if self.actor is not None:
            await self.actor_off(self.actor)
        if self.resetsensor == "Yes":
            self.sensor.instance.reset()

    async def run(self):
        if self.actor is not None:
            await self.actor_on(self.actor)
        self.summary = ""
        await self.push_update()
        while self.running:
            self.current_volume = self.get_sensor_value(self.vol_sensor).get("value")
            self.summary = "Volume: {:.3f}".format(self.current_volume)
            await self.push_update()

            if self.current_volume >= self.target_volume and self.timer.is_running is not True:
                self.timer.start()
                self.timer.is_running = True

            await asyncio.sleep(0.2)

        return StepResult.DONE


def setup(cbpi):
    cbpi.plugin.register("XiaomiScale", XiaomiScale)
    cbpi.plugin.register("FillStep", FillStep)
