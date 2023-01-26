from onvif import ONVIFCamera
import requests
import shutil
from io import BytesIO
import time

import logging
logger = logging.getLogger(__name__)

class SnapSequence:
    """
    A class for managing ONVIF camera to take snapshot-like panorama. Moves camera along a given path of coordinates and takes pictures.
    """

    def __init__(self, ip, port, user, password, wsdl, positions):
        """
        ip:         ONVIFCamera IP address
        user:       ONVIF user with sufficient permissions
        password:   ONVIF user's password
        wsdl:       location to wsdl files (protocol)
        positions:  list of locations to visit [{'x': ..., 'y': ..., 'zoom': ...}, ...]
        """
        self._cam = ONVIFCamera(ip, port, user, password, wsdl)
        self._user = user
        self._password = password
        self._ptz = PTZ(self._cam)

        # get snapshot URI for downloading snapshots
        media = self._cam.create_media_service()
        media_profile = media.GetProfiles()[0]
        snapshot_uri_resp = media.GetSnapshotUri({'ProfileToken': media_profile.token})

        self._snapshot_uri = snapshot_uri_resp.Uri
        self._positions = positions

    def _download_snapshot(self):
        resp = requests.get(self._snapshot_uri, auth=requests.auth.HTTPDigestAuth(self._user, self._password))

        if 200 <= resp.status_code < 300:
            return BytesIO(resp.content)
        else:
            raise DownloadException("Cannot download image from camera.")

    def loop(self, callback):
        """
        Visit every location provided in self.positions.
        callback: a void function (image_binary, position) -> None to be called after taking a single snapshot
        """
        i = 0
        logger.debug("Starting snapshot loop.")

        for position in self._positions:
            x = position['x']
            y = position['y']
            zoom = position['zoom']
            name = position['name'] if 'name' in position else 'unnamed'

            logger.info(f"Moving camera to position \"{name}\" @ (x={x}, y={y}, zoom={zoom})...")
            self._ptz.absolute_move(x, y, zoom)
            self._ptz.wait_for_move()

            # output single snapshot
            snapshot_bin = self._download_snapshot()
            callback(snapshot_bin, position)
            
            logger.debug("Snapshot %i taken.", i)
            i += 1

        # reset to initial position
        # self.ptz.absolute_move(0, 0, 0)

        logger.debug("Loop finished.")

class DownloadException(Exception):
    pass

class PTZ:
    """ A wrapper for useful PTZ (Pan&Tilt&Zoom) actions. """
    def __init__(self, cam):
        """
        cam: ONVIFCamera object
        """
        # create ptz (pan tilt zoom) service object
        self._ptz_service = cam.create_ptz_service()

        # get media service token
        media = cam.create_media_service()
        self._media_token = media.GetProfiles()[0].token
        self._ptz_token = media.GetProfiles()[0].PTZConfiguration.token

        # configuration request to get bounds on AbsoluteMove and RelativeMove action space (range of movement) + speeds
        self.conf = self.get_ptz_configuration()

    def absolute_move(self, x, y, zoom):
        """
        Moves camera to absolute position specified by x, y coordinates and zooms.
        x: rotation with respect to axis going perpendicularly through ceiling
        y: up/down rotation, rotation with respect to axis going parallel with ceiling
        Common ranges for x, y and zoom are [-1,1], [-1,1] and [0,1] respectively but it depends on particular camera.
        """
        # check x coordinate
        assert self.conf.Spaces.AbsolutePanTiltPositionSpace[0].XRange.Min <= x <= self.conf.Spaces.AbsolutePanTiltPositionSpace[0].XRange.Max, \
            "x coordinate is not in bounds specified by camera"

        # check y coordinate
        assert self.conf.Spaces.AbsolutePanTiltPositionSpace[0].YRange.Min <= y <= self.conf.Spaces.AbsolutePanTiltPositionSpace[0].YRange.Max, \
            "y coordinate is not in bounds specified by camera"

        # check zoom coordinate
        assert self.conf.Spaces.AbsoluteZoomPositionSpace[0].XRange.Min <= zoom <= self.conf.Spaces.AbsoluteZoomPositionSpace[0].XRange.Max, \
            "zoom is not in bounds specified by camera"

        # create request to AbsoluteMove
        # Arguments: ProfileToken [ReferenceToken], Position [PTZVector], Speed - optional [PTZSpeed]
        absmove_request = self._ptz_service.create_type('AbsoluteMove')
        absmove_request.ProfileToken = self._media_token

        # == set actual move instructions ==
        absmove_request.Position = {
            'PanTilt': {
                'x': x,
                'y': y,
                'space': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/PositionGenericSpace'
            },
            'Zoom': {
                'x': zoom,
                'space': 'http://www.onvif.org/ver10/tptz/ZoomSpaces/PositionGenericSpace'
            }
        }

        # - set maximum speeds so that the action takes least amount of time
        # there is no PanTiltSpeedSpace[0].YRange, x and y share XRange speed space
        absmove_request.Speed = {
            'PanTilt': {
                'x': self.conf.Spaces.PanTiltSpeedSpace[0].XRange.Max,
                'y': self.conf.Spaces.PanTiltSpeedSpace[0].XRange.Max,
                'space': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/GenericSpeedSpace'
            },
            'Zoom': {
                'x': self.conf.Spaces.ZoomSpeedSpace[0].XRange.Max,
                'space': 'http://www.onvif.org/ver10/tptz/ZoomSpaces/ZoomGenericSpeedSpace'
            }
        }

        # send request
        self._ptz_service.AbsoluteMove(absmove_request)

    def relative_move(self, x, y, zoom):
        """
        Moves camera along vector specified by x, y coordinates and zooms. This is a RELATIVE translation as opposed to
            setting ABSOLUTE coordinates of self.absolute_move.
        The camera stops when it can continue no further.
        x: rotation with respect to axis going perpendicularly through ceiling
        y: up/down rotation, rotation with respect to axis going parallel with ceiling
        Common ranges for x, y and zoom are [-1,1], [-1,1] and [0,1] respectively but it depends on particular camera.
        """
        # check x coordinate
        assert self.conf.Spaces.RelativePanTiltTranslationSpace[0].XRange.Min <= x <= self.conf.Spaces.RelativePanTiltTranslationSpace[0].XRange.Max, \
            "x coordinate is not in bounds specified by camera"

        # check y coordinate
        assert self.conf.Spaces.RelativePanTiltTranslationSpace[0].YRange.Min <= y <= self.conf.Spaces.RelativePanTiltTranslationSpace[0].YRange.Max, \
            "y coordinate is not in bounds specified by camera"

        # check zoom coordinate
        assert self.conf.Spaces.RelativeZoomTranslationSpace[0].XRange.Min <= zoom <= self.conf.Spaces.RelativeZoomTranslationSpace[0].XRange.Max, \
            "zoom is not in bounds specified by camera"

        # create request to RelativeMove
        # Arguments: ProfileToken [ReferenceToken], Translation [PTZVector], Speed - optional [PTZSpeed]
        relmove_request = self._ptz_service.create_type('RelativeMove')
        relmove_request.ProfileToken = self._media_token

        # == set actual move instructions ==
        # - copy structure of correct response from current position
        relmove_request.Translation = {
            'PanTilt': {
                'x': x,
                'y': y,
                'space': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/TranslationGenericSpace'
            },
            'Zoom': {
                'x': zoom,
                'space': 'http://www.onvif.org/ver10/tptz/ZoomSpaces/TranslationGenericSpace'
            }
        }

        # - set maximum speeds so that the action takes least amount of time
        relmove_request.Speed = {
            'PanTilt': {
                'x': self.conf.Spaces.PanTiltSpeedSpace[0].XRange.Max,
                'y': self.conf.Spaces.PanTiltSpeedSpace[0].XRange.Max,
                'space': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/GenericSpeedSpace'
            },
            'Zoom': {
                'x': self.conf.Spaces.ZoomSpeedSpace[0].XRange.Max,
                'space': 'http://www.onvif.org/ver10/tptz/ZoomSpaces/ZoomGenericSpeedSpace'
            }
        }

        # send request
        self._ptz_service.RelativeMove(relmove_request)

    def wait_for_move(self):
        """
        Block until movement of the camera is finished.
        """
        time.sleep(0.1)  # update move status
        status = self.get_move_status()
        while status.PanTilt == 'MOVING' or status.Zoom == 'MOVING':
            status = self.get_move_status()
            time.sleep(0.2)
        return True

    def get_status(self):
        return self._ptz_service.GetStatus({'ProfileToken': self._media_token})
        # >>> ptz.GetStatus({'ProfileToken': media_profile.token}).Position
        # {
        #     'PanTilt': {
        #         'x': -0.027778,
        #         'y': -1.0,
        #         'space': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/PositionGenericSpace'
        #     },
        #     'Zoom': {
        #         'x': 0.0,
        #         'space': 'http://www.onvif.org/ver10/tptz/ZoomSpaces/PositionGenericSpace'
        #     }
        # }

    def get_move_status(self):
        return self.get_status().MoveStatus

    def get_ptz_configuration(self):
        """
        Get PTZ configuration (to set movement bounds).
        """
        # configuration request to get bounds on action space (range of movement)
        request = self._ptz_service.create_type('GetConfigurationOptions')
        request.ConfigurationToken = self._ptz_token
        ptz_configuration_options = self._ptz_service.GetConfigurationOptions(request)
        return ptz_configuration_options

        # >>> ptz_configuration_options.Spaces
        # {
        #     'AbsolutePanTiltPositionSpace': [
        #         {
        #             'URI': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/PositionGenericSpace',
        #             'XRange': {
        #                 'Min': -1.0,
        #                 'Max': 1.0
        #             },
        #             'YRange': {
        #                 'Min': -1.0,
        #                 'Max': 1.0
        #             }
        #         }
        #     ],
        #     'AbsoluteZoomPositionSpace': [
        #         {
        #             'URI': 'http://www.onvif.org/ver10/tptz/ZoomSpaces/PositionGenericSpace',
        #             'XRange': {
        #                 'Min': 0.0,
        #                 'Max': 1.0
        #             }
        #         }
        #     ],
        #     'PanTiltSpeedSpace': [
        #         {
        #             'URI': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/GenericSpeedSpace',
        #             'XRange': {
        #                 'Min': 0.0,
        #                 'Max': 1.0
        #             }
        #         }
        #     ], ... }
