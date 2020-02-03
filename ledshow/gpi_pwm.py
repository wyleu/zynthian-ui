import time
import RPi.GPIO as GPIO

gpio_modes = {
    GPIO.BOARD: 'Pins on Board',
    GPIO.BCM: 'Pins on BCM'
}

GPIO.setmode(GPIO.BOARD)
print(gpio_modes[GPIO.getmode()])

gpio_pinmodes = {
    GPIO.IN: 'In',
    GPIO.OUT: 'Out',
    GPIO.SPI: 'SPI',
    GPIO.I2C: 'I2C',
    GPIO.HARD_PWM: 'PWM',
    GPIO.SERIAL: 'Serial',
    GPIO.UNKNOWN: 'Unknown'
}

colour_pins = {
    'r': 33,
    'b': 32,
    'g': 36
}

for i in range(1, 41, 2):
    for j in range(2):
        if j == 0:
            try:
                print(i, gpio_pinmodes[GPIO.gpio_function(i)]),
            except:
                print(i, '----'),
        if j == 1:
            try:
                print(i + j, gpio_pinmodes[GPIO.gpio_function(i + j)]),
            except:
                print(i + j, '----'),
        print('')

GPIO.setup(32, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)

def generator(offset, low, high):
    direction = 1 # Up
    value = offset
    while True:
        value = value + direction
        if value in (low, high):
            direction = direction * -1
        yield value

red_gen = generator(0, 0, 100)
green_gen = generator(int(100 / 3), 0, 100)
blue_gen = generator(int(200 / 3), 0, 100)

# An example to brighten/dim an LED:

b = GPIO.PWM(32, 50)  # channel=32 frequency=50Hz
r = GPIO.PWM(33, 50)
g = GPIO.PWM(36, 50)


b.start(0)
r.start(0)
g.start(0)

if __name__ == '__main__':
    try:
        while 1:
            b.ChangeDutyCycle(next(blue_gen))
            r.ChangeDutyCycle(next(red_gen))
            g.ChangeDutyCycle(next(green_gen))
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    b.stop()
    r.stop()
    g.stop()
    GPIO.cleanup()

