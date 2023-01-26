from onvif import ONVIFCamera
import requests
import shutil


def get_snapshot_uri(cam):
    # Create ptz service object
    # ptz = cam.create_ptz_service()

    # Create media service object
    media = cam.create_media_service()
    # >>> dir(media)
    # [__...__, 'clone', 'create_type', 'daemon', 'dt_diff', 'encrypt', 'passwd', 'service_wrapper', 'to_dict', 'url',
    #  'user', 'ws_client', 'xaddr', 'zeep_client']

    # Get target profile
    # print(media.GetProfiles())
    media_profile = media.GetProfiles()[0]
    # print(media_profile)

    snapshot_uri_resp = media.GetSnapshotUri({'ProfileToken': media_profile.token})
    return snapshot_uri_resp.Uri


def save_snapshot_digest(uri, path, username, password):

    resp = requests.get(uri, auth=requests.auth.HTTPDigestAuth(username, password), stream=True)
    if 200 <= resp.status_code < 300:
        with open(path, 'wb') as f:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, f)
        return True

    return False


if __name__ == '__main__':
    cam = ONVIFCamera('10.42.0.250', 80, 'onvif', 'javova123456789', '/home/hello/git/unicorn_ipcam-img/wsdl')

    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # resp = get_info(cam)
    # pp.pprint(resp)

    uri = get_snapshot_uri(cam)
    status = save_snapshot_digest(uri, './snapshot.jpg', 'onvif', 'javova123456789')
    print(status)
