from wsntk.network import SensorNetwork

def SimuNet(*args, **kwargs):
    return iter(SensorNetwork(*args, **kwargs))
