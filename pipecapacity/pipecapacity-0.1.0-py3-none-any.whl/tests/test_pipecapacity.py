import os
import sys

from pipecapacity.common.ymlInput import ymlInput
from pipecapacity.common.update_deep import AttributeDict
from pipecapacity.common.ApplicationManager import ConfigureApplicationInputs
from pipecapacity.pipe_capacity import pipe_capacity

ymlfile = 'src/pipecapacity/tests/test_data/pipecapacity.yml'
sys.argv.append(ymlfile)
print(os.path.isfile(ymlfile))
cfg = ymlInput(ymlfile, updateYml=None)
cfg = AttributeDict(cfg)

basename = 'pipecapacity'
application_manager = ConfigureApplicationInputs(basename)
application_manager.configure(run_dict=None)

cfg_base = pipe_capacity(application_manager.cfg)
