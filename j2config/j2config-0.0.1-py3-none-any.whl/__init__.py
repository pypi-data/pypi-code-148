"""Package which helps simplifying text output generation from template. 
"""

__doc__ = '''Package which helps simplifying text output generation from template.'''


from .j2 import PrepareConfig
from .read_conditions import get_variables, get_conditions


__all__ = [
	'PrepareConfig',
	'get_conditions', 'get_variables'
	
]

__version__ = '0.0.1'