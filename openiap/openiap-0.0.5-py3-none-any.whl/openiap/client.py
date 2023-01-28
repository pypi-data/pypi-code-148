from urllib.parse import urlparse
from queue import Queue
import traceback
#import queue
import gzip
import os
import json
from datetime import datetime
# from concurrent import futures
import asyncio
import random
import time
import logging
import functools
import threading

import grpc
from proto.base_pb2_grpc import grpcServiceStub
from proto.base_pb2 import envelope
from proto import base_pb2
from proto import queues_pb2
from proto import workitems_pb2
from ObjectWithEvents import ObjectWithEvents

class Client(ObjectWithEvents.ObjectWithEvents):
    def __init__(self, url):
        self.url = url
        if(self.url == None or self.url == ""): self.url = "grpc://grpc.app.openiap.io:443"
        self.loop = asyncio.get_event_loop()
        self.pending = {}
        self.messagequeues = {}
        self.queue = Queue()
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
        # self.send_queue = queue.SimpleQueue() # or Queue if using Python before 3.7
        # threading.Thread(target=self.__server_pinger, args=(queue,)).start()
        # threading.Thread(target=self.__listen_for_messages, args=(queue,)).start()
        # threading.Thread(target=self.__server_pinger, daemon=True).start()

        # uri = urlparse(self.url)
        # if(uri.username != None and uri.username != "" and uri.password != None and uri.password != ""):
        #     self.__login_event = threading.Event()
        #     threading.Thread(target=self.__Signin, args=(uri.username, uri.password,)).start()
        #     self.__login_event.wait(timeout=None)
    def uniqueid(self):
        self.seed = random.getrandbits(32)
        while True:
            yield self.seed
            self.seed += 1
    def __Unpack(self, message):
        if(message.command == "getelement"):
            msg = base_pb2.getelement()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "signinreply"):
            msg = base_pb2.signinreply()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "registerqueuereply"):
            msg = queues_pb2.registerqueuereply()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "queuemessagereply"):
            msg = queues_pb2.queuemessagereply()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "queueevent"):
            msg = queues_pb2.queueevent()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "pushworkitemreply"):
            msg = workitems_pb2.pushworkitemreply()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "popworkitemreply"):
            msg = workitems_pb2.popworkitemreply()
            if(message.data.value != None and message.data.value != "" and message.data.value != b""):
                msg.ParseFromString(message.data.value);
                return msg
            else:
                return None
        elif(message.command == "updateworkitemreply"):
            msg = workitems_pb2.updateworkitemreply()
            if(message.data.value != None and message.data.value != "" and message.data.value != b""):
                msg.ParseFromString(message.data.value);
                return msg
            else:
                return None                
        elif(message.command == "pong"):
            msg = base_pb2.pong()
            msg.ParseFromString(message.data.value);
            return msg
        elif(message.command == "error"):
            msg = base_pb2.error()
            msg.ParseFromString(message.data.value);
            return msg
        else:
            logging.error(f"Got unknown {message.command} message")
            return None
    def __connect_and_listen(self, itr):
        try:
            uri = urlparse(self.url)
            logging.info(f"Connecting to {uri.hostname}:")
            if(uri.port == 443 or uri.port == "443"):
                credentials = grpc.ssl_channel_credentials()
                chan = grpc.secure_channel(f"{uri.hostname}:{uri.port}", credentials, options=(('grpc.ssl_target_name_override', uri.hostname),))
            else:
                chan = grpc.insecure_channel(f"{uri.hostname}:{uri.port}")
            fut = grpc.channel_ready_future(chan)
            while not fut.done():
                logging.debug("channel is not ready")
                time.sleep(1)
            logging.debug(f"Create stub and connect streams")
            stub = grpcServiceStub(chan)
            for message in stub.SetupStream(itr):
                logging.debug(f"RCV[{message.id}][{message.rid}][{message.command}]")
                self.__parse_message(message)
        except Exception as e:
            print(repr(e))
            traceback.print_tb(e.__traceback__)
            pass
        logging.debug(f"Close channels")
        for id in self.pending:
            err = ValueError("Channel closed")
            self.loop.call_soon_threadsafe(self.pending[id].set_exception, err)
        for id in self.pending:
            err = ValueError("Channel closed")
            self.loop.call_soon_threadsafe(self.pending[id].set_exception, err)
        chan.close()
    async def onmessage(self, client, command, rid, message):
        logging.info(f"Got {command} message event")
    def __parse_message(self, message):
        msg = self.__Unpack(message)
        if(message.rid in self.pending):
            if(message.command == "error"):
                #raise ValueError(msg.message)
                self.loop.call_soon_threadsafe(self.pending[message.rid].set_exception, ValueError(msg.message))
            else:
                self.loop.call_soon_threadsafe(self.pending[message.rid].set_result, msg)
            self.pending.pop(message.rid, None)
        else:
            if(message.command == "queueevent" and msg.queuename in self.messagequeues):
                asyncio.run(self.messagequeues[msg.queuename](msg))                
            else:
                # self.trigger("message", message.command, message.id, msg)
                reply = asyncio.run(self.onmessage(self, message.command, message.id, msg))
                if(reply.command != "noop"):
                    self.Send(reply, message.id)
    def __server_pinger(self):
        count = 0
        while True:
            time.sleep(5)
            asyncio.run(self.__ping())
            # message = envelope(command="ping")
            # self.queue.put(message)
            count += 1
    def __request_iterator(self, connectonid):
        logging.debug(f"Waiting for message for connecton id {connectonid}")
        message = self.queue.get()
        if(connectonid != self.connectonid):
            self.queue.put(message)
            return None
        logging.debug(f"Process sending message for connecton id {connectonid}")
        if(message.id == None or message.id == ""): message.id = str(next(self.uniqueid()))
        logging.debug(f"SND[{message.id}][{message.rid}][{message.command}]")
        return(message)

    def __listen_for_messages(self):
        while True:
            self.connectonid = str(next(self.uniqueid()))
            count = 0
            logging.debug(f"Estabilish connecton id {self.connectonid}")
            self.__connect_and_listen(
                iter(functools.partial(self.__request_iterator, self.connectonid), None)
            )
            count += 1
            logging.debug(f"Reconnect number {count}")
            time.sleep(2)
    def __RPC(self, request):
        id = str(next(self.uniqueid()))
        request.id = id
        future = asyncio.Future()
        self.pending[id] = future
        self.queue.put(request)
        return future
    async def __ping(self):
        # self.__Send(base_pb2.envelope(command="ping"), "")
        # self.queue.put(base_pb2.envelope(command="ping"))
        await self.__RPC(base_pb2.envelope(command="ping"))
    def Send(self, request, rid):
        if(rid == None or rid == ""): raise ValueError("RID is mandatory")
        id = str(next(self.uniqueid()))
        request.id = id
        request.rid = rid
        self.queue.put(request)
        # 
    def __Signin(self, username, password):
        signin = asyncio.run(self.Signin(username, password))
        logging.info(f"Signed in as {signin.name}" )
        self.__login_event.set()
    async def Signin(self, username=None, password=None):
        request = base_pb2.envelope(command="signin")
        if(username == None and password==None):
            uri = urlparse(self.url)
            if(uri.username != None and uri.username != "" and uri.password != None and uri.password != ""):
                username=uri.username
                password=uri.password
        if(password== None or password == ""):
            request.data.Pack(base_pb2.signin(jwt=username))
        else:
            request.data.Pack(base_pb2.signin(username=username, password=password))
        result = await self.__RPC(request)
        self.jwt = result.jwt
        self.user = result.user
        return result.user
    async def GetElement(self, xpath):
        request = base_pb2.envelope(command="getelement")
        request.data.Pack(base_pb2.getelement(xpath=xpath))
        result = await self.__RPC(request)
        return result.xpath
    async def RegisterQueue(self, queuename, callback):
        request = base_pb2.envelope(command="registerqueue")
        request.data.Pack(queues_pb2.registerqueue(queuename=queuename))
        result = await self.__RPC(request)
        self.messagequeues[result.queuename] = callback
        return result.queuename
    async def QueueMessage(self, queuename, data):
        request = base_pb2.envelope(command="queuemessage")
        request.data.Pack(queues_pb2.queuemessage(queuename=queuename, data=data, striptoken=True))
        return self.__RPC(request)
    async def PushWorkitem(self, wiq:str, name:str, payload:dict, files: any = None, wiqid:str = None, nextrun: datetime = None, priority: int = 2, compressed: bool = False):
        request = base_pb2.envelope(command="pushworkitem")
        _files = []
        if(files != None):
            for filepath in files:
                filename = os.path.basename(filepath)
                if compressed == True:
                    with open(filepath, mode="rb") as content:
                        _files.append({"filename":filename, "compressed": compressed, "file": gzip.compress(content.read())})
                else:
                    with open(filepath, mode="rb") as content:
                        _files.append({"filename":filename, "compressed": compressed, "file": content.read()})
        q = workitems_pb2.pushworkitem(wiq=wiq,name=name, files=_files, wiqid=wiqid, nextrun=nextrun, priority=priority )
        q.payload = json.dumps(payload)
        request.data.Pack(q)
        result = await self.__RPC(request)
        return result.workitem;
    async def PopWorkitem(self, wiq:str,includefiles:bool=False,compressed:bool=False):
        request = base_pb2.envelope(command="popworkitem")
        request.data.Pack(workitems_pb2.popworkitem(wiq=wiq,includefiles=includefiles,compressed=compressed))
        result = await self.__RPC(request)
        if(result == None): return None
        return result.workitem;
    async def UpdateWorkitem(self, workitem):
        request = base_pb2.envelope(command="updateworkitem")
        uwi = workitems_pb2.updateworkitem(workitem = workitem);
        request.data.Pack(uwi)
        result = await self.__RPC(request)
        if(result == None): return None
        return result.workitem;
