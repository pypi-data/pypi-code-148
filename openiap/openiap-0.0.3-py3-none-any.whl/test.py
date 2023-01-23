import asyncio
import logging
from api_openiap import client
import json 
from google.protobuf import any_pb2 
from proto import base_pb2_grpc, base_pb2

def onmessage(client, command, rid, message):
    reply = base_pb2.envelope(command=command)
    reply.rid = rid
    try:
        if(command == "getelement"):
            logging.info("{}".format(message.xpath) )
        elif(command == "queueevent"):
            data = json.loads(message.data);
            logging.info("{}".format(str(data['name'])) )
        else:
            logging.info("Got {} message event".format(command))
    except Exception as e: 
        print(e)
    client.Send(reply, rid)

async def main():
    logging.basicConfig(level=logging.INFO) # logging.DEBUG logging.INFO
    password = input("password for allan5")
    c = client.Client()
    c.on("message", onmessage)
    signin = await c.Signin("allan5", password)
    q = await c.RegisterQueue("findme333")
    q = await c.RegisterQueue("findme222")
    # logging.info("Signed in as {} with token {}".format(signin.user.name, signin.jwt) )
    logging.info("Signed in as {}".format(signin.user.name) )
    while True:
        text = input("")
        if text == 'p':
            c.Ping()
        elif text == 's':
            signin = await c.Signin("allan5", password)
            logging.info("Signed in as {}".format(signin.user.name) )
        elif text == 'q':
            await c.QueueMessage("findme222", '{"name":"py find me"}')
            # logging.info("Signed in as {}".format(signin.user.name) )
        else:
            getelement = await c.GetElement(text)
            logging.info(getelement.xpath)

if __name__ == '__main__':
    asyncio.run(main())
