import spidev


class MCP3008_RPi(object):
    """Class for accessing MCP3008 A/D converter via SPI bus on RPi
    """
    
    def __init__(self):
        # create SPI
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)

    def read(self, adcnum):
        """Read SPI data from the MCP3008, 8 channels in total
        """
        if adcnum > 7 or adcnum < 0:
            return -1
        r = self.spi.xfer2([1, 8 + adcnum << 4, 0])
        data = ((r[1] & 3) << 8) + r[2]
        return data

    



