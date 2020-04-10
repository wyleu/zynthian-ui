"""
Collection of reactions to encoder events.
"""
import RPi.GPIO as GPIO
import logging

from i2cEncoderLibV2 import i2cEncoderLibV2 as i2c

class Encoder(i2c.i2cEncoderLibV2):
    def __init__(self, bus, add):
        self.setup_gpio()
        self.encoder = i2c.i2cEncoderLibV2(bus, add)

    def encoderChange(self):
        self.encoder.writeLEDG(100)
        print ('Changed: %d' % (self.encoder.readCounter32()))
        self.encoder.writeLEDG(0)

    def encoderPush(self):
        self.encoder.writeLEDB(100)
        print ('Encoder Pushed!')
        self.encoder.writeLEDB(0)

    def encoderDoublePush(self):
        self.encoder.writeLEDB(100)
        self.encoder.writeLEDG(100)
        print ('Encoder Double Push!')
        self.encoder.writeLEDB(0)
        self.encoder.writeLEDG(0)

    def encoderMax(self):
        self.encoder.writeLEDR(100)
        print ('Encoder max!')
        self.encoder.writeLEDR(0)

    def encoderMin(self):
        self.encoder.writeLEDR(100)
        print ('Encoder min!')
        self.encoder.writeLEDR(0)

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        self.INT_pin = 4
        GPIO.setup(self.INT_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def add_event_gpio(self):
        def enc_int(self):
            self.encoder.updateStatus()
        GPIO.add_event_detect(self.INT_pin, GPIO.FALLING, callback=enc_int, bouncetime=10)

    def i2c_setup(self):
        encconfig = (
                i2c.INT_DATA | i2c.WRAP_ENABLE | i2c.DIRE_RIGHT | i2c.IPUP_ENABLE | i2c.RMOD_X1 | i2c.RGB_ENCODER)
        self.encoder.begin(encconfig)

        self.encoder.writeCounter(0)
        self.encoder.writeMax(35)
        self.encoder.writeMin(-20)
        self.encoder.writeStep(1)
        self.encoder.writeAntibouncingPeriod(8)
        self.encoder.writeDoublePushPeriod(50)
        self.encoder.writeGammaRLED(i2c.GAMMA_2)
        self.encoder.writeGammaGLED(i2c.GAMMA_2)
        self.encoder.writeGammaBLED(i2c.GAMMA_2)

        self.encoder.onChange = self.encoderChange
        self.encoder.onButtonPush = self.encoderPush
        self.encoder.onButtonDoublePush = self.encoderDoublePush
        self.encoder.onMax = self.encoderMax
        self.encoder.onMin = self.encoderMin

        self.encoder.autoconfigInterrupt()
        print('Board ID code: 0x%X' % (self.encoder.readIDCode()))
        logging.info('Board ID code: 0x%X' % (self.encoder.readIDCode()))
        print('Board Version: 0x%X' % (self.encoder.readVersion()))
        logging.info('Board Version: 0x%X' % (self.encoder.readVersion()))
        logging.error('Board Version: 0x%X' % (self.encoder.readVersion()))

