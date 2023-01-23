from runfalconpipelineintegration.uc_scenario_runner import ScenarioRunner
from runfalconpipelineintegration.uc_authenticator import Authenticator
from runfalconpipelineintegration.model_credentials import Credentials

def test_run_scenario_async():
    credentials:Credentials = Credentials('al@runfalcon.com', 'andres123')
    authenticator:Authenticator = Authenticator()
    token:str = authenticator.authenticate(credentials)
    scenario_runner:ScenarioRunner = ScenarioRunner( \
                                        client_name = 'RunFalcon', \
                                        application_name = 'App', \
                                        scenario_code = 'Prueba google', \
                                        token = token)
    result:any = scenario_runner.run_sync()
    print(' >>>> result: {}'.format(result))