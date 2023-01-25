from simunetcore.serializer import Serializer
import numpy as np
    
class Model(Serializer):
    """Model base class."""  

    def __init__(self, name=""):
        """
        Creates a new Model object.

        Parameters
        ----------
        name : str
            The name of the model.
 
        """
       
        Serializer.__init__(self)
        
        # Meta Data
        self.name = name        # Name of the model
        self.description = ""   # Description of the model
        self.dim = "unknown"    # Dimension of the model ["unknown", "0D", "1D", "2D", "3D"]
        self.domain = "unknown" # Domain of the model [e.g. "unknown", "VT", "PLM", "LCA"]
        
        # Enpoint of the the model
        self.site = "local"     # Computation site ["local", "remote"]       
        self.threadsafe = False # Supports threading [True, False]

        # Model specific members
        self.params = {}        # Parameters of the model
        self.vars = {}          # State variables of the model (dependent in time and space)
        self.u = {}             # Input vectors of the model
        self.y = {}             # Output vectors of  the model
        self.t = [0]            # Time base of the values (dim(t) = dim(var))
        self.adj = []           # Internal adjacencies of the model
  
    def __get_value(self, port, port_id, t):
        
        result = []
        for var_id in port[port_id]["vars"]:
            result.append(self.get_var(var_id, t))
        return result
        
    def __set_value(self, port, port_id, value):
        
        if len(value) != len(port[port_id]["vars"]):
            raise ValueError("Shape mismatch")
        for var_id in port[port_id]["vars"]:
            index = port[port_id]["vars"].index(var_id)
            if isinstance(value[index], np.ndarray):
                self.vars[var_id]["value"] = value[index].tolist() 
            else:
                self.vars[var_id]["value"] = value[index]
            
    def __get_port_vars(self, port):
        
        var_set = set()
        for port_id in port:
            var_set = var_set.union(port[port_id]["vars"])
        return var_set
    
    def get_params(self):
        """
        Returns the parameters of the model.

        Returns
        -------
        value : set of str
            A set of ids of the parameters of the model.
    
        """
        return set(self.vars.keys())

    def get_param(self, param_id):
        """
        Returns the value of the parameter with id `param_id`.

        Returns
        -------
        value : Any
            The value of the parameter with id `param_id`.

        Parameters
        ----------
        param_id : str
            The id of the parameter to retrieve.
    
        """
       
        return self.params[param_id]["value"]

    def set_param(self, param_id, value):
        """
        Sets the value of the parameter with id `param_id`.

        Parameters
        ----------
        param_id : str
            The id of the parameter to set.
        value : Any
            The value to be stored under the id `param_id`.
    
        """
       
        if isinstance(value, np.ndarray):
            self.params[param_id]["value"] = value.tolist() 
        else: 
            self.params[param_id]["value"] = value

    def get_vars(self):
        """
        Returns the variables of the model.

        Returns
        -------
        value : set of str
            A set of ids of the variables of the model.
    
        """
        
        return set(self.vars.keys())

    def get_var(self, var_id, t=None):
        """
        Returns the value of the variable with id `var_id`.
        If `t` is given the value is interpolated for the given time steps.

        Returns
        -------
        value : Any
            The value of the variable with id `var_id`.

        Parameters
        ----------
        var_id : str
            The id of the variable to retrieve.
        t : float or list of float, optional
            The time steps for which the result is to be interpolated. 
            Deafult = None.
    
        """
        
        if t is None:
            return self.vars[var_id]["value"]  
        else:
            return np.interp(t, self.get_t(), self.vars[var_id]["value"]).tolist()

    def set_var(self, var_id, value):
        """
        Sets the value of the variable with id `var_id`.

        Parameters
        ----------
        var_id : str
            The id of the variable to set.
        value : Any
            The value to be stored under the id `var_id`.
    
        """
       
        if isinstance(value, np.ndarray):
            self.vars[var_id]["value"] = value.tolist()  
        else:
            self.vars[var_id]["value"] = value

    def get_t(self):
        """
        Returns the current time frame of the state variables of the model.

        Returns
        -------
        value : float or list of float
            The time frame of the state variables of the model.
        """       
        return self.t
    
    def set_t(self, value):
        """
        Sets the time frame for the state variables of the model.

        Parameters
        ----------
        value : float, list of float or np.ndarray
            The time frame to be stored.
    
        """
        
        if isinstance(value, np.ndarray):
            self.t = value.tolist()  
        else:
            self.t = value
        
    def get_u(self, u_id, t=None):
        """
        Returns the values of the variables of the input port with id `u_id`.
        If `t` is given the values are interpolated for the given time steps.

        Returns
        -------
        value : list
            The values of the variables of the port with id `u_id`.

        Parameters
        ----------
        u_id : str
            The id of the input port.
        t : float or list of float, optional
            The time steps for which the result is to be interpolated.  
            Deafult = None.
    
        """
        
        return self.__get_value(self.u, u_id, t)
    
    def set_u(self, u_id, value):
        """
        Sets the values of the variables of the input port with id `u_id`.

        Parameters
        ----------
        u_id : str
            The id of the input port.
        value : list
            The value to be stored for the variables of the port 
            with the id `port_id`.
    
        """
       
        if isinstance(value, np.ndarray):
            self.__set_value(self.u, u_id, value.tolist())
        else:
            self.__set_value(self.u, u_id, value)
        
    def get_u_vars(self):
        """
        Returns the input variables of the model.

        Returns
        -------
        value : set of str
            A list of ids of the the input variables of the model.
    
        """
       
        return self.__get_port_vars(self.u)

    def get_y(self, y_id, t=None):
        """
        Returns the values of the variables of the output port with id `y_id`.
        If `t` is given the values are interpolated for the given time steps.

        Returns
        -------
        value : list
            The values of the variables of the port with id `y_id`.

        Parameters
        ----------
        y_id : str
            The id of the output port.
        t : float or list of float, optional
            The time steps for which the result is to be interpolated.  
            Deafult = None.
    
        """
        
        return self.__get_value(self.y, y_id, t)
    
    def set_y(self, y_id, value):
        """
        Sets the values of the variables of the output port with id `y_id`.

        Parameters
        ----------
        y_id : str
            The id of the output port.
        value : list
            The value to be stored for the variables of the port 
            with the id `port_id`.
    
        """
        
        if isinstance(value, np.ndarray):
            self.__set_value(self.y, y_id, value.tolist())
        else:
            self.__set_value(self.y, y_id, value)
    
    def get_y_vars(self):
        """
        Returns the output variables of the model.

        Returns
        -------
        value : set of str
            A list of ids of the the output variables of the model.
    
        """
        
        return self.__get_port_vars(self.y)
    
    def compute(self, *args, **kwargs):
        """
        Computes the state variables.

        Paramters
        ---------
        *args : Any
            A list of arguments used by derived classes.
        **kwargs : dict {str : Any}
            A dictionary of keyword : argument pairs used by derived classes.
    
        """
        if self.get_vars() == self.get_u_vars():
            return

        raise NotImplementedError("Method 'compute' is not implemented in 'Model'")
