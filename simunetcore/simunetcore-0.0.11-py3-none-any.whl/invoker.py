from simunetcore import mqtt
from simunetcore import aws
from threading import Thread
import json
import traceback

class Invoker(object):
    """MQTT Invoker base class."""  
    
    def __init__(self, provider, simulation_id, model_id, function):
        """
        Creates a new Invoker object.
        The parameters are used to subscribe to the mqtt broker on:
        `/simunet/{provider}/{simulation_id}/{model_id}/{function}/task`

        Parameters
        ----------
        provider : str
            The provider id within simunet.
        simulation_id : str
            The simulation id to serve.
        model_id : str
            The model id to serve.
        function : str
            The function name.
 
        """
        
        # Store properties
        self.provider = provider
        self.simulation_id = simulation_id
        self.model_id = model_id
        self.function = function
        
        # MQTT communication client
        self.mqtt_client = None
        
        # Request topic
        self.topic_request  = "/simunet/{}/{}/{}/{}/task".format(
            provider, simulation_id, model_id, function)     
    
    def __on_message(self, client, userdata, msg):
        
        # Create thread
        t = Thread(
            target=self.compute_model, 
            args=(msg.topic, msg.payload.decode()))
        
        # Fire & forget
        t.start()

    def compute_model(self, topic, payload):
        """
        Computes the associated model.

        Paramters
        ---------
        topic : str
            The subscripted mqtt topic.
        payload : str
            The payload of the mqtt message.
    
        """

        raise NotImplementedError(
            "Method 'compute_model' is not implemented in 'Invoker'")
         
    def connect_mqtt(self, mqtt_endpoint):
        """
        Connects to a mqtt broker and subscribes to:
        `/simunet/provider/simulation_id/model_id/function/task`

        Paramters
        ---------
        mqtt_endpoint : dict{str: Any}
            The endpoint dictionary containing the mqtt parameters.
            {
                "broker": "mqtt.broker.url",
                "port": 1883,
                "transport": "tcp",
                "tls": False,
                "username": "user",
                "password": "passwd"
            }

        See Also
        --------
        paho.mqtt library : simunet uses paho for mqtt communication.

        """        
        # Create mqtt client
        self.mqtt_client = mqtt.createMQTTClient(
            mqtt_endpoint, "{}[{}|{}|{}]".format(
                self.provider, self.simulation_id, self.model_id, self.function))
        
        # Attach callbacks
        self.mqtt_client.on_message = self.__on_message     
        # Subscribe to topic
        self.mqtt_client.subscribe(self.topic_request)        
        # Start listener loop
        self.mqtt_client.loop_start()

    def disconnect_mqtt(self):
        """
        Disconnects from the mqtt broker.

        """
        
        # Stop listener loop
        self.mqtt_client.loop_stop()
        # Unsubscribe
        self.mqtt_client.unsubscribe(self.topic_request)
        # Disconnect
        self.mqtt_client.disconnect()
                
class AWSInvoker(Invoker):
    """AWS Invoker class."""  
    
    def __init__(self, simulation_id):
        """
        Creates a new AWSInvoker object.
        The parameter is used to subscribe to the mqtt broker on
        `/simunet/invoker/{simulation_id}/+/+/task` so that requests 
        for all values for `model_id` and `function` are catched.

        Parameters
        ----------
        simulation_id : str
            The simulation id to serve.
 
        """
        
        Invoker.__init__(
            self, provider="invoker", simulation_id=simulation_id, 
            model_id="+", function="+")
            
        # AWS lambda client
        self.lambda_client = None
                         
    def compute_model(self, topic, payload):
        """
        Computes the associated model.

        Paramters
        ---------
        topic : str
            The subscripted mqtt topic.
        payload : str
            The payload of the mqtt message.
    
        """
        
        # Get function name from topic
        topic_list = topic.split("/")
        function = topic_list[-2]
        
        # Call Lambda function
        response = self.lambda_client.invoke(
            FunctionName=function, 
            InvocationType='RequestResponse',
            Payload=payload
        )

        # Get the result
        result = response["Payload"].read()
        
        # Publish the result
        topic_list[-1] = "result"
        topic_response = "/".join(topic_list)
        self.mqtt_client.publish(topic_response, result)   

    def connect_aws(self, aws_endpoint):
        """
        Connects to AWS lambda.

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
        
        # Create boto client
        self.lambda_client = aws.createLambdaClient(aws_endpoint)
        
class LocalInvoker(Invoker):
    """Local Invoker class."""  
    
    def __init__(self, model, provider, function):
        """
        Creates a new LocalInvoker object.
        The parameters 'provider' and 'function' are used to 
        subscribe to the mqtt broker on:
        `/simunet/{provider}/+/+/{function}/task` so that requests 
        for all values for `simulation_id` and `model_id` are catched.

        Parameters
        ----------
        model : simunet.Model
            The associated simunet model.
        provider : str
            The provider id within simunet.
        function : str
            The function name.

        """
        
        Invoker.__init__(
            self, provider=provider, simulation_id="+", 
            model_id="+", function=function)
        
        # Store the connected model
        self.model = model
        
    def compute_model(self, topic, payload):
        """
        Computes the associated model.

        Paramters
        ---------
        topic : str
            The subscripted mqtt topic.
        payload : str
            The payload of the mqtt message.
    
        """
        
        try:         
            # Get simulation id an model id name from topic
            topic_list = topic.split("/")
            simulation_id = topic_list[-4]
            model_id = topic_list[-3]

            # Task disctionary
            task = json.loads(payload)
            # Result dictionary
            result = {}

            # Call function
            if task:
                self.model.loads(task["body"])
                self.model.compute(
                    simulation_id = simulation_id,
                    model_id = model_id)
                result["statusCode"] = 200
                result["body"] = self.model.dumps(indent = True)
            else:
                result["statusCode"] = 204
                result["body"] = ""
                
        except:
            # Set error code and error messgae
            result["statusCode"] = 500
            result["body"] = traceback.format_exc()
            
        finally:
            # Publish the result
            topic_list[-1] = "result"
            topic_response = "/".join(topic_list)
            self.mqtt_client.publish(topic_response, json.dumps(result, indent=True))
        