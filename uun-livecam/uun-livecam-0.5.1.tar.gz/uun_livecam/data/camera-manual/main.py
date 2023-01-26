#!/usr/bin/python3

# usage: 
#   ./main.py 
#       - without arguments: make a full 360° loop and take equally angled snapshots
#   ./main.py positions.json
#       - read positions from JSON file in format '[{"x": 0, "y": 0.5, "zoom": 0.2}, ...]'
#   ./main.py x y [z]
#       - x: rotation along the main circle (-1 ... 1]
#       - y: rotation (up/down) [0 ... 1]
#       - z: zoom [0 ... 1]

from onvif import ONVIFCamera
from ptz import absolute_move, relative_move, get_move_status
from snapshot import get_snapshot_uri, save_snapshot_digest
import json
import time
import sys

USER = "xxx"
PASSWORD = "xxx"
IP = "192.168.1.10"

def wait_for_move(ptz, media_token):
    """
    Block until move is finished.
    """
    time.sleep(0.1)  # update move status
    while get_move_status(ptz, media_token).PanTilt == 'MOVING' or get_move_status(ptz, media_token).Zoom == 'MOVING':
        time.sleep(0.2)
    return True

# create camera object
cam = ONVIFCamera(IP, 80, USER, PASSWORD, './wsdl')

# create ptz move object
ptz = cam.create_ptz_service()

# get first media service token
media_token = cam.create_media_service().GetProfiles()[0].token

print("[+] Getting snapshot uri...")
snapshot_uri = get_snapshot_uri(cam)
print(f"[+] Retrieved snapshot URI: {snapshot_uri}")

if len(sys.argv) == 1:
    # spin in a circle

    stepx = 0.25
    print(f"[+] Setting step size as {stepx}, `x` interval is [0+, 1=-1, 0-).")

    print("[+] Moving camera to initial position (0,0,0)...")
    absolute_move(cam, 0, 0, 0)
    wait_for_move(ptz, media_token)
    print("=== Camera initialized for sequencing. ===\n")

    print("[+] Starting loop...")
    no_steps = int(2.0/stepx)
    for i in range(no_steps):
        print("[+] Taking snapshot...")
        save_snapshot_digest(snapshot_uri, f"./snapshots/{i}.jpg", USER, PASSWORD)
        print(f"[+] Snapshot {i} taken. Moving camera to next position...")
        relative_move(cam, stepx, 0, 0)
elif len(sys.argv) == 2:
    # read from file
    positions = json.load(open(sys.argv[1]))
    for p in positions:
        x = p['x']
        y = p['ÿ́']
        z = p['zoom']
        print(f"[+] Moving camera to ({x}, {y}, {z})...")
        absolute_move(cam, x, y, z)
        wait_for_move(ptz, media_token)

        print("[+] Taking snapshot...")
        timestamp = int(time.time())
        save_snapshot_digest(snapshot_uri, f"./snapshots/{x}_{y}_{z}.jpg", USER, PASSWORD)
        print(f"[+] Snapshot taken and saved.")
    print("[+] Loop finished.")

elif len(sys.argv) == 4 or len(sys.argv) == 3:
    x = sys.argv[1]
    y = sys.argv[2]
    if len(sys.argv) > 3:
        z = sys.argv[3]
    else: 
        z = 1
    
    print(f"[+] Moving camera to ({x}, {y}, {z})...")
    absolute_move(cam, x, y, z)
    print("[+] Taking snapshot...")
    timestamp = int(time.time())
    save_snapshot_digest(snapshot_uri, f"./snapshots/{timestamp}.jpg", USER, PASSWORD)
    print(f"[+] Snapshot taken, saved to ./snapshots/{timestamp}.jpg")

# absolute_move(cam, 0, 0, 0)  # to be sure
