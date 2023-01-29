#!python

from pynscq.paths import nscq_nvswitch_device_uuid_path
from pynscq import *

devices = []

@nscqCallback(p_nscq_uuid_t, nscq_rc_t, p_nscq_uuid_t, user_data_type)
def device_uuid_callback(device, rc, uuid, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    devices.append(label.data.decode("UTF-8"))


with NSCQSession() as session:
    session.path_observe(nscq_nvswitch_device_uuid_path, device_uuid_callback)

for label in devices:
    print(label)
