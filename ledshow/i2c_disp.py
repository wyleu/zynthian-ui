import smbus2


import RPi.GPIO as GPIO
import logging
from time import sleep
import Source.i2cEncoderLibV2 as i2c

ENCODERS = {
    0x41: "Encoder 1",
    0x42: "Encoder 2",
    0x43: "Encoder 3",
    0x44: "Encoder 4"
}

try:
    logging.info("i2c_disp started cleanly...")
except Exception as e:
    logging.error("ERROR initializing i2c_disp: %s" % e)


class Encoder(i2c.i2cEncoderLibV2):
    def __init__(self, bus, add):
        super().__init__(bus, add)

    def set_encoder(self):
        self.writeCounter(0)
        self.writeMax(35)
        self.writeMin(-20)
        self.writeStep(1)
        self.writeAntibouncingPeriod(8)
        self.writeDoublePushPeriod(50)
        self.writeGammaRLED(i2c.GAMMA_2)
        self.writeGammaGLED(i2c.GAMMA_2)
        self.writeGammaBLED(i2c.GAMMA_2)

    def clear(self):
        self.writeRGBCode(0x00)

    def blip(self):
        self.writeRGBCode(0x000064)
        sleep(0.2)
        encoder.clear()

    def EncoderChange(self):
        self.writeLEDG(100)
        print('Changed: %d' % (self.readCounter32()))
        self.writeLEDG(0)




if __name__ == '__main__':

    def Encoder_INT():
        print ('Encoder Interupt')

    INT_pin = 7
    GPIO.setmode(GPIO.BOARD)

    with smbus2.SMBus(1) as bus:
        GPIO.setup(INT_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        encoders = [Encoder(bus, add) for add in ENCODERS]

        encconfig = (
                    i2c.INT_DATA |
                    i2c.WRAP_ENABLE |
                    i2c.DIRE_RIGHT |
                    i2c.IPUP_ENABLE |
                    i2c.RMOD_X1 |
                    i2c.RGB_ENCODER)

        for encoder in encoders:
            encoder.begin(encconfig)
            encoder.set_encoder()
            encoder.autoconfigInterrupt()
            encoder.onChange=encoder.EncoderChange
            encoder.blip()

        GPIO.add_event_detect(
            INT_pin,
            GPIO.FALLING,
            callback=Encoder_INT,
            bouncetime=10)

        for encoder in encoders:
            encoder.blip()


            try:
                while True:
                    pass
            except KeyboardInterrupt as e:
                print('Error:-', e)
                for encoder in encoders:
                    encoder.blip()




    GPIO.setmode(GPIO.BCM)
    with smbus2.SMBus(1) as bus:
        INT_pin = 4
        GPIO.setup(INT_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        encoder = i2c.i2cEncoderLibV2(bus, 0x41)
        encoder2 = i2c.i2cEncoderLibV2(bus, 0x42)
        encoder3 = i2c.i2cEncoderLibV2(bus, 0x43)
        encoder4 = i2c.i2cEncoderLibV2(bus, 0x44)

        # Simple callback that ist's called when the encoder is rotated and blink the green led #

        encconfig = (
                    i2c.INT_DATA | i2c.WRAP_ENABLE | i2c.DIRE_RIGHT | i2c.IPUP_ENABLE | i2c.RMOD_X1 | i2c.RGB_ENCODER)
        encoder.begin(encconfig)
        encoder2.begin(encconfig)
        encoder3.begin(encconfig)
        encoder4.begin(encconfig)

        def encoder_change(encoder):
            def EncoderChange():
                encoder.writeLEDG(100)
                print('Changed: %d' % (encoder.readCounter32()))
                encoder.writeLEDG(0)
            return EncoderChange()


        def Encoder_INT(self):
            encoder.updateStatus()

        def set_encoder(encoder):
            encoder.writeCounter(0)
            encoder.writeMax(35)
            encoder.writeMin(-20)
            encoder.writeStep(1)
            encoder.writeAntibouncingPeriod(8)
            encoder.writeDoublePushPeriod(50)
            encoder.writeGammaRLED(i2c.GAMMA_2)
            encoder.writeGammaGLED(i2c.GAMMA_2)
            encoder.writeGammaBLED(i2c.GAMMA_2)

        set_encoder(encoder)
        set_encoder(encoder2)
        set_encoder(encoder3)
        set_encoder(encoder4)

        encoder.onChange = encoder_change(encoder)  # Attach the event to the callback function#
        encoder2.onChange = encoder_change(encoder2)  # Attach the event to the callback function#
        encoder3.onChange = encoder_change(encoder3)  # Attach the event to the callback function#
        encoder4.onChange = encoder_change(encoder4)  # Attach the event to the callback function#

        encoder.autoconfigInterrupt()
        encoder2.autoconfigInterrupt()
        encoder3.autoconfigInterrupt()
        encoder4.autoconfigInterrupt()

        encoder2.writeLEDR(60)
        encoder3.writeLEDG(60)
        encoder4.writeLEDB(60)

        encoder.writeRGBCode(0x640000)
        sleep(0.3)
        encoder.writeRGBCode(0x006400)
        sleep(0.3)
        encoder.writeRGBCode(0x000064)
        sleep(0.3)

        encoder.writeRGBCode(0x00)
        encoder2.writeRGBCode(0x00)
        encoder3.writeRGBCode(0x00)
        encoder4.writeRGBCode(0x00)

        print('Board ID code: 0x%X' % (encoder.readIDCode()))
        logging.info('Info Board ID code: 0x%X' % (encoder.readIDCode()))
        print('Board Version: 0x%X' % (encoder.readVersion()))
        logging.info('Info Board Version: 0x%X' % (encoder.readVersion()))
        logging.error('Error Board Version: 0x%X' % (encoder.readVersion()))

        GPIO.add_event_detect(INT_pin, GPIO.FALLING, callback=Encoder_INT, bouncetime=10)

        while True:
            pass

