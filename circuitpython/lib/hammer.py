from adafruit_motor import servo
from pulseio import PWMOut

CLICK_PRESS_DURATION = 0.2


class Hammer:
    DEFAULT = 0
    REST = 89
    PRESSED = 96

    def __init__(self, pin, wait):
        self._servo = servo.Servo(PWMOut(pin, duty_cycle=2 ** 15, frequency=5))
        self.wait = wait

    def _setAngle(self, angle):
        self._servo.angle = angle

    def default(self):
        self._setAngle(self.DEFAULT)

    def rest(self):
        self._setAngle(self.REST)

    def pressed(self):
        self._setAngle(self.PRESSED)

    def click(self):
        self.pressed()
        self.wait.sleep(CLICK_PRESS_DURATION)
        self.rest()
