import json
import traceback
import asyncio
import logging
import zlib
from openiap import client
from google.protobuf import any_pb2 
from proto import base_pb2_grpc, base_pb2
from google.protobuf import json_format

async def onmessage(client, command, rid, message):
    reply = base_pb2.envelope(command=command)
    reply.rid = rid
    try:
        if(command == "getelement"):
            logging.info(f"Server sent getelement {message.xpath}")
            reply.data.Pack(base_pb2.getelement(xpath=f"Did you say {message.xpath} ?"))
        elif(command == "queueevent"):
            data = json.loads(message.data);
            logging.info(f"{str(data['name'])}")
        elif(command == "error"):
            reply.command = "noop"
            logging.error(f"{str(message.message)}")
        else:
            reply.command = "error"
            reply.data.Pack(base_pb2.error(message=f"Unknown command {command}"))
            logging.error(f"Got message with unknown command {command}")
    except Exception as e:
        print("onmessage EXCEPTION!!!!")
        print(repr(e))
        traceback.print_tb(e.__traceback__)
    return reply
async def findme333(message):
    data = json.loads(message.data);
    logging.info(f"findme333: {str(data['name'])}")
async def findme222(message):
    data = json.loads(message.data);
    try:
        logging.info(f"findme222: {str(data['name'])}")
    except:
        logging.info(f"findme222: {str(data['payload']['name'])}")
        pass

async def main():
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    # logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    # logging.basicConfig(level=logging.INFO) # logging.DEBUG logging.INFO
    c = client.Client("grpc://testuser:testuser@localhost:50051")
    # c = client.Client("grpc://testuser:testuser@grpc.demo.openiap.io:443")
    # c.on("message", onmessage)
    c.onmessage = onmessage
    try:
        user = await c.Signin()
        logging.info(f"Signed in as {user.name}")
        q = await c.RegisterQueue("findme333", findme333)
        logging.info(f"Registered queue {q}")
        q = await c.RegisterQueue("findme222", findme222)
        logging.info(f"Registered queue {q}")
    except (Exception,BaseException) as e:
        print("MAIN EXCEPTION!!!!")
        print(repr(e))
        traceback.print_tb(e.__traceback__)
        pass
    
    while True:
        #try:
            text = input("COMMAND")
            print(f"PROCESSING {text}")
            if text == 'p':
                workitem = {"name": "Allan", "test":"Hi mom", "age":23, "files": []}
                filepath = "/home/allan/Pictures/allan.png"
                result = await c.PushWorkitem("q2", "find me", workitem, [filepath], compressed=True)
                logging.info(f"Workitem pushed with id {result._id}")

                workitem = await c.PopWorkitem("q2", True, True)
                if(workitem == None):
                    logging.info("No more workitems in queue q2")                    
                else:
                    try:
                        for f in workitem.files:
                            if f.compressed:
                                with open("download.png", "wb") as out_file:
                                    out_file.write(zlib.decompress(f.file))
                            else:
                                with open("download.png", "wb") as out_file:
                                    out_file.write(f.file)
                        logging.info(f"Popped workitem id {workitem._id}")
                        workitem.state = "successful"
                        payload = json.loads(workitem.payload)
                        # payload =json_format.MessageToDict(workitem.payload)
                        # logging.info(f"payload name {payload.name} workitem name {workitem.name}")
                        # logging.info(f"payload name {payload['name']}  workitem name {workitem.name}")
                        logging.info(f"payload name {payload['name']}  workitem name {workitem.name}")
                        payload['name'] = "Allan 2222"
                        workitem.payload = json.dumps(payload)
                        workitem = await c.UpdateWorkitem(workitem)
                        logging.info(f"Popped workitem id {workitem._id} now in state {workitem.state}")
                    except (Exception,BaseException) as e:
                         workitem.state = "retry"
                         workitem.errortype = "business" # business / application
                         workitem.errormessage = "".join(traceback.format_exception_only(type(e), e)).strip()
                         workitem.errorsource = ''.join(traceback.format_exception(e))
                         await c.UpdateWorkitem(workitem)
                         print("Workitem EXCEPTION!!!!")
                         print(repr(e))
                         traceback.print_tb(e.__traceback__)
                         pass
            elif text == 's':
                signin = await c.Signin()
                logging.info(f"Signed in as {signin.name}")
            elif text == 'q':
                await c.QueueMessage("findme222", '{"name":"py find me"}')
            elif text == 'push':
                workitem = {"test":"Hi mom", "age":23}
                result = await c.PushWorkitem("q2", "find me", workitem)
                logging.info(f"Workitem pushed with id {result._id}")
            else:
                xpath = await c.GetElement(text)
                logging.info(xpath)
        # except (Exception,BaseException) as e:
        #     print("MAIN EXCEPTION!!!!")
        #     print(repr(e))
        #     traceback.print_tb(e.__traceback__)
        #     pass
if __name__ == '__main__':
    asyncio.run(main())
