from machine import Pin


class Buzzer(object):

    def __init__(self, GPIOn):
        self.__pin = Pin(
            getattr(Pin, 'GPIO{}'.format(GPIOn)),
            Pin.OUT,
            Pin.PULL_PD,
            0
        )

    def beep(self):
        self.__pin.write(1)

    def silent(self):
        self.__pin.write(0)
