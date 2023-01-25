import asyncio
import logging
import uuid
import json
import uvloop

from quantnet_controller.mq.gmqtt.mqttclient import MQTTClient

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def on_connect(client, flags, rc, properties):
    print('Connected')

def on_message(client, topic, payload, qos, properties):
    print('RECV MSG:', payload)
    
    # find the corr
    corrid = payload['corr_id']
    
    # set value of body
    body = payload['body']
    client.handler(corrid, body)
    

def on_disconnect(client, packet, exc=None):
    print('Disconnected')

def on_subscribe(client, mid, qos, properties):
    print('Subscribed')

class RPCClient:
    def __init__(self, cid, **kwargs):
        self._cid = cid or uuid.uuid4().hex
        self._queue = 'rpc-res/' + self._cid
        
        self._mqtt_client_username = None
        self._mqtt_client_password = None
        self._mqtt_broker_host = None
        self._mqtt_broker_port = None
        self._mqttclient = None
        
        self._sent_requests = {}
        
    async def start_mqttclient(self, host, port=1883, username="", password=None):
        """
        start the mqtt client
        """
        self._mqttclient = MQTTClient('rpc-client-' + self._cid)
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
    
    def __call__(self, corrid, body):
        fut = _sent_requests.pop(corrid)
        if fut != None:
            fut.set_result(body)
    
    def call(self, target, params, timeout=1.0, verbose=None):
        corrid = uuid.uuid4().hex
        
        msg = {"corr_id": corrid,
               "reply_to": self._queue,
               'body': params}
        
        topic = 'rpc/' + target
        self._mqttclient.publish(topic, msg, qos=1, retain=False)
        
        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        _sent_requests[corrid] = fut
        
        # TODO: wait for reply
        try:
            asyncio.wait_for(fut, timeout=5.0)
        except TimeoutError:
            print('timeout')
        
        # TODO: return reply
        body = fut.get_result()
        return body