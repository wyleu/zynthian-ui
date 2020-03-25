import smbus2
import RPi.GPIO as GPIO
from time import sleep
import Source.i2cEncoderLibV2 as i2c

ENCODERS = {
    0x41: "Encoder 1",
    0x42: "Encoder 2",
    0x43: "Encoder 3",
    0x44: "Encoder 4"
}

class Encoders:
    def __init__(self):
        self.encoders = None
        self.INT_pin = 7  # 4 GPIO.BCM
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.INT_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(
            self.INT_pin,
            GPIO.BOTH,
            callback=self.Encoder_INT,
            bouncetime=10)


    def run(self):
        with smbus2.SMBus(1) as bus:
            self.encoders = [Encoder(bus, add) for add in ENCODERS]
            for encoder in self.encoders:
                encoder.blip()
            while True:
                try:
                    pass
                except KeyboardInterrupt:
                    GPIO.cleanup()
        GPIO.cleanup()

    def Encoder_INT(self, channel):
        for encoder in self.encoders:
            if encoder.updateStatus():
                print('encoder %s %s' % (encoder, encoder.stat))


class Encoder(i2c.i2cEncoderLibV2):
    def __init__(self, bus, add, name=None):
        super().__init__(bus, add)
        if name:
            self.name = name
        else:
            self.name = str(add)

        encconfig = (
                i2c.INT_DATA |
                i2c.WRAP_ENABLE |
                i2c.DIRE_RIGHT |
                i2c.IPUP_ENABLE |
                i2c.RMOD_X1 |
                i2c.RGB_ENCODER)

        self.begin(encconfig)
        self.set_encoder()
        self.onChange = self.EncoderChange
        self.onButtonPush = self.EncoderPush
        self.onButtonRelease = self.EncoderRelease
        # self.onButtonDoublePush = self.EncoderDoublePush
        self.onMax = self.EncoderMax
        self.onMin = self.EncoderMin
        self.autoconfigInterrupt()
        self.blip()

    def __str__(self):
        return self.name

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
        self.clear()

    def EncoderChange(self):
        self.writeLEDG(100)
        print('Encoder %s Changed: %d' % (self.name, self.readCounter32()))
        self.writeLEDG(0)

    def EncoderPush(self):
        self.writeLEDB(100)
        print ('Encoder %s Pushed!'  % (self.name,))
        self.writeLEDB(0)

    def EncoderRelease(self):
        self.writeLEDG(100)
        print ('Encoder %s Released!'  % (self.name,))
        self.writeLEDG(0)

    # def EncoderDoublePush(self):
    #     self.writeLEDB(100)
    #     self.writeLEDG(100)
    #     print ('Encoder %s Double Push!' % (self.name,))
    #     self.writeLEDB(0)
    #     self.writeLEDG(0)

    def EncoderMax(self):
        self.writeLEDR(100)
        print ('Encoder %s max!' % (self.name,))
        self.writeLEDR(0)

    def EncoderMin(self):
        self.writeLEDR(100)
        print ('Encoder %s min!' % (self.name,))
        self.writeLEDR(0)


if __name__ == '__main__':
    Encoders().run()