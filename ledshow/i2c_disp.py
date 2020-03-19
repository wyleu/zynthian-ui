import smbus2
import RPi.GPIO as GPIO

import logging
from time import sleep
import Source.i2cEncoderLibV2 as i2c

from encoder import Encoder

try:
    logging.info("i2c_disp started cleanly...")
except Exception as e:
    logging.error("ERROR initializing i2c_disp: %s" % e)


def main(reactor):
    GPIO.setmode(GPIO.BCM)
    INT_pin = 4
    GPIO.setup(INT_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    encoder = reactor.encoder

    def enc_int(self):
        encoder.updateStatus()

    encconfig = (
                i2c.INT_DATA | i2c.WRAP_ENABLE | i2c.DIRE_RIGHT | i2c.IPUP_ENABLE | i2c.RMOD_X1 | i2c.RGB_ENCODER)
    encoder.begin(encconfig)

    encoder.writeCounter(0)
    encoder.writeMax(35)
    encoder.writeMin(-20)
    encoder.writeStep(1)
    encoder.writeAntibouncingPeriod(8)
    encoder.writeDoublePushPeriod(50)
    encoder.writeGammaRLED(i2c.GAMMA_2)
    encoder.writeGammaGLED(i2c.GAMMA_2)
    encoder.writeGammaBLED(i2c.GAMMA_2)

    encoder.onChange = reactor.encoderChange
    encoder.onButtonPush = reactor.encoderPush
    encoder.onButtonDoublePush = reactor.encoderDoublePush
    encoder.onMax = reactor.encoderMax
    encoder.onMin = reactor.encoderMin

    encoder.autoconfigInterrupt()
    print('Board ID code: 0x%X' % (encoder.readIDCode()))
    print('Board Version: 0x%X' % (encoder.readVersion()))

    encoder.writeRGBCode(0x640000)
    sleep(0.3)
    encoder.writeRGBCode(0x006400)
    sleep(0.3)
    encoder.writeRGBCode(0x000064)
    sleep(0.3)
    encoder.writeRGBCode(0x00)

    GPIO.add_event_detect(INT_pin, GPIO.FALLING, callback=enc_int, bouncetime=10)

    while True:
        #  if GPIO.input(INT_pin) == False: #
        #     Encoder_INT() #
        pass


if __name__ == '__main__':
    bus = smbus2.SMBus(1)
    reactor = Encoder(bus, 0x41)

    main(reactor)
    while True:
        #  if GPIO.input(INT_pin) == False: #
        #     Encoder_INT() #
        pass