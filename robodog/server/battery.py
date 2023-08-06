import logging
import time

import smbus

logger = logging.getLogger(__name__)


class ADS7830:
    def __init__(self):
        # Get I2C bus
        self.bus = smbus.SMBus(1)
        # I2C address of the device
        self.ADS7830_DEFAULT_ADDRESS = 0x48
        # ADS7830 Command Set
        self.ADS7830_CMD = 0x84  # Single-Ended Inputs

    def readAdc(self, channel):
        """Select the Command data from the given provided value above"""
        COMMAND_SET = self.ADS7830_CMD | ((((channel << 2) | (channel >> 1)) & 0x07) << 4)
        self.bus.write_byte(self.ADS7830_DEFAULT_ADDRESS, COMMAND_SET)
        data = self.bus.read_byte(self.ADS7830_DEFAULT_ADDRESS)
        return data

    def power(self, channel):
        data = [self.readAdc(channel) for _ in range(9)]
        data.sort()
        # I guess this is taking the median
        battery_voltage = data[4] / 255.0 * 5.0 * 3
        return battery_voltage


def test():
    adc = ADS7830()
    logger.info("Reading battery voltage:")
    try:
        while True:
            power = adc.power(0)
            print(f"{power}V")
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("End of program")


if __name__ == "__main__":
    from robodog.server.config import configure_logging

    configure_logging()
    test()
