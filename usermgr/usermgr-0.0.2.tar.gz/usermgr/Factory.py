import importlib

AWS_COGNITO = 'cognito'

singleton = None


def get_instance(provider, **kwargs):
    global singleton
    if singleton != None:
        return singleton
    module = importlib.import_module(f'.{provider}', 'usermgr.providers')
    singleton = module.new_instance(**kwargs)
    return singleton
