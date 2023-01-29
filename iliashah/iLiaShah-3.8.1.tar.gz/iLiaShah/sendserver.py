from iLiaShah.WebAdress import server_bot
import random
from random import choice

class send_server_rubika:
    
    def server_full(self):
        return choice(server_bot.list_servers)

    def server_files(self):
        return choice(server_bot.list_servers)