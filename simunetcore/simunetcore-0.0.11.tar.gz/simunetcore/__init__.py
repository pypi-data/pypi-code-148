"""
Simulation Network simunet
"""

import datetime
from simunetcore.serializer import Serializer
from simunetcore.model import Model
from simunetcore.rest import RESTModel
from simunetcore.mqtt import MQTTModel
from simunetcore.aws import AWSModel
from simunetcore.waveform import Waveform
from simunetcore.factory import Factory

__all__ = ["Serializer", "Model", "RESTModel", "MQTTModel", "AWSModel", "Waveform", "Factory"]
__title__ = "simunetcore"
__version__ = "0.0.11"
__license__ = "MIT License"
__copyright__ = "core simunet team and contributors".format(datetime.date.today().year)

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
