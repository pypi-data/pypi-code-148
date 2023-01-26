#!/usr/bin/python3

from onvif import ONVIFCamera


def get_info(cam):
    resp = {}
    resp['hostname'] = cam.devicemgmt.GetHostname().Name
    resp['datetime'] = cam.devicemgmt.GetSystemDateAndTime()

    params = {'IncludeCapability': True}
    # same as before:
    # params = self.cam.devicemgmt.create_type('GetServices')
    # params.IncludeCapability = False
    resp['services'] = cam.devicemgmt.GetServices(params)
    resp['service-capabilities'] = cam.devicemgmt.GetServiceCapabilities()

    categories = ['PTZ', 'Media', 'Imaging', 'Device', 'Analytics', 'Events']
    resp['capabilities'] = cam.devicemgmt.GetCapabilities()

    resp['category-capabilities'] = {}
    for category in categories:
        resp['category-capabilities'][category] = cam.devicemgmt.GetCapabilities({'Category': category})

    return resp


if __name__ == '__main__':
    cam = ONVIFCamera('10.42.0.250', 80, 'onvif', 'javova123456789', '/home/hello/git/unicorn_ipcam-img/wsdl')

    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    resp = get_info(cam)
    pp.pprint(resp)
