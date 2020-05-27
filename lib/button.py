from digitalio import DigitalInOut, Direction, Pull


class Button:
    def __init__(self, pin):
        self._button = DigitalInOut(pin)
        self._button.direction = Direction.INPUT
        self._button.pull = Pull.DOWN

        self._value = False

    def reset(self):
        self._value = False

    def is_pressed(self):
        if self._value and self._button.value:
            return True
        elif not self._value and not self._button.value:
            self._value = True

        return False
