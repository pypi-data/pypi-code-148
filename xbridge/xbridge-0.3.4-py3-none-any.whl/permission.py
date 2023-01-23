


import json
import os
from typing import List

# class PermItem:
    

class Permission:
    permissions_filename = 'permissions.json'

    clients: List[any]

    def __init__(self, clients):
        self.clients = clients
        pass


    @classmethod
    def load(cls, dir: str):
        permisson_file = os.path.join(dir, Permission.permissions_filename)
    
        clients = []
        if os.path.isfile(permisson_file):
            with open(permisson_file, mode='r') as file:
                clients = json.load(file)
      
        return Permission(clients)

    def allowConnect(self, client_hash: str) -> bool:
        return True
        for c in self.clients:
            if c['client_hash'] == client_hash:
                if c['allow_connect'] == True:
                    return True
                return False
        return False

    def allowAction(self, client_hash: str, action: str) -> bool:
        return True
        if action == "":
    
            return True
        try:
            for c in self.clients:
                if c['client_hash'] == client_hash:
                    if c['allow_actions'][action] == True:
                        return True
                    return False
        except:
            return False
        return False