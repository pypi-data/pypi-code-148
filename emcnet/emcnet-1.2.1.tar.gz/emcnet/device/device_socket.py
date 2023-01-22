import socket
import json


class DeviceSocket:

    def __init__(self, device_id='Unknown', gateway_address='localhost', gateway_port=10000):
        # Create a UDP socket
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.gateway_address = (gateway_address, gateway_port)
        self.device_id = device_id

    def send_command(self, sock, message, log=True):
        if log:
            print('Sending:')
            print(message)
        sock.sendto(message.encode('utf-8'), self.gateway_address)

        # Receive response
        # if log:
        #     print('Waiting for response')
        # response, _ = sock.recvfrom(4096)
        # if log:
        #     print('Received: "{}"'.format(response))
        #
        # return response

    def make_message_into_jsonstring(self, action, data=None):
        if data is not None:
            packet = {"device": self.device_id, "action": action, "data": data}
        else:
            packet = {"device": self.device_id, "action": action}
        return json.dumps(packet)

    def message_gateway(self, action, data, log=False):
        message_string = self.make_message_into_jsonstring(action, data)
        self.send_command(self.client_sock, message_string, log=log)

    def close(self):
        self.client_sock.close()

