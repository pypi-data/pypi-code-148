class ParameterError(Exception):
    """Parameter mismatch exception"""
    
    def __init__(self, msg):      
        """
        Creates a new ParameterError object.

        Parameters
        ----------
        msg : str
            The msg of the exception.
 
        """

        self.msg = msg
 
    def __str__(self):       
        return self.msg
    
    
class ComputeError(Exception):
    """Computation error"""
    
    def __init__(self, model_name, model_id):       
        """
        Creates a new ComputeError object.

        Parameters
        ----------
        model_name : str
            The name of the model that caused the error.
        model_id : str
            The id of the model that caused the error.
 
        """

        self.model_name = model_name
        self.model_id = model_id
 
    def __str__(self):
        return "Computation of model '{}' with id '{}' failed".format(
            self.model_name, self.model_id)

    
class CouplingError(Exception):
    """Coupling error"""
    
    def __init__(self, model_name, model_id, u_id):   
        """
        Creates a new InvokerError object.

        Parameters
        ----------
        model_name : str
            The name of the model that caused the error.
        model_id : str
            The id of the model that caused the error.
        u_id : str
            The id of the model input that caused the error.
 
        """

        self.model_name = model_name
        self.model_id = model_id
        self.u_id = u_id
 
    def __str__(self):     
        return "Coupling of model '{}' with id '{}' on port '{}' failed".format(
            self.model_name, self.model_id, self.u_id)


class InvokerError(Exception):
    """Invoker command error"""
    
    def __init__(self, command, result):
        """
        Creates a new InvokerError object.

        Parameters
        ----------
        command : str
            The remote command that caused the error.
        result : str
            The result that was returned from the remote host.
 
        """

        self.command = command
        self.result = result
 
    def __str__(self):       
        return "Invoker command '{}' failed: {}".format(self.command, self.result)

    
class RemoteFunctionError(Exception):
    """Remote function error"""
    
    def __init__(self, function, invocation_type, result):
        """
        Creates a new RemoteFunctionError object.

        Parameters
        ----------
        function : str
            The remote function that caused the error.
        invocation_type : str
            The invocation_type that was used.
        result : str
            The result that was returned from the remote host.
 
        """
        
        self.function = function
        self.invocation_type = invocation_type
        self.result = result
 
    def __str__(self):       
        return "Remote invocation '{}' of function '{}' failed: {}".format(
            self.invocation_type, self.function, self.result)
    