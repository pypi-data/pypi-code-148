import asyncio
import random
import logging
# import required libraries & proto defn.
import threading
import grpc
import queue
from proto import base_pb2_grpc, base_pb2, querys_pb2, queues_pb2
from ObjectWithEvents import ObjectWithEvents
# https://stackoverflow.com/questions/65363868/how-to-handle-a-bidirectional-grpc-stream-asynchronously
class Client(ObjectWithEvents.ObjectWithEvents):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.pending = {}
        self.send_queue = queue.SimpleQueue() # or Queue if using Python before 3.7
        self.channel = grpc.insecure_channel(target="localhost:50051")
        self.stub = base_pb2_grpc.grpcServiceStub(channel=self.channel)
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()
    def uniqueid(self):
        self.seed = random.getrandbits(32)
        while True:
            yield self.seed
            self.seed += 1
    def __listen_for_messages(self):
        while True:
            try:
                # self.send_queue = queue.SimpleQueue()  # Should we reset on disconnect ?
                response_iterator = self.stub.SetupStream(iter(self.send_queue.get, None))
                for message in response_iterator:
                    logging.debug("RCV[{}][{}][{}]".format(message.id, message.rid, message.command))
                    msg = self.Unpack(message)
                    if(message.rid in self.pending):
                        self.loop.call_soon_threadsafe(self.pending[message.rid].set_result, msg)
                        self.pending.pop(message.rid, None)
                    else:
                        self.trigger("message", message.command, message.id, msg)
            except Exception as e: 
                # print(e)
                for key in list(self.pending):
                    self.loop.call_soon_threadsafe(self.pending[key].set_exception, e)
                    self.pending.pop(key, None)

    def Unpack(self, message):
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
        elif(message.command == "pong"):
            msg = base_pb2.pong()
            msg.ParseFromString(message.data.value);
            return msg
        else:
            logging.error("Got unknown {} message".format(message.command))
            return None
    def Send(self, request, rid):
        id = str(next(self.uniqueid()))
        request.id = id
        request.rid = rid
        logging.debug("SND[{}][{}][{}]".format(request.id, request.rid, request.command))
        self.send_queue.put(request)
    def RPC(self, request):
        id = str(next(self.uniqueid()))
        request.id = id
        future = asyncio.Future()
        self.pending[id] = future
        logging.debug("SND[{}][{}][{}]".format(request.id, request.rid, request.command))
        self.send_queue.put(request)
        return future
    def Ping(self):
        self.Send(base_pb2.envelope(command="ping"), "")
    def Signin(self, username, password):
        request = base_pb2.envelope(command="signin")
        request.data.Pack(base_pb2.signin(username=username, password=password))
        return self.RPC(request)
    def GetElement(self, xpath):
        request = base_pb2.envelope(command="getelement")
        request.data.Pack(base_pb2.getelement(xpath=xpath))
        return self.RPC(request)
    def RegisterQueue(self, queuename):
        request = base_pb2.envelope(command="registerqueue")
        request.data.Pack(queues_pb2.registerqueue(queuename=queuename))
        return self.RPC(request)
    def QueueMessage(self, queuename, data):
        request = base_pb2.envelope(command="queuemessage")
        request.data.Pack(queues_pb2.queuemessage(queuename=queuename, data=data, striptoken=True))
        return self.RPC(request)
