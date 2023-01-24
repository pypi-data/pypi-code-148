import os
from tqdm import tqdm
import psutil
import time
import fire

class mysystemmonitor:
    def __init__(self, interval=2, nosystemload=False, nomemoryusage=False, nodiskusage=False):
        self.total = 100
        self.interval = interval
        
        self.nosystemload = nosystemload
        self.nomemoryusage = nomemoryusage
        self.nodiskusage = nodiskusage

    def system_load(self):
        load = psutil.getloadavg()
        return (load[0] / psutil.cpu_count()) * 100

    def memory_usage(self):
        memory = psutil.virtual_memory()
        return memory.percent

    def disk_usage(self):
        disk = psutil.disk_usage('/')
        return disk.percent

    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    
    def run(self):
        while True:
            self.clear()
            if not self.nosystemload:
                with tqdm(total=self.total, desc="SYSTEM LOAD") as pbar:
                    load = self.system_load()
                    pbar.update(load)
            if not self.nomemoryusage:
                with tqdm(total=self.total, desc="MEMORY USAGE") as pbar:
                    memory = self.memory_usage()
                    pbar.update(memory)
            if not self.nodiskusage:
                with tqdm(total=self.total, desc="DISK USAGE") as pbar:
                    disk = self.disk_usage()
                    pbar.update(disk)
            time.sleep(self.interval)

def main():
    fire.Fire(mysystemmonitor)
