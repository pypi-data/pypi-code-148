from simunetcore.model import Model
from simunetcore import exception
import requests

class RESTModel(Model):
    """REST model class."""  
    
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
            "url": "", 
            "timeout": 300,
            "compress": False,
            "header": {}
        } 
    
    def compute(self, invocation_type="compute", **kwargs):
        """
        Computes the state variables.

        Paramters
        ---------
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
        function = self.endpoint["url"]
        
        # Get compression settings
        use_compression = self.endpoint["compress"]

        # Create payload
        if invocation_type == "warmup":
            body = {}
            
        elif invocation_type == "compute":
            # Create and compress body
            body = self.dumps(compress=use_compression)
            
        else:
            raise exception.ParameterError(
                "Parameter 'invocation_type' must be 'compute' or 'warmup'")

        # Create headers dict and request
        headers_dict = self.endpoint["header"]
        headers_dict["sn-use-compression"] = str(use_compression)

        # Post the request
        response = requests.post(
            function, 
            data=body, 
            timeout=self.endpoint["timeout"], 
            headers = headers_dict)

        # Check the result
        if invocation_type == "compute" and response.status_code == 200:                  
            # load the data from the result
            self.loads(response.text, decompress=use_compression)
            
        elif invocation_type == "warmup" and response.status_code == 204:
            pass
        
        else:
            # Raise error if something went wrong
            raise exception.RemoteFunctionError(
                function=function, 
                invocation_type=invocation_type, 
                result="statusCode {}, {}".format(
                    response.status_code,
                    response.text))
