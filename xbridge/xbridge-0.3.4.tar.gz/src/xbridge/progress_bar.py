

from progress.bar import Bar

class TranferBar(Bar):
    suffix='%(percent)d%% | %(eta_td)s/%(elapsed_td)s | %(size)s | %(speed)s ' 

    @property
    def speed(self):
        Bps = 1.0 / self.avg
        return size_string(Bps) + '/s'
        
    @property
    def size(self):
        return size_string(float(self.max))

def size_string(byte: float):
    
    if byte < 1024:
        return '%.2f B' % byte
    
    KB = byte / 1024
    if KB < 1024:
        return '%.2f KB' % KB

    MB = KB / 1024
    if MB < 1024:
        return '%.2f MB' % MB

    GB = MB / 1024
    return '%.2f GB' % GB
