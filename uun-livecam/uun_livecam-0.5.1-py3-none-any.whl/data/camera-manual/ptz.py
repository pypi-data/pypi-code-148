# ptz: absolute and relative movements + zoom
from onvif import ONVIFCamera


def absolute_move(cam, x, y, zoom):
    # create ptz (pan tilt zoom) service object
    ptz = cam.create_ptz_service()

    # get media service token
    media = cam.create_media_service()
    media_token = media.GetProfiles()[0].token
    ptz_token = media.GetProfiles()[0].PTZConfiguration.token

    # configuration request to get bounds on AbsoluteMove action space (range of movement)
    limits = get_ptz_configuration(ptz, ptz_token)

    # create request to AbsoluteMove
    # Arguments: ProfileToken [tt:ReferenceToken], Position [tt:PTZVector], Speed - optional [tt:PTZSpeed]
    absmove_request = ptz.create_type('AbsoluteMove')
    absmove_request.ProfileToken = media_token

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
    # http://www.onvif.org/ver10/tptz/PanTiltSpaces/SphericalPositionSpace Degrees

    # - set maximum speeds so that the action takes least amount of time
    absmove_request.Speed = {
        'PanTilt': {
            'x': limits["MAX_SPEED"],
            'y': limits["MAX_SPEED"],
            'space': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/GenericSpeedSpace'
        }
        # 'Zoom': {
        #     'x': 1,
        #     'space': 'http://www.onvif.org/ver10/tptz/ZoomSpaces/ZoomGenericSpeedSpace'
        # }
    }

    # send request
    ptz.AbsoluteMove(absmove_request)


def relative_move(cam, x, y, zoom):
    # create ptz (pan tilt zoom) service object
    ptz = cam.create_ptz_service()

    # get media service token
    media = cam.create_media_service()
    media_token = media.GetProfiles()[0].token
    ptz_token = media.GetProfiles()[0].PTZConfiguration.token

    # configuration request to get bounds on AbsoluteMove action space (range of movement)
    limits = get_ptz_configuration(ptz, ptz_token)

    # create request to RelativeMove
    # Arguments: ProfileToken [ReferenceToken], Translation [PTZVector], Speed - optional [PTZSpeed]
    relmove_request = ptz.create_type('RelativeMove')
    relmove_request.ProfileToken = media_token

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
            'x': limits["MAX_SPEED"],
            'y': limits["MAX_SPEED"],
            'space': 'http://www.onvif.org/ver10/tptz/PanTiltSpaces/GenericSpeedSpace'
        }
        # 'Zoom': {
        #     'x': 1,
        #     'space': 'http://www.onvif.org/ver10/tptz/ZoomSpaces/ZoomGenericSpeedSpace'
        # }
    }

    # send request
    ptz.RelativeMove(relmove_request)


def get_ptz_configuration(ptz, ptz_token):
    aux = {}

    # configuration request to get bounds on AbsoluteMove action space (range of movement)
    request = ptz.create_type('GetConfigurationOptions')
    request.ConfigurationToken = ptz_token
    ptz_configuration_options = ptz.GetConfigurationOptions(request)

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

    # bounds
    aux["X_MIN"] = ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].XRange.Min
    aux["X_MAX"] = ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].XRange.Max
    aux["Y_MIN"] = ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].YRange.Min
    aux["Y_MAX"] = ptz_configuration_options.Spaces.AbsolutePanTiltPositionSpace[0].YRange.Max
    aux["MAX_SPEED"] = ptz_configuration_options.Spaces.PanTiltSpeedSpace[0].XRange.Max
    aux["MIN_SPEED"] = ptz_configuration_options.Spaces.PanTiltSpeedSpace[0].XRange.Min
    return aux


def get_status(ptz, media_token):
    return ptz.GetStatus({'ProfileToken': media_token})
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


def get_move_status(ptz, media_token):
    return get_status(ptz, media_token).MoveStatus


if __name__ == '__main__':
    cam = ONVIFCamera('10.42.0.250', 80, 'onvif', 'javova123456789', '/home/hello/git/unicorn_ipcamseq/wsdl')
    print("started")
    absolute_move(cam, 0, 1, 0)
    # relative_move(cam, 0.25, 0, 0)
    print("stopped")
