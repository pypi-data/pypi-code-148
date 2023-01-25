"""
Get the confiugration file from /opt/quantnet/etc/quantnet.cfg
"""

import os
import json
import sys

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

from quantnet_controller.common import exception


def config_get(section, option, raise_exception=True, default=None):
    """
    Return the string value for a given option in a section

    :param section: the named section.
    :param option: the named option.
    :param raise_exception: Boolean to raise or not NoOptionError or NoSectionError.
    :param default: the default value if not found.
.
    :returns: the configuration value.
    """
    try:
        return __CONFIG.get(section, option)
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError) as err:
        if raise_exception and default is None:
            raise err
        return default


__CONFIG = ConfigParser.SafeConfigParser(os.environ)

__CONFIGFILES = list()
if 'QUANTNET_HOME' in os.environ:
    __CONFIGFILES.append('%s/etc/quantnet.cfg' % os.environ['QUANTNET_HOME'])
__CONFIGFILES.append('/opt/quantnet/etc/quantnet.cfg')

__HAS_CONFIG = False
for configfile in __CONFIGFILES:
    __HAS_CONFIG = __CONFIG.read(configfile) == [configfile]
    if __HAS_CONFIG:
        break

if not __HAS_CONFIG:

    if 'sphinx' not in sys.modules:
        # test to not fail when build the API doc
        raise Exception('Could not load quantnet configuration file quantnet.cfg.'
                        'Quantnet looks in the following directories for a configuration file, in order:'
                        '\n\t${QUANTNET_HOME}/etc/quantnet.cfg'
                        '\n\t/opt/quantnet/etc/quantnet.cfg'
                        '\n\t${VIRTUAL_ENV}/etc/quantnet.cfg')
        
class Config:
    def __init__(
            self,
            mq_broker_host: str = "127.0.0.1",
            mq_broker_port: int = 1883,
        ):
            self.mq_broker_host = mq_broker_host
            self.mq_broker_port = mq_broker_port
            
            self.path = config_get('mq', 'path')
            
            