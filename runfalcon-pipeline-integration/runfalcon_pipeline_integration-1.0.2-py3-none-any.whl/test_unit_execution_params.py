import array
from runfalconpipelineintegration.util_configuration import Configuration
from runfalconpipelineintegration.model_execution_params import ExecutionParams, parse_from_args

def test_parse_args():
    Configuration.instance().set_config_value('LOGGER', 'level', 'DEBUG')

    args:array = ['operation1', 'param1', 'value1', '--switch1', '-switch2']
    execution_params:ExecutionParams = parse_from_args(args)
    assert execution_params.operation == 'operation1'
    assert execution_params.get_arg('param1') == 'value1'
    assert execution_params.exists_swtich('--switch1')
    assert execution_params.exists_swtich('-switch2')
    assert not execution_params.exists_swtich('--switch3')
    assert not execution_params.exists_swtich('-switch4')
