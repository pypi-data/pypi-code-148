from simunetcore.model import Model
from simunetcore import exception
from simunetcore import logger
from paho.mqtt import client as mqtt
import uuid
import json
import time

   
def createMQTTClient(mqtt_endpoint, client_id=uuid.uuid4()):
    """
    Creates an mqtt client.

    Returns
    -------
    mqtt_client : paho.mqtt.Client
        The mqtt client.

    Parameters
    ----------
    mqtt_endpoint : dict{str: Any}
        The endpoint dictionary containing the mqqt parameters.
        {
            "broker"   : "mqtt.broker.url",
            "port"     : 1883,
            "transport": "tcp",
            "tls"      : False,
            "username" : "username",
            "password" : "password"
        }
    client_id: str, optional
        Sets client id of this client (used by the broker). 
        Default = uuid4.uuid().

    See Also
    --------
    paho.mqtt library : simunet uses paho for mqtt communication.

    """
    
    # Create mqtt client
    mqtt_client = mqtt.Client("{}".format(client_id))
    mqtt_client.username_pw_set(
        mqtt_endpoint["username"], 
        mqtt_endpoint["password"])
    
    # Enable tls
    if mqtt_endpoint["tls"]:
        mqtt_client.tls_set()
    
    # Attach logger
    mqtt_client.on_log = lambda client, userdata, level, msg : logger.debug(msg)
 
    # Connect to the broker
    mqtt_client.connect(mqtt_endpoint["broker"], mqtt_endpoint["port"])
    
    # Return the mqtt client
    return mqtt_client

class MQTTCommand(object):
    """MQTT command class."""
    
    def __init__(self):
        """
        Creates a new MQTTCommand object.
 
        """

        # MQTT response and command result
        self.response = None
        self.result = None
        
    def __on_message(self, client, userdata, msg):
        
        # Decode msg payload
        self.response = msg.payload.decode()
        
    def run(
            self, mqtt_client, topic_request, payload, 
            topic_response, timeout=900):
        """
        Runs the blocking MQTT command.

        Parameters
        ----------
        mqtt_client : paho.mqtt.client
            The mqqtt client to use for the communication. 
        topic_request : str
            The request topic to publish to.
        payload : object
            The payload object (It will be serialized to json). 
        topic_response : str
            The response topic to subscribe to.
        timeout : int, optional
            The timeout for the command in seconds.
            Default = 900.

        Raises
        ------
        `TimeoutError` if `timeout` is reached.

        """

        # Add callbacks
        prev_on_message = mqtt_client.on_message
        mqtt_client.on_message = self.__on_message
                        
        try:
            # Subscribe
            mqtt_client.subscribe(topic_response)

            # Publish payload to topic request
            mqtt_client.publish(topic_request, json.dumps(payload))

            # Wait for results
            self.response = None                                                    
            t_start = time.time()
            while self.response == None and time.time() - t_start < timeout:
                mqtt_client.loop(0.001)

            # Check the result
            if self.response:
                self.result = json.loads(self.response)
            else:
                raise TimeoutError("Function timeout {}s reached".format(timeout))
                
        finally:
            # Unsubscribe from the topic
            mqtt_client.unsubscribe(topic_response)
            mqtt_client.on_message = prev_on_message

        
class MQTTModel(Model):
    """MQTT command class."""
    
    def __init__(self, name=""):
        """
        Creates a new MQTTModel object.

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
            self, simulation_id="", model_id="", client=None, 
            invocation_type="compute", **kwargs):
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
        client : paho.mqtt.client, optional
            The mqtt client to use for the communication.
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
        
        # Command properties
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
        use_compression = self.endpoint['compress']
            
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

        # Set provider id
        provider = "invoker"

        # Overwrite provider id if necessary
        if "provider" in self.endpoint:
            provider = self.endpoint["provider"]
            
        # Create topics
        topic_request  = "/simunet/{}/{}/{}/{}/task".format(
            provider, simulation_id, model_id, function)
        topic_response = "/simunet/{}/{}/{}/{}/result".format(
            provider, simulation_id, model_id, function)
            
        # Create MQTT command
        cmd = MQTTCommand()
        # Run the command
        cmd.run(client, topic_request, payload, topic_response)

        if invocation_type == "compute" and cmd.result["statusCode"] == 200:
            # Get the result and deserialize the model
            self.loads(cmd.result["body"], decompress=use_compression)
            
        elif invocation_type == "warmup" and cmd.result["statusCode"] == 204:
            pass
        
        else:
            # Raise error if something went wrong
            raise exception.RemoteFunctionError(
                function=function, 
                invocation_type=invocation_type, 
                result="statusCode {} {}".format(
                    cmd.result["statusCode"],
                    cmd.result["body"]))

