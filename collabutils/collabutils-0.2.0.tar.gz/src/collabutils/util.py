import warnings


def warn(name, extra, e):
    warnings.warn(
        '{0} is only available when collabutils is installed with {1} support\n'
        'pip install collabutils[{1}]'.format(name, extra))
    raise e
