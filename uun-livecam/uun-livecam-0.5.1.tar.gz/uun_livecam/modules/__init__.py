"""Initialize additional modules."""
from uun_livecam.modules.SnapCam import SnapCam
import logging
logger_sc = logging.getLogger(__name__ + '.uuCmdSnapshotCreate')

# module list in format { module_id: [module_instance, None], ... }
def init(config, uuclient):

    def cmd_livecam_snapshot_create(snapshot):
        """
        snapshotCreateDtoIn = {
          cameraCode: "...", // camera code
          tourTs: "...", //tour timestamp
          image: "...", //
          x: 0,
          y: 0,
          zoom: 0
        }
        """
        cam_id = snapshot[0]
        timestamp = snapshot[1]
        image_bin = snapshot[2]
        positions = snapshot[3]
        x = positions["x"]
        y = positions["y"]
        zoom = positions["zoom"]
        
        uucmd = config['uuApp']['uuCmdList']['snapshotCreate']
        uuclient.multipart_request(uucmd, {
            'cameraCode': str(cam_id),
            'tourTs': str(timestamp),
            'x': str(x),
            'y': str(y),
            'zoom': str(zoom),
            'image': ('image.jpeg', image_bin, 'image/jpeg') 
        })

        return [] # do not care if failed or succeded, do not save anyway

    gconfig = config["gateway"]

    return [
            SnapCam(gconfig, cmd_livecam_snapshot_create)
            ]


