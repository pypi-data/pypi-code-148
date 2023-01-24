"""
This module encapsulates the different sources which might be used by the calibration.
"""
import logging
import struct
import numpy as np
import h5py
from o3r_algo_utilities import o3r_uncompress_di
import ifm3dpy

try:
    from ifm_imeas.imeas_tools import unpack_imeas
except ImportError:
    # Optional algo debug h5 files / algo debug live input are not supported.
    unpack_imeas = None

try:
    from ifm_o3r_algodebug.Receiver import ADReceiver
except ImportError:
    # Optional algo debug live input is not supported.
    ADReceiver = None

logger = logging.getLogger(__name__)
    
def getFrame(source):
    """
    :param source: Specifies the source the following formats are supported:
        'adrec://<pathToFile>' use an algo debug hdf5 recording stored in <pathToFile> 
            (requires the ifm proprietary library imeas)
        'adlive://<ip>/port<camPort>' use a live connection to the camera specified 
            by <ip> and <camPort> (0..5)
        'ifm3dpy://<ip>/port<camPort>' use a live connection to the camera specified 
            by <ip> and <camPort> (0..5)    """
    if source.startswith("adrec://"):
        if unpack_imeas is None:
            raise RuntimeError("The ifm-internal tool imeas is required for reading algo debug recordings.")
        h5_algo_debug = source[len("adrec://"):]
        frame = load_algo_debug_recording(h5_algo_debug)
    elif source.startswith("adlive://"):
        if unpack_imeas is None:
            raise RuntimeError("The ifm-internal tool imeas is required for algo debug input.")
        if ADReceiver is None:
            raise RuntimeError("The tool ifm_o3r_algodebug is required for algo debug live input.")
        ip_port = source[len("adlive://"):]
        ip, port = ip_port.split("/")
        if port.startswith("port"):
            port = port[len("port"):]
        port = int(port)
        frame = grab_algo_debug(ip, port)
    elif source.startswith("ifm3dpy://"):
        ip_port = source[len("ifm3dpy://"):]
        ip, port = ip_port.split("/")
        if port.startswith("port"):
            port = port[len("port"):]
        port = int(port)

        frame = grab_ifm3d_frame(ip,port)
        
    else:
        raise RuntimeError("cannot interpret source.")    
    return frame
    
def load_algo_debug_recording(h5file):
    """
    Parses the last frame of an algo debug measurement while ignoring the referenced calibration.
    
    :param h5file: The path of the h5 file to be read.
    :return: a dictionary with Cartesian coordinates, distance and amplitude matrix and calibration information.
    """
    f = h5py.File(h5file, "r")
    calib = None
    for i in range(len(f["streams"]["o3r_di_0"])):
        d, _ = unpack_imeas(f["streams"]["o3r_di_0"][i][0].tobytes(), add_toplevel_wrapper=False)
        if "irs2381/calib" in d:
            calib = d["irs2381/calib"]
            break

    d,_ = unpack_imeas(f["streams"]["o3r_di_0"][-1][0].tobytes(), add_toplevel_wrapper=False)
    f.close()
    
    ifout_compr = d["irs2381/ifout_compr"]

    return proc_algo_debug(calib, ifout_compr)

def grab_algo_debug(ip, port):
    calib = None
    ifout_compr = None
    with ADReceiver(ip, "port%d"%port, autoInterpret=True, xmlrpcTimeout=3, autostart=True) as rcv:
        logger.debug("receiving frame ...")
        cnt = 0
        ifout_compr = None
        while cnt < 10:
            data = rcv.get(timeout=3)
            cnt += 1
            if "irs2381/calib" in data:
                calib = data["irs2381/calib"]
            if "irs2381/ifout_compr" in data:
                # use 2m mode if available
                if ifout_compr is None or data["irs2381/ifout_compr"].measurementRangeMax < ifout_compr.measurementRangeMax:
                    ifout_compr = data["irs2381/ifout_compr"]
        if calib is None or ifout_compr is None:
            raise RuntimeError("Could not grab algo debug frame from specified address.")

    return proc_algo_debug(calib, ifout_compr)

def proc_algo_debug(calib, ifout_compr):
    # ignore the currently parametrized calibration
    opticToUserTrans = np.array([getattr(calib.intrinsicCalibration.camRefToOpticalSystem, "trans"+a) for a in "XYZ"])
    opticToUserRot = np.array([getattr(calib.intrinsicCalibration.camRefToOpticalSystem, "rot"+a) for a in "XYZ"])
    X,Y,Z,D = o3r_uncompress_di.xyzdFromDistance(np.array(ifout_compr.distance), ifout_compr.distanceResolution, 
                                                 opticToUserTrans, opticToUserRot,
                                                 ifout_compr.intrinsicCalib.modelID,
                                                 ifout_compr.intrinsicCalib.modelParameters,
                                                 ifout_compr.width, ifout_compr.height)
    A = o3r_uncompress_di.convertAmplitude(np.array(ifout_compr.amplitude), ifout_compr.amplitudeResolution, ifout_compr.width, ifout_compr.height)
    R = np.reshape(ifout_compr.reflectivity, (ifout_compr.height, ifout_compr.width))
    res = dict(X=X,Y=Y,Z=Z,D=D,A=A,R=R,
               camRefToOpticalSystem=dict(trans=opticToUserTrans,rot=opticToUserRot),
               intrinsic=dict(modelID=ifout_compr.intrinsicCalib.modelID,modelParameters=np.array(ifout_compr.intrinsicCalib.modelParameters)),
               inverseIntrinsic=dict(modelID=ifout_compr.inverseIntrinsicCalib.modelID,modelParameters=np.array(ifout_compr.inverseIntrinsicCalib.modelParameters)),
               )
    return res

def set_extrinsic_zero(o3r_object,port):
    port=f"port{port}"
    o3r_object.set({'ports':{port:{'state':'CONF'}}})
    o3r_object.set({'ports':{port:{'processing':{'extrinsicHeadToUser': {'rotX': 0.0,'rotY': 0.0, 'rotZ': 0.0, 'transX': 0.0, 'transY': 0.0, 'transZ': 0.0}}}}})
    o3r_object.set({'ports':{port:{'state':'RUN'}}})

    return o3r_object

def grab_ifm3d_frame(ip,port):
    ifm3dpy_version = tuple(int(x) for x in ifm3dpy.__version__.split("."))
    if ifm3dpy_version < (1,0,0):
        logger.warning("Using ifm3dpy legacy version. Consider updating to a version >= 1.0.1")
        # legacy API
        o3r=ifm3dpy.O3RCamera(ip)
        final_port=o3r.port("port%d" %port).pcic_port

        oldCalib=o3r.get([f"/ports/port{port}/processing/extrinsicHeadToUser"])
        try:  
            o3r=set_extrinsic_zero(o3r,port)
            frame_grabber=ifm3dpy.FrameGrabber(o3r,pcic_port=final_port)
            im = ifm3dpy.ImageBuffer()
            if frame_grabber.wait_for_frame(im, 500)==False:
                raise ValueError #Exception('fg-timeout on ' + port + ' reached')
            xyz=im.xyz_image()
            invIntrinsic=im.inverse_intrinsics()
            invIntrinsic=np.array(invIntrinsic,dtype=np.float)
            frame = {'A': im.amplitude_image(),'D': im.distance_image(),'X':xyz[:,:,0],'Y':xyz[:,:,1],'Z':xyz[:,:,2],'R': np.zeros((172, 224)),'inverseIntrinsic': dict(modelID=1,modelParameters=invIntrinsic),
                    'camRefToOpticalSystem': dict(trans=np.array(im.extrinsics()[0:3]), rot=np.array(im.extrinsics()[3:6]) )}
        finally:
            o3r.set(oldCalib)
    else:
        if ifm3dpy_version == (1,0,0):
            raise RuntimeError("Need a later version due to issues in ifm3dpy 1.0.0")
        # updated API
        o3r = ifm3dpy.O3R(ip=ip)
        final_port = o3r.get([f"/ports/port{port}/data/pcicTCPPort"])["ports"][f"port{port}"]["data"]["pcicTCPPort"]
        oldCalib=o3r.get([f"/ports/port{port}/processing/extrinsicHeadToUser"])
        try:  
            o3r=set_extrinsic_zero(o3r,port)
            frame_grabber=ifm3dpy.FrameGrabber(o3r,pcic_port=final_port)
            frame_grabber.start()
            ok, frame = frame_grabber.wait_for_frame().wait_for(timeout_ms=500)
            if not ok:
                raise ValueError #Exception('fg-timeout on ' + port + ' reached')
            xyz=frame.get_buffer(ifm3dpy.buffer_id.XYZ)
            ampl=frame.get_buffer(ifm3dpy.buffer_id.NORM_AMPLITUDE_IMAGE)
            dist=frame.get_buffer(ifm3dpy.buffer_id.RADIAL_DISTANCE_IMAGE)
            refl=frame.get_buffer(ifm3dpy.buffer_id.REFLECTIVITY)
            invIntrinsic = frame.get_buffer(ifm3dpy.buffer_id.INVERSE_INTRINSIC_CALIBRATION).tobytes()
            invIntrinsicModelID, *invIntrinsicModelParams = struct.unpack("<I32f", invIntrinsic)
            extrinsics = frame.get_buffer(ifm3dpy.buffer_id.EXTRINSIC_CALIB).flatten()
            frame = {
                'A': ampl,
                'D': dist,
                'X': xyz[:,:,0],
                'Y': xyz[:,:,1],
                'Z': xyz[:,:,2],
                'R': refl,
                'inverseIntrinsic': dict(modelID=invIntrinsicModelID,modelParameters=invIntrinsicModelParams),
                'camRefToOpticalSystem': dict(trans=extrinsics[0:3], rot=extrinsics[3:6])
            }
        finally:
            o3r.set(oldCalib)
    return frame
