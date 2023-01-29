from dataclasses import dataclass
import os
import traceback
import urllib.parse
import builtins
import jsons
import requests
from requests.exceptions import HTTPError
import logging
from . import utils
logger:logging.Logger = utils.get_logger(__name__)

@dataclass
class GetVersionResponse:
    """
    See member variables for doc
    """
    isConcurrent:bool = False
    """ are we running in a concurrent environment? """
    isInfinMlflowServer:bool = False
    """ are we running in an infinstor Mlflow environment? """
    cognitoCliClientId:str = ""
    """ Applies to both: concurrent environment and infin mlflow environment """
    cognitoAppClientId:str = ""
    """ Available only in infin mlflow environment """
    mlflowDnsName: str = ""
    """ Available only in infin mlflow environment.  Used to contruct rest api URLs of infinstor mlflow server """
    mlflowuiDnsName: str = ""
    """ Available only in infin mlflow environment """
    mlflowstaticDnsName: str = ""
    """ Available only in infin mlflow environment """
    apiDnsName: str = ""
    """ Available only in infin mlflow environment """
    serviceDnsName: str = ""
    """ Available only in infin mlflow environment """
    region:str = ""
    """ Applies to both: concurrent environment and infin mlflow environment """
    service:str = None
    """this is similar to 'infinstor.com'.  Note that 'service' is not part of the response from https://mlflow.infinstor.com/api/2.0/mlflow/infinstor/get_version.  It is populated by the method below.  Applies to both: concurrent environment and infin mlflow environment """
    mlflowParallelsDnsName:str = ""
    """the concurrent API endpoint dns name, similar to 'concurrent'.  Available only in concurrent environment  """
    mlflowParallelsUiDnsName:str = ""
    """ the concurrent UI dns name, similar to 'mlflowui'.  Available only in concurrent environment """
    cognitoMlflowuiClientId = ""
    """ the cognito client ID for mlflow UI.  Applies to both: concurrent environment and infin mlflow environment  """
    
    
def bootstrap_config_values_from_mlflow_rest_if_needed() -> GetVersionResponse:
    """
    invokes /api/2.0/mlflow/infinstor/get_version or /api/2.0/mlflow/parallels/getversion to get configuration details of infinstor service or concurrent service

    [extended_summary]

    Raises:
        Exception: no exceptions raised

    Returns:
        GetVersionResponse: server response or None (on failure)
    """
    ##########
    #  TODO: a copy exists in 
    #  infinstor-mlflow/plugin/infinstor_mlflow_plugin/login.py 
    #  infinstor-mlflow/processors/singlevm/scripts/rclocal.py
    #  infinstor-jupyterlab/server-extension/jupyterlab_infinstor/__init__.py
    #  infinstor-jupyterlab/server-extension/jupyterlab_infinstor/cognito_utils.py
    #  infinstor-jupyterlab/clientlib/infinstor/bootstrap.py
    #  infinstor-jupyterlab/infinstor_py_bootstrap_project/infinstor_py_bootstrap/infinstor_py_bootstrap.py
    #  Need to see how to share code between two pypi packages to eliminate this duplication
    #  when refactoring this code, also refactor the copies
    ############
    
    # if the configuration values have already been bootstrapped, return
    if getattr(builtins, 'region', None): return
    
    # note that this code (server-extension code) runs in the jupyterlab server, where MLFLOW_TRACKING_URI was not set earlier.  Now it needs to be set correctly to the mlflow api hostname: mlflow.infinstor.com.  Note that 'mlflow' in the hostname is not hardcoded.. it can be a different subdomain name
    #
    # is_concurrent: are we running in a concurrent environment?
    is_concurrent:bool = True if os.getenv('MLFLOW_CONCURRENT_URI') else False
    
    # if running in concurrent's environment, ensure that mlflow_concurrent_uri is set correctly
    concurrent_purl:urllib.parse.ParseResult = None
    if is_concurrent:
        concurrent_purl = urllib.parse.urlparse(os.getenv('MLFLOW_CONCURRENT_URI'))
        if concurrent_purl.scheme.lower() != 'https':
            raise Exception(f"environment variable MLFLOW_CONCURRENT_URI={os.getenv('MLFLOW_CONCURRENT_URI')} has an invalid value or the url scheme != https.  Set the environment variable correctly and restart the process")
    
    mlflow_purl:urllib.parse.ParseResult = None
    mlflow_purl = urllib.parse.urlparse(os.getenv('MLFLOW_TRACKING_URI'))
    # if not running in concurrent's environment, then mlflow_tracking_uri has to be infinstor.. if running in concurrent's environment, can also have non infinstor mlflow server
    if not is_concurrent:
        if mlflow_purl.scheme.lower() != 'infinstor':
            raise Exception(f"environment variable MLFLOW_TRACKING_URI={os.getenv('MLFLOW_TRACKING_URI')} has an invalid value or the url scheme != infinstor.  Set the environment variable correctly and restart the process")
    
    # detect if the mlflow server is an infinstor mlflow server.  For 'R' MlProjects, the tracking URI for infinstor mlflow is set to https and not 'infinstor', but this is ok since 'R' will not use this python package
    is_infinMlflowServer:bool =  mlflow_purl.scheme.lower() == 'infinstor'
    
    try:
        headers = { 'Authorization': 'None' }
        resp:dict = {};  service_name_from_infin_mlflow = ''
        # if we have an infinstor mlflow server, use its get_version
        if is_infinMlflowServer:
            url =  'https://' + mlflow_purl.hostname + '/api/2.0/mlflow/infinstor/get_version' 
            service_name_from_infin_mlflow = mlflow_purl.hostname[mlflow_purl.hostname.find('.')+1:]
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            resp.update(response.json())
        
        # also get the concurrent's getversion, if available
        concurrent_dns_name = ''; service_name_from_concurrent = ''
        if is_concurrent:
            url = 'https://' + concurrent_purl.hostname + '/api/2.0/mlflow/parallels/getversion'
            concurrent_dns_name:str = concurrent_purl.hostname[:concurrent_purl.hostname.find('.')]
            service_name_from_concurrent = concurrent_purl.hostname[concurrent_purl.hostname.find('.')+1:]
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            # add 'concurrent' /getversion response to 'infinstor' /get_version response dict
            resp.update(response.json())
        
        # at this point, 'resp' may have the get_version response from 'infinstor' and 'concurrent'        
        logger.debug(f'bootstrap_config_values_from_mlflow_rest_if_needed: /getversion={resp}')
        
        builtins.clientid = resp['cognitoCliClientId'] if resp.get('cognitoCliClientId') else ''
        builtins.appclientid = resp['cognitoAppClientId'] if is_infinMlflowServer else ''
        # string slicing below: to extract 'infinstor.com' from 'mlflow.infinstor.com'
        # handle scenario where older server versions do not send resp['cookieHost']
        service_domain = resp.get('cookieHost') if resp.get('cookieHost') else service_name_from_infin_mlflow if is_infinMlflowServer else service_name_from_concurrent
        builtins.mlflowserver = resp['mlflowDnsName'] + '.' + service_domain if resp.get('mlflowDnsName') else '' # if is_infinMlflowServer else ''
        builtins.mlflowuiserver = resp['mlflowuiDnsName'] + '.' + service_domain if resp.get('mlflowuiDnsName') else '' # if is_infinMlflowServer else ''
        builtins.mlflowstaticserver = resp['mlflowstaticDnsName'] + '.' + service_domain if resp.get('mlflowstaticDnsName') else '' # if is_infinMlflowServer else ''
        builtins.apiserver = resp['apiDnsName'] + '.' + service_domain if resp.get('apiDnsName') else '' # if is_infinMlflowServer else ''
        builtins.serviceserver = resp['serviceDnsName'] + '.' + service_domain if resp.get('serviceDnsName') else '' # if is_infinMlflowServer else ''
        builtins.service = service_domain
        builtins.region = resp['region']
        mlflowParallelsDnsName = ''
        if is_concurrent:
            # handle scenario where older server versions do not send resp['mlflowParallelsDnsName']
            mlflowParallelsDnsName:str = resp['mlflowParallelsDnsName'] if resp.get('mlflowParallelsDnsName') else concurrent_dns_name if concurrent_dns_name else '' # if is_concurrent else ''
            builtins.concurrent_server = mlflowParallelsDnsName + '.' + service_domain # if is_concurrent else ''
            
            # older server versions do not send resp['mlflowParallelsUiDnsName']
            builtins.concurrent_ui_server = resp['mlflowParallelsUiDnsName'] + '.' + service_domain if resp.get('mlflowParallelsUiDnsName') else '' # if is_concurrent else ''

        # older server versions do not send resp['cognitoMlflowuiClientId']
        builtins.mlflowuiClientId = resp['cognitoMlflowuiClientId']  if resp.get('cognitoMlflowuiClientId') else ''
        builtins.isConcurrent = is_concurrent; 
        builtins.isInfinMlflowServer:bool = is_infinMlflowServer
        
        get_version_resp:GetVersionResponse = jsons.load(resp, GetVersionResponse)
        get_version_resp.service = service_domain
        get_version_resp.isConcurrent = is_concurrent
        get_version_resp.isInfinMlflowServer = is_infinMlflowServer
        # handle scenario where older server versions do not send resp['mlflowParallelsDnsName']
        get_version_resp.mlflowParallelsDnsName = mlflowParallelsDnsName
        
        logger.debug(f'bootstrap_config_values_from_mlflow_rest_if_needed: get_version_resp={get_version_resp}')
        builtins_dict:dict = {  'builtins.' + builtin_name:getattr(builtins, builtin_name, None)  for builtin_name in ['clientid', 'appclientid', 'mlflowserver', 'mlflowuiserver', 'mlflowstaticserver', 'apiserver', 'serviceserver', 'service', 'region', 'concurrent_server', 'concurrent_ui_server', 'mlflowuiClientId', 'isConcurrent', 'isInfinMlflowServer']   }
        logger.debug(f'bootstrap_config_values_from_mlflow_rest_if_needed: builtins_dict={builtins_dict}')
        
        return get_version_resp
    except HTTPError as http_err:
        logger.error(f"Caught Exception: {http_err}: {traceback.format_exc()}" )
        return None
    except Exception as err:
        logger.error(f"Caught Exception: {err}: {traceback.format_exc()}" )
        return None


