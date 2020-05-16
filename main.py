from time import sleep
import board
import pulseio
from adafruit_motor import servo
from functools import reduce
import rotaryio

from button import Button
from sequences import SEQUENCES

class Wait():
    def __init__(self, cancel_button):
        self.cancel_button = cancel_button

    def sleep(self, seconds):
        sleep(seconds)

    def interruptible_sleep(self, seconds, increment = .01):
        interrupted = False

        while seconds > 0 and not self.cancel_button.is_pressed():
            sleep(increment)
            seconds = seconds - increment

            if self.cancel_button.is_pressed():
                interrupted = True
                break

        return interrupted

class Hammer():
    DEFAULT = 0
    REST = 90
    PRESSED = 97

    def __init__(self, pin, wait):
        self._servo = servo.Servo(
            pulseio.PWMOut(pin, duty_cycle=2 ** 15, frequency=5)
        )
        self.wait = wait

    def _setAngle(self, angle):
        self._servo.angle = angle

    def default(self): self._setAngle(self.DEFAULT)
    def rest(self): self._setAngle(self.REST)
    def pressed(self): self._setAngle(self.PRESSED)

    def click(self):
        self.pressed()
        self.wait.sleep(CLICK_PRESS_DURATION)
        self.rest()

class Display():
    def get_time_per_item(self, sequence):
        return reduce(
            lambda a, b: a + b,
            map(
                lambda x: x.get("seconds"),
                sequence
            )
        )

    def get_time_per_item_at_step(self, sequence, step_index):
        return reduce(
            lambda a, b: a + b,
            map(
                lambda x: x[1].get("seconds") if (x[0] < step_index) else 0,
                enumerate(sequence)
            )
        )

    def get_item_percent_complete(
        self,
        step_index,
        sequence,
        by_time = True
    ):
        if (by_time):
            completed_time = self.get_time_per_item_at_step(sequence, step_index)
            return round(completed_time / self.get_time_per_item(sequence) * 100)
        else:
            return round(step_index / len(sequence) * 100)

    def get_sequence_percent_complete(
        self,
        item_index,
        step_index,
        sequence,
        count,
        by_time = True
    ):
        if (by_time):
            time_per_item = self.get_time_per_item(sequence)
            time_elapsed = (
                time_per_item * item_index
                + self.get_time_per_item_at_step(sequence, step_index)
            )
            time_total = time_per_item * count
            return round(time_elapsed / time_total * 100)
        else:
            return round(
                (item_index * len(sequence) + step_index)
                / (len(sequence) * count)
                * 100
            )

    def start_sequence(self):
        print()

    def start_item(self, item_index, count):
        print(
            "Making item {} of {}:".format(
                item_index + 1,
                count
            )
        )
        print()

    def start_step(self, step_index, item):
        print(
            "  {}: {} seconds to {}".format(
                step_index + 1,
                item.get("seconds"),
                item.get("description")
            )
        )

    def end_step(self, step_index, sequence, item_index, count):
        print(
            "  Item {}% complete. Sequence {}% complete.".format(
                self.get_item_percent_complete(step_index + 1, sequence),
                self.get_sequence_percent_complete(
                    item_index,
                    step_index + 1,
                    sequence,
                    count
                )
            )
        )
        print()

    def end_sequence(self, halt):
        if halt:
            print("Halted prematurely")
        else:
            print("All done!!")
        print()

    def choice(self, prompt, selection):
        print(prompt, selection)

display = Display()

class Menu():
    def __init__(self, pin_up, pin_down, confirm_button, cancel_button):
        self.encoder_previous_position = None
        self.encoder = rotaryio.IncrementalEncoder(pin_up, pin_down)
        self.confirm_button = confirm_button
        self.cancel_button = cancel_button

    def choice(self, prompt, options = [], is_cancelable = False):
        i = 0
        offset = self.encoder_previous_position or 0

        self.confirm_button.reset()
        self.cancel_button.reset()

        selection = options[0]

        display.choice(prompt, selection)

        while True:
            position = self.encoder.position

            if position != self.encoder_previous_position:
                i = (position - offset) % len(options)

                selection = options[i]
                self.encoder_previous_position = position

                display.choice(prompt, selection)

            if self.confirm_button.is_pressed():
                break

            if is_cancelable and self.cancel_button.is_pressed():
                return (None, 0)

        return (selection, i)

CLICK_PRESS_DURATION = .2

cancel_button = Button(board.A5)
confirm_button = Button(board.A4)

wait = Wait(cancel_button)
hammer = Hammer(board.A1, wait)
menu = Menu(board.A3, board.A2, confirm_button, cancel_button)

def run(sequence = [], count = 0):
    display.start_sequence()

    hammer.default()
    wait.sleep(1)

    hammer.rest()

    halt = False

    for item_index in range(0, count, 1):
        if halt: break

        display.start_item(item_index, count)

        for step_index, item in enumerate(sequence):
            display.start_step(step_index, item)

            halt = wait.interruptible_sleep(
                item.get("seconds") - CLICK_PRESS_DURATION
            )

            if halt: break

            hammer.click()

            display.end_step(step_index, sequence, item_index, count)

    display.end_sequence(halt)

    hammer.default()
    wait.sleep(1)

while True:
    hammer.default()

    count = None
    while count is None:
        (_, sequence_i) = menu.choice(
            "Choose sequence:",
            list(map(lambda seq: seq.get("text"), SEQUENCES))
        )
        (count, _) = menu.choice(
            "How many?",
            range(1, 101, 1),
            True
        )

    run(SEQUENCES[sequence_i].get("value"), count)
