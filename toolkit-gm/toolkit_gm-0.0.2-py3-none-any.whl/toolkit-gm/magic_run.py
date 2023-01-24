###
# This is a magic command for Jupyter Notebook cells.
# 
# It controls if specified cells have to be executed or not.
# When called, if the variable behind the command is True, then the cell will run, else it will be skipped.
# This is particularly usefull with large notebook when some part of the code does not require to be exectuted every time.
#
# How to do so? Set at the begining of the notebook "control variables" like `run_part_2_of_notebook = True`
# And then, at the top of cells you want to control execution, simply add: `%run $run_part_2_of_notebook`
#
###


def run(line, cell=None):
    '''Run execution of the current line/cell if line evaluates to True.'''
    if eval(line): get_ipython().ex(cell)
    else: 
        print('Cell execution skipped by magic "run"')
        return

def load_ipython_extension(shell):
    '''Registers the run magic when the extension loads.'''
    shell.register_magic_function(run, 'line_cell')

def unload_ipython_extension(shell):
    '''Unregisters the run magic when the extension unloads.'''
    del shell.magics_manager.magics['cell']['run']
# 
