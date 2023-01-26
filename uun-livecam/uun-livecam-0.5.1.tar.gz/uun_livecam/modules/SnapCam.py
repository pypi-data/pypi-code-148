"""
Make a tour with IP cam and send snapshots to a server.
"""

from uun_iot.utils import get_iso_timestamp
from uun_iot import Module, on
from uun_livecam.onvif import SnapSequence

import threading
import datetime
import time
import os

import logging
logger = logging.getLogger(__name__)

# wsdl path relative to this file located in 'modules/SnapCam.py'
# wsdl data will be stored in package folder together with .py files
wsdl_path = os.path.abspath(os.path.dirname(__file__)) + "/../wsdl"

class SnapCam(Module):
    id = "snapCam"

    def __init__(self, config, uucmd):
        super().__init__(config=config, uucmd=uucmd)

        # dict for storing all cams in format {cam_id: snapsequence object}
        self._cameras = {}
        self._init_camera()

        # indicate whether there is a tour in progress, so that it is not interrupted by another tour
        self._tour_lock = threading.Lock()
        
        # indicate whether there is an (configuration) update in progress to prevent waiting in queue and updating multiple times
        self._update_lock = threading.Lock()

    def _init_camera(self, cid=None):
        """ Initialize camera object(s). """
        def __init_camera(cid):
            cam = self._c(cid)
            self._cameras[cid] = None
            try:
                self._cameras[cid] = SnapSequence(
                    ip=cam['onvif']['ip'],
                    port=cam['onvif']['port'],
                    user=cam['onvif']['user'],
                    password=cam['onvif']['password'],
                    wsdl=wsdl_path,
                    positions=cam['tour']
                )
                return True
            except Exception as e:
                logger.warning("Exception occured when initializing camera [%s].", cid)
                logger.debug("Exception: %s", e)
                return False

        if cid is None:
            for cid in self._c():
                __init_camera(cid)
        else:
            return __init_camera(cid)

    @on("tick")
    def start_cam_tour(self):
        """
        Make every camera take a predefined tour and send images after each snapshot.
        """

        if self._tour_lock.locked():
            logger.warning("Tour is already in progress. wait until tours for all cameras are finished.")
            return
        
        with self._tour_lock:

            # async loop over all cameras (join all threads in the end)
            # send images as async callback after completing the snapshot
            threads = []
            for cam_id, cam in self._cameras.items(): 
                if cam is None:
                    logger.debug("Trying to reiinit camera `%s`...", cam_id)
                    if self._init_camera(cam_id):
                        logger.debug("Reiinitialization of camera `%s` done.", cam_id)
                    else:
                        logger.warning("Reiinitialization of camera `%s` failed.", cam_id)
                        continue

                def on_snapshot_get(image_bin, position):
                    timestamp = get_iso_timestamp(datetime.datetime.now())
                    self._send_data((cam_id, timestamp, image_bin, position))

                t = threading.Thread(target=cam.loop, kwargs={'callback': on_snapshot_get})
                t.start()
                threads.append(t)
        
            # wait for all cameras to finish their tours
            for t in threads:
                t.join()

    @on("update")
    def config_update(self):
        """ Reinitialize cameras with new configuration. """
        
        # prevent waiting in queue and then updating multiple times
        # in case update triggers multiple times during a tour
        if self._update_lock.locked():
            return

        with self._update_lock:
            with self._tour_lock:
                # wait to finish all tours (do not decontruct object for active cameras)

                # reinitialize cameras with new config (no need to pass new config, pointer is passively updated)
                self._init_camera()
