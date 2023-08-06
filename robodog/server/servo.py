import logging
import math
import time

import smbus

logger = logging.getLogger(__name__)


class PCA9685:
    """Raspi PCA9685 16-Channel PWM Servo Driver"""

    # Registers/etc.
    __SUBADR1 = 0x02
    __SUBADR2 = 0x03
    __SUBADR3 = 0x04
    __MODE1 = 0x00
    __PRESCALE = 0xFE
    __LED0_ON_L = 0x06
    __LED0_ON_H = 0x07
    __LED0_OFF_L = 0x08
    __LED0_OFF_H = 0x09
    __ALLLED_ON_L = 0xFA
    __ALLLED_ON_H = 0xFB
    __ALLLED_OFF_L = 0xFC
    __ALLLED_OFF_H = 0xFD

    def __init__(self, address=0x40, debug=False):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.debug = debug
        self.write(self.__MODE1, 0x00)

    def write(self, reg, value):
        "Writes an 8-bit value to the specified register/address"
        self.bus.write_byte_data(self.address, reg, value)

    def read(self, reg):
        "Read an unsigned byte from the I2C device"
        result = self.bus.read_byte_data(self.address, reg)
        return result

    def setPWMFreq(self, freq):
        "Sets the PWM frequency"
        prescaleval = 25000000.0  # 25MHz
        prescaleval /= 4096.0  # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        prescale = math.floor(prescaleval + 0.5)

        oldmode = self.read(self.__MODE1)
        newmode = (oldmode & 0x7F) | 0x10  # sleep
        self.write(self.__MODE1, newmode)  # go to sleep
        self.write(self.__PRESCALE, int(math.floor(prescale)))
        self.write(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.write(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        "Sets a single PWM channel"
        self.write(self.__LED0_ON_L + 4 * channel, on & 0xFF)
        self.write(self.__LED0_ON_H + 4 * channel, on >> 8)
        self.write(self.__LED0_OFF_L + 4 * channel, off & 0xFF)
        self.write(self.__LED0_OFF_H + 4 * channel, off >> 8)

    def setMotorPwm(self, channel, duty):
        self.setPWM(channel, 0, duty)

    def setServoPulse(self, channel, pulse):
        "Sets the Servo Pulse,The PWM frequency must be 50HZ"
        pulse = pulse * 4096 / 20000  # PWM frequency is 50HZ,the period is 20000us
        self.setPWM(channel, 0, int(pulse))


class Servo:
    def __init__(self):
        self.angleMin = 18
        self.angleMax = 162
        self.pwm = PCA9685(address=0x40, debug=True)
        self.pwm.setPWMFreq(50)  # Set the cycle frequency of PWM

    # Convert the input angle to the value of pca9685
    def map(self, value, fromLow, fromHigh, toLow, toHigh):
        return (toHigh - toLow) * (value - fromLow) / (fromHigh - fromLow) + toLow

    def setServoAngle(self, channel, angle):
        if angle < self.angleMin:
            angle = self.angleMin
        elif angle > self.angleMax:
            angle = self.angleMax
        data = self.map(angle, 0, 180, 102, 512)
        logging.debug(data, data / 4096 * 0.02)
        self.pwm.setPWM(channel, 0, int(data))


def test_90():
    logger.info("Now servos will rotate to 90°.")
    logger.info("If they have already been at 90°, nothing will be observed.")
    logger.info("Please keep the program running when installing the servos.")
    logger.info("After that, you can press ctrl-C to end the program.")
    S = Servo()
    while True:
        try:
            for i in range(16):
                S.setServoAngle(i, 90)
        except KeyboardInterrupt:
            logger.info("\nEnd of program")
            break


if __name__ == "__main__":
    from robodog.config import configure_logging

    configure_logging()
    test_90()
