import asyncio
import logging
import uuid
import json
import uvloop

from quantnet_controller.mq.gmqtt.mqttclient import MQTTClient

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

def on_connect(client, flags, rc, properties):
    print('Connected')
    # client.subscribe('TEST/#', qos=0)
    # client.subscribe("$SYS/#")
    type = 0x01
    params = (flags, rc, properties)
    client._handler(type, params)

def on_message(client, topic, payload, qos, properties):
    print('RPCServer RECV MSG:', payload)
    rpcprops = {payload['corr_id'], payload['reply_to']}
    body = payload['body']
    type = 0x02
    params = (body, rpcpros)
    client._handler(type, params)

def on_disconnect(client, packet, exc=None):
    print('Disconnected')

def on_subscribe(client, mid, qos, properties):
    print('Subscribed')
    type = 0x04
    params = (mid, qos, properties)
    client._handler(type, params)

class RPCServer:
    def __init__(self, cid, **kwargs):
        self._cid = cid or uuid.uuid4().hex
        self._queue = 'rpc/' + self._cid
        
        self._mqtt_client_username = None
        self._mqtt_client_password = None
        self._mqtt_broker_host = None
        self._mqtt_broker_port = None
        self._mqttclient = None
        
        self._subscriptions = {}
        
    async def start_mqttclient(self, host, port=1883, username="", password=None):
        """
        start the mqtt client
        """
        self._mqttclient = MQTTClient('rpc-server-' + self._queue)
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
    
    def __call__(self, type, params):
        if type==0x1:
            flags, rc, properties = params
            self._handle_connect(flags, rc, properties)
        if type==0x02:
            body, rpcpros = params
            self._handle_message(body, rpcpros)
        if type==0x04:
            mid, qos, properties = params
            self._handle_subscribe(mid, qos, properties)
        
    def _handle_connect(self, flags, rc, properties):
        print(flags)
        
    def _handle_message(self, body, rpcpros):
        print(body)
        self.on_rpcmsg(body, rpcpros)
        
    def _handle_subscribe(self, mid, qos, properties):
        pass
    
    async def start(self):
        await self.start_mqttclient('localhost')
        
    async def stop(self):
        pass
        
    @property
    def on_rpcmsg(self):
        return self._on_rpcmsg_callback
    
    @on_rpcmsg.setter
    def on_rpcmsg(self, cb):
        if not callable(cb):
            raise ValueError
        self._on_rpcmsg_callback = cb
    
    def _on_msg(self, topic, msg):
        self._mqttclient.publish('rpc/' + repcprops.reply_to, reply, 1, False)
        
    def _on_conn(self, conn, id):
        pass
    
    def send_response(self, reply, props):
        msg = {"corr_id": props.correlateion_id,
               'body': reply}
        self._mqttclient.publish(props.reply_to, msg, 1, False)