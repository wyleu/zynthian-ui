"""
Collection of reactions to encoder events.
"""
from Source import i2cEncoderLibV2

class Encoder():
    def __init__(self, bus, port):

        self.encoder = i2cEncoderLibV2.i2cEncoderLibV2(bus, 0x41)

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