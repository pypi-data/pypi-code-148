""" Supervisor """
import json
import logging
import random
import subprocess
import threading
import time
from typing import Any
from typing import List
from typing import Optional

import dotenv
import pendulum
from gridworks.actor_base import ActorBase
from gridworks.enums import GNodeRole
from pydantic import BaseModel

import gwatn.config as config
from gwatn.data_classes.g_node import GNode
from gwatn.data_classes.g_node_instance import GNodeInstance
from gwatn.data_classes.supervisor_container import SupervisorContainer
from gwatn.enums import UniverseType
from gwatn.simple_atn_actor import SimpleAtnActor as Atn
from gwatn.types import GNodeGt_Maker
from gwatn.types import GNodeInstanceGt
from gwatn.types import GNodeInstanceGt_Maker
from gwatn.types import HeartbeatA
from gwatn.types import HeartbeatA_Maker
from gwatn.types import SimTimestep
from gwatn.types import SimTimestep_Maker
from gwatn.types import SuperStarter
from gwatn.types import SuperStarter_Maker


DATA_DIR = "input_data"
LOG_FORMAT = (
    "%(levelname) -10s %(asctime)s %(name) -30s %(funcName) "
    "-35s %(lineno) -5d: %(message)s"
)
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class Subordinate(BaseModel):
    Gni: GNodeInstanceGt
    Process: Any
    LastHeartbeatReceivedMs: int
    SubLastHex: str = "0"
    SuperLastHex: str = "0"


class SupervisorA(ActorBase):
    TIMEOUT_SECONDS = 7
    HB_SEND_SECONDS = 2.5

    def __init__(self, settings: config.SupervisorSettings, size: int):
        super().__init__(settings=settings)  # type: ignore
        self.settings: config.SupervisorSettings = settings
        self.super_starter: SuperStarter = self.get_dev_super_starter()
        scid = self.settings.supervisor_container_id
        gnid = self.settings.g_node_instance_id
        my_gnis: List[GNodeInstanceGt] = list(
            filter(
                lambda x: x.SupervisorContainerId == scid and x.GNodeInstanceId != gnid,
                self.super_starter.GniList,
            )
        )
        size = min(len(my_gnis), size)
        my_gnis = my_gnis[0:size]
        self.load_data_classes()
        self.my_flock: List[Subordinate] = list(
            map(
                lambda x: Subordinate(
                    Gni=x, Process=None, LastHeartbeatReceivedMs=int(time.time() * 1000)
                ),
                my_gnis,
            )
        )

        my_gni = list(
            filter(lambda x: x.GNodeInstanceId == gnid, self.super_starter.GniList)
        )[0]
        self.my_own_boss: Subordinate = Subordinate(
            Gni=my_gni,
            Process=None,
            LastHeartbeatReceivedMs=int(time.time() * 1000),
            SubLastHex="0",
            SuperLastHex="0",
        )
        LOGGER.info(f"Will be Supervising {size} Atns")
        self.main_thread: threading.Thread = threading.Thread(target=self.main)
        self.old_connections: List[Any] = []

    def load_data_classes(self) -> None:
        for gni in self.super_starter.GniList:
            gn = gni.GNode
            GNodeGt_Maker.tuple_to_dc(gn)
            if gni.SupervisorContainerId == self.settings.supervisor_container_id:
                GNodeInstanceGt_Maker.tuple_to_dc(gni)

    def get_dev_super_starter(self) -> SuperStarter:
        alias = self.settings.g_node_alias
        with open(f"{DATA_DIR}/dev_super_starter.json") as f:
            data = json.load(f)
        super_starter = SuperStarter_Maker.dict_to_tuple(data)
        if super_starter.SupervisorContainer.SupervisorGNodeAlias != alias:
            raise Exception(
                "file dev_super_starter.json was for supevisor "
                f"{super_starter.SupervisorContainer.SupervisorGNodeAlias},"
                f" not {alias}"
            )
        return super_starter

    def local_rabbit_startup(self) -> None:
        self.my_own_boss.LastHeartbeatReceivedMs = int(time.time() * 1000)
        self.my_own_boss.SubLastHex = "0"
        self.my_own_boss.SuperLastHex = str(random.choice("0123456789abcdef"))
        self.send_hb(self.my_own_boss)
        d = pendulum.from_timestamp(time.time())
        LOGGER.info(
            f"[{self.short_alias}] Sent first self HB: SuperLastHex {self.my_own_boss.SuperLastHex}, SubLastHex {self.my_own_boss.SubLastHex}:  {d.minute}:{d.second}.{d.microsecond}"
        )

    def local_start(self):
        self.main_thread.start()

    def local_stop(self):
        self.main_thread.join()
        for sub in self.my_flock:
            sub.Process.terminate()

    def start_subordinate(self, sub: Subordinate):
        gni = sub.Gni
        g_node_alias = gni.GNode.Alias
        g_node_id = gni.GNode.GNodeId
        g_node_instance_id = gni.GNodeInstanceId
        try:
            idx = self.super_starter.AliasWithKeyList.index(g_node_alias)
        except ValueError:
            raise Exception(f"{g_node_alias} not in AliasWithKeyList!")

        sk = self.super_starter.KeyList[idx]
        cmd = f"python run_atn.py {g_node_alias} {g_node_id} {g_node_instance_id} {sk}"
        sub.Process = subprocess.Popen(
            cmd.split(),
        )
        sub.LastHeartbeatReceivedMs = int(time.time() * 1000)
        sub.SuperLastHex = "0"
        sub.SubLastHex = "0"
        LOGGER.info(f"Starting {g_node_alias}")

    def refresh_own_channels(self):
        LOGGER.info("NEED TO REFRESH. TRY DELETING QUEUE")
        self.actor_main_stopped = True
        self._consume_channel.queue_delete(self.queue_name)

        time.sleep(0.5)
        try:
            self.stop_consumer()
        except:
            pass

        time.sleep(0.5)

        if self.consuming_thread.is_alive():
            self.old_connections.append(self._consume_connection)
            LOGGER.warning(f"OLD  CONNECTION IS ALIVE (old thread) ... INVESTIGATE!!")
        self.actor_main_stopped = False
        self.consuming_thread = threading.Thread(target=self.run_reconnecting_consumer)
        self.consuming_thread.start()

    def needs_a_whack(self, sub: Subordinate) -> bool:
        delta_ms = int(time.time() * 1000) - sub.LastHeartbeatReceivedMs
        if delta_ms > self.TIMEOUT_SECONDS * 1000:
            d = pendulum.from_timestamp(sub.LastHeartbeatReceivedMs / 1000)
            short_alias = sub.Gni.GNode.Alias.split(".")[-1]
            LOGGER.warning(
                f"Last {short_alias} hb: {d.minute}:{d.second}.{d.microsecond}, delta s: {round(delta_ms/1000, 2)}. {short_alias} NEEDS A WHACK"
            )
            return True
        return False

    def heartbeat_overdue(self, sub: Subordinate) -> bool:
        delta_ms = int(time.time() * 1000) - sub.LastHeartbeatReceivedMs
        if delta_ms > self.HB_SEND_SECONDS * 1000:
            return True
        return False

    def send_hb(self, sub: Subordinate) -> None:
        ping = HeartbeatA_Maker(
            my_hex=sub.SuperLastHex, your_last_hex=sub.SubLastHex
        ).tuple
        self.send_message(
            payload=ping,
            to_role=sub.Gni.GNode.Role,
            to_g_node_alias=sub.Gni.GNode.Alias,
        )

        LOGGER.debug(
            f"[{self.short_alias}] Sent HB: SuHex {ping.MyHex}, AtnHex {ping.YourLastHex}"
        )

    def main(self):
        for sub in self.my_flock:
            self.start_subordinate(sub)

        self.healthy: bool = True
        while (self.shutting_down is False) and (self.healthy is True):
            if self.needs_a_whack(self.my_own_boss):
                self.healthy is False
                self.refresh_own_channels()
                self.healthy = True
                return
            self.send_hb(self.my_own_boss)

            for sub in self.my_flock:
                if self.needs_a_whack(sub):
                    d = pendulum.from_timestamp(time.time())
                    short_alias = sub.Gni.GNode.Alias.split(".")[-1]
                    LOGGER.warning(
                        f"{d.minute}:{d.second}.{d.microsecond}: KILLING {short_alias}"
                    )
                    sub.Process.terminate()
                    sub.Process = None
                    self.start_subordinate(sub)
                    d = pendulum.from_timestamp(time.time())
                    LOGGER.warning(
                        f"{d.minute}:{d.second}.{d.microsecond}: DONE STARTING {short_alias}"
                    )
            for sub in self.my_flock:
                self.send_hb(sub)
            time.sleep(self.HB_SEND_SECONDS)

    ########################
    # Sends
    ########################

    def prepare_for_death(self) -> None:
        self.actor_main_stopped = True

    ########################
    # Receives
    ########################

    def route_message(
        self, from_alias: str, from_role: GNodeRole, payload: HeartbeatA
    ) -> None:
        if payload.TypeName == SimTimestep_Maker.type_name:
            try:
                self.timestep_from_timecoordinator(payload)
            except:
                LOGGER.exception("Error in timestep_from_timecoordinator")
        if payload.TypeName == HeartbeatA_Maker.type_name:
            try:
                self.heartbeat_a_received(from_alias, from_role, payload)
            except:
                LOGGER.exception("Error in heartbeat_a_received")
        else:
            LOGGER.info(f"Does not process TypeName {payload.TypeName}")
            return

    def heartbeat_a_received(
        self, from_alias: str, from_role: GNodeRole, payload: HeartbeatA
    ) -> None:
        if from_alias == self.alias:
            if payload.MyHex != self.my_own_boss.SuperLastHex:
                return
            next = str(random.choice("0123456789abcdef"))
            self.my_own_boss.SubLastHex = next
            self.my_own_boss.SuperLastHex = next
            self.my_own_boss.LastHeartbeatReceivedMs = int(time.time() * 1000)
            LOGGER.debug(f"Received Own HB: {payload.MyHex}")

        if from_alias not in self.my_flock_alias_list:
            return
        try:
            sub = list(
                filter(lambda x: x.Gni.GNode.Alias == from_alias, self.my_flock)
            )[0]
        except:
            LOGGER.warning(f"Issue finding Supervisee for {from_alias}")

        if payload.YourLastHex != sub.SuperLastHex:
            LOGGER.info("HB received out of order, ignoring")
            return

        # Update the sub
        prev_hb_ms = sub.LastHeartbeatReceivedMs
        sub.LastHeartbeatReceivedMs = int(time.time() * 1000)
        delta_ms = sub.LastHeartbeatReceivedMs - prev_hb_ms
        sub.SubLastHex = payload.MyHex
        sub.SuperLastHex = str(random.choice("0123456789abcdef"))
        LOGGER.debug(
            f"[{self.short_alias}] Valid Heartbeat received. DeltaMs {delta_ms}"
        )
        delta_ms = int(sub.LastHeartbeatReceivedMs - prev_hb_ms)
        if self.heartbeat_overdue(sub):
            self.send_hb(sub)

    def timestep_from_timecoordinator(self, payload: SimTimestep):
        if self._time == 0:
            self._time = payload.TimeUnixS
            self.new_timestep(payload)
            LOGGER.info(f"TIME STARTED: {self.time_str()}")
        elif self._time < payload.TimeUnixS:
            self._time = payload.TimeUnixS
            self.new_timestep(payload)
            LOGGER.debug(f"Time is now {self.time_str()}")
        elif self._time == payload.TimeUnixS:
            self.repeat_timestep(payload)

    def new_timestep(self, payload: SimTimestep) -> None:
        pass

    def repeat_timestep(self, payload: SimTimestep) -> None:
        pass

    def time(self) -> float:
        if self.universe_type == UniverseType.Dev:
            return self._time
        else:
            return time.time()

    def time_str(self) -> str:
        return pendulum.from_timestamp(self.time()).strftime("%m/%d/%Y, %H:%M")

    # @property
    # def latest_time_utc(self) -> Optional(pendulum.DateTime):
    #     if self.latest_time_unix_s is None:
    #         return None
    #     return pendulum.from_timestamp(self.latest_time_unix_s)

    @property
    def my_flock_alias_list(self) -> List[str]:
        return list(map(lambda x: x.Gni.GNode.Alias, self.my_flock))

    @property
    def short_alias(self) -> str:
        return self.alias.split(".")[-1]
