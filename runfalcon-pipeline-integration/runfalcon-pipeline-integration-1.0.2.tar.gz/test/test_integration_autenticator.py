from runfalconpipelineintegration.uc_authenticator import Authenticator
from runfalconpipelineintegration.model_credentials import Credentials

def test_authenticate_success():
    credentials:Credentials = Credentials('r@runfalcon.com', 'rdevilla123')
    authenticator:Authenticator = Authenticator()
    exception:any = None
    try:
        token:str = authenticator.authenticate(credentials)
    except Exception as e:
        print(e)
        exception = e
    assert exception == None
    assert token != None

def test_authenticate_error():
    credentials:Credentials = Credentials('r@runfalcon.com', 'xxxx')
    authenticator:Authenticator = Authenticator()
    exception:any = None
    try:
        token:str = authenticator.authenticate(credentials)
    except Exception as e:
        print(e)
        exception = e
    assert exception != None