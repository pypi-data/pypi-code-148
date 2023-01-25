from simunetcore.model import Model
from simunetcore import exception
import botocore
import boto3
import json

def createLambdaClient(aws_endpoint):
    """
    Creates an AWS lambda client.

    Returns
    -------
    lambda_client :boto3.Session.client
        The lambda client.

    Parameters
    ----------
    aws_endpoint : dict{str: Any}
        The endpoint dictionary containing the aws parameters.
        {
            "aws_id": "aws_id",
            "aws_key": "aws_key",
            "region": "eu-central-1",
            "max_attempts": 0,
            "read_timeout": 900,
            "connect_timeout": 60 
        }

    See Also
    --------
    boto3 library : simunet uses boto3 for aws communication.

    """
    
    # Create boto Session
    session = boto3.Session(
        aws_access_key_id=aws_endpoint["aws_id"],
        aws_secret_access_key=aws_endpoint["aws_key"],
        region_name=aws_endpoint["region"])

    # Create boto config
    cfg = botocore.config.Config(
        retries={"max_attempts": aws_endpoint["max_attempts"]}, 
        read_timeout=aws_endpoint["read_timeout"], 
        connect_timeout=aws_endpoint["connect_timeout"])
    
    # Create client
    lambda_client = session.client("lambda", config=cfg)
    
    # Return the lambda client
    return lambda_client

class AWSModel(Model):
    """AWS model class."""  
    
    def __init__(self, name=""):
        """
        Creates a new Model object.

        Parameters
        ----------
        name : str
            The name of the model.
 
        """
        
        Model.__init__(self, name)
        
        # Remote compute endpoint of the model
        self.endpoint = {
            "compress": True,
            "function": ""
        }

    def compute(
            self, client=None, invocation_type="compute", **kwargs):
        """
        Computes the state variables.

        Paramters
        ---------
        simulation_id : str, optional
            The id of simulation the model is used in.
            Default = "".
        model_id : str, optional
            The id of the model wihtin the simulation.
            Default = "".
        client : boto3.Session.client, optional
            The aws client to use for the communication.
            Default = None.
        invocation_type : str, optional
            The type of function invocation. Must be on of "warmup" 
            or "compute".
            Default = "compute".
        **kwargs : dict {str : Any}
            A dictionary of keyword : argument pairs used by derived classes.
    
        Raises
        ------
        `RemoteFunctionError` if soemthing went wrong on the remote site.
        `ParameterError` if parameters are not correct.

        """
           
        # Get function
        function = self.endpoint["function"]
        
        # Skip computation if function is None
        if function is None:
            return

        # Sanity Check 
        if client is None:
            raise exception.RemoteFunctionError(
                function=function, 
                invocation_type=invocation_type, 
                result="Client is 'None'")
            
        # Get compression settings
        use_compression = self.endpoint["compress"]
                   
        # Create payload
        if invocation_type == "warmup":
            payload = {}
            
        elif invocation_type == "compute":
            payload = { 
                "body" : self.dumps(compress=use_compression),
                "headers" : {
                    "sn-use-compression" : str(use_compression)
                }
            }
            
        else:
            raise exception.ParameterError(
                "Parameter 'invocation_type' must be 'compute' or 'warmup'")

        # Call Lambda function
        response = client.invoke(
            FunctionName=function, 
            InvocationType="RequestResponse",
            Payload=json.dumps(payload))
        
        # Get the result
        result = json.loads(response["Payload"].read())
 
        if invocation_type == "compute" and result["statusCode"] == 200:
            # Get the result and deserialize the model
            self.loads(result["body"], decompress=use_compression)
            
        elif invocation_type == "warmup" and result["statusCode"] == 204:
            pass
            
        else:
            # Raise error if something went wrong
            raise exception.RemoteFunctionError(
                function=function, 
                invocation_type=invocation_type, 
                result="statusCode {}, {}".format(
                    result["statusCode"],
                    result["body"]))
    