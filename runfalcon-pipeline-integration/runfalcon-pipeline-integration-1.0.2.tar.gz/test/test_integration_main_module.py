import array
from runfalconpipelineintegration.int_main_module import ModuleMain
from runfalconpipelineintegration.uc_authenticator import Authenticator
from runfalconpipelineintegration.model_credentials import Credentials

def get_token() -> str:
    credentials:Credentials = Credentials('r@runfalcon.com', 'rdevilla123')
    authenticator:Authenticator = Authenticator()
    return authenticator.authenticate(credentials)


# def test_main_authenticate():
#     args:array = ['authenticate', 'login', 'r@runfalcon.com', 'password', 'rdevilla123']
#     main_module:ModuleMain = ModuleMain()
#     main_module.run(args)

def test_main_run_scenario():
    token:str = get_token()
    args:array = ['run', 'token', token, 'client', 'RunFalcon', 'application', 'App', 'scenario', 'Prueba google', '-q']
    main_module:ModuleMain = ModuleMain()
    main_module.run(args)
    