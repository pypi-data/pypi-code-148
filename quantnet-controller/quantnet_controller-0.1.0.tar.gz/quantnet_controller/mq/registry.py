import asyncio
import logging
import uuid
import json
import uvloop

from quantnet_controller.mq.gmqtt.mqttclient import MQTTClient

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def on_connect(client, flags, rc, properties):
    print('Registry: Connected')

def on_message(client, topic, payload, qos, properties):
    print('Registry: RECV MSG:')
    print(json.dumps(json.loads(payload), indent=4, sort_keys=False))
    
    if client.topic_match('reg/', topic):
        # tokens = client.topic_tokenise(topic)
        # online = payload['online']
        # queue = payload['queue']
        # client._handler('on_message', online, tokens, queue, payload['modules'])
        client._handler('on_message', (topic, payload, qos, properties))
    else:
        print('Registry: unknown message')

def on_disconnect(client, packet, exc=None):
    print('Registry Disconnected')

def on_subscribe(client, mid, qos, properties):
    print('Registry: Subscribed')

class Registry:
    def __init__(self, cid, **kwargs):
        self._cid = cid or uuid.uuid4().hex
        self._queue = 'reg/+'
        
        self._mqtt_client_username = None
        self._mqtt_client_password = None
        self._mqtt_broker_host = None
        self._mqtt_broker_port = None
        self._mqttclient = None
        
        self._subscriptions = {}
        self._on_register_callback = None
        
    async def start_mqttclient(self, host, port=1883, username="", password=None):
        """
        start the mqtt client
        """
        self._mqttclient = MQTTClient('quantnet-server-' + self._queue)
        self._mqttclient.set_handler(self)
        
        self._mqttclient.on_connect = on_connect
        self._mqttclient.on_message = on_message
        self._mqttclient.on_disconnect = on_disconnect
        self._mqttclient.on_subscribe = on_subscribe
        
        self._mqtt_client_username = username
        self._mqtt_client_password = password
        self._mqttclient.set_auth_credentials(username, password)
        
        self._mqtt_broker_host = host
        self._mqtt_broker_port = port
        await self._mqttclient.connect(host=host, port=port)
        
        self._mqttclient.subscribe(self._queue, 2)
        self._add_subscription(self._queue, 2)
        
    def _add_subscription(self, queue, qos):
        self._subscriptions[queue] = qos
        
    def stop_mqttclient(self):
        pass
    
    async def start(self):
        await self.start_mqttclient('localhost')
        
    async def stop(self):
        self.stop_mqttclient()
        
    async def register(self, config, host, port=1883, username="", password=None):
        """
        start the mqtt client
        """
        self._mqttclient = MQTTClient('quantnet-client')
        self._mqttclient.set_handler(self)
        
        # self._mqttclient.on_connect = on_connect
        # self._mqttclient.on_message = on_message
        # self._mqttclient.on_disconnect = on_disconnect
        # self._mqttclient.on_subscribe = on_subscribe
        
        self._mqtt_client_username = username
        self._mqtt_client_password = password
        self._mqttclient.set_auth_credentials(username, password)
        
        self._mqtt_broker_host = host
        self._mqtt_broker_port = port
        await self._mqttclient.connect(host=host, port=port)
        
        with open(config.path) as file:
            msg = json.load(file)
            print('register=')
            print(json.dumps(msg, indent=4))
        file.close()
        
        self._mqttclient.subscribe('client', 2)
        self._mqttclient.publish('reg/server', json.dumps(msg), 1, False)
        
    
    def __call__(self, source, args):
        if source == 'on_message':
            topic, payload, qos, properties = args
            
            """ debug: dump the registration message """
            print("Register")
            
            """TODO: update db record """
        
        """ callback to user """    
        if (self._on_register_callback != None):
            """ parse and callback """
            online = "TODO"
            tokens = "TODO"
            queue = "TODO"
            modules = "TODO"
            self._on_register_callback(online, tokens, queue, modules)
        
    @property
    def on_register(self):
        return self._on_register_callback
    
    @on_register.setter
    def on_register(self, cb):
        if not callable(cb):
            raise ValueError
        self._on_register_callback = cb
    
    # def send_response(self, reply, props):
    #     msg = {"corr_id": props.correlateion_id,
    #            'body': reply}
    #     self._mqttclient.publish(props.reply_to, msg, 1, false)