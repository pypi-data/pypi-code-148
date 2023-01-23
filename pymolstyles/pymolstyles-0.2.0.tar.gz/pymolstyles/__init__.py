# Configure the default workspace
from pymolstyles.workspace import *

# Load styles
from pymolstyles.styles import *

# Load default atoms settings
from pymolstyles.environment import standardize_vdw_radius
standardize_vdw_radius()

# Load plotting tools
from pymolstyles.plots import *

# Load utilities functions
from pymolstyles.tools import *