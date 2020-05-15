import time
import board
import pulseio
from adafruit_motor import servo
from functools import reduce
import rotaryio
import digitalio

class Hammer():
    DEFAULT = 0
    REST = 90
    PRESSED = 97

    def __init__(self, pin):
        self._servo = servo.Servo(
            pulseio.PWMOut(pin, duty_cycle=2 ** 15, frequency=5)
        )

    def setAngle(self, angle):
        self._servo.angle = angle

    def default(self): self.setAngle(self.DEFAULT)
    def rest(self): self.setAngle(self.REST)
    def pressed(self): self.setAngle(self.PRESSED)

    def click(self):
        self.pressed()
        time.sleep(CLICK_PRESS_DURATION)
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

    def end_sequence(self):
        print("All done!!")
        print()

    def choice(self, prompt, selection):
        print(prompt, selection)

display = Display()

class Menu():
    def __init__(self, pin_up, pin_down, pin_button):
        self.encoder_previous_position = None

        self.encoder = rotaryio.IncrementalEncoder(pin_up, pin_down)

        self.button = digitalio.DigitalInOut(pin_button)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.DOWN

    def choice(self, prompt, options = []):
        i = 0
        offset = self.encoder_previous_position or 0
        button_pressed = False

        selection = options[0]

        display.choice(prompt, selection)

        while True:
            position = self.encoder.position

            if position != self.encoder_previous_position:
                i = (position - offset) % len(options)

                selection = options[i]
                self.encoder_previous_position = position

                display.choice(prompt, selection)

            if not self.button.value and not button_pressed:
                button_pressed = True
            if self.button.value and button_pressed:
                break

        return (selection, i)

hammer = Hammer(board.A1)
menu = Menu(board.A3, board.A2, board.A4)

CLICK_PRESS_DURATION = .2

def run(sequence = [], count = 0):
    display.start_sequence()

    hammer.default()
    time.sleep(1)

    hammer.rest()

    for item_index in range(0, count, 1):
        display.start_item(item_index, count)

        for step_index, item in enumerate(sequence):
            display.start_step(step_index, item)

            time.sleep(item.get("seconds") - CLICK_PRESS_DURATION)
            hammer.click()

            display.end_step(step_index, sequence, item_index, count)

    display.end_sequence()

    hammer.default()
    time.sleep(1)

REDEEM_NOOK_MILES_SEQUENCE = [
    {
        "seconds": 2.5,
        "description": 'Wait for menu and select item',
    },
    {
        "seconds": 3,
        "description": 'Redeem ...?',
    },
    {
        "seconds": .75,
        "description": 'Confirm',
    },
    {
        "seconds": 8,
        "description": 'Wait for item and receive',
    },
    {
        "seconds": 2.5,
        "description": 'click through explanation',
    },
    {
        "seconds": 4.5,
        "description": 'put item away and make another selection',
    },
    {
        "seconds": .75,
        "description": 'confirm dialog',
    },
]
CRAFT_SEQUENCE = [
    {
        "seconds": 3,
        "description": 'Wait for menu and select item'
    },
    {
        "seconds": .75,
        "description": 'Craft it!'
    },
    {
        "seconds": .75,
        "description": 'Confirm'
    },
    {
        "seconds": 7,
        "description": 'Make item and receive it'
    },
    {
        "seconds": .75,
        "description": 'Keep crafting'
    },
]
WISH_ON_A_STAR_SEQUENCE = [
    {
        "seconds": 1.5,
        "description": 'Wish on a possible star'
    },
]
DEBUG_SEQUENCE = [
    {
        "seconds": 1,
        "description": 'Debug'
    },
]

SEQUENCES = [
    {"text": "Redeem Nook Miles", "value": REDEEM_NOOK_MILES_SEQUENCE},
    {"text": "Craft item", "value": CRAFT_SEQUENCE},
    {"text": "Wish on a star", "value": WISH_ON_A_STAR_SEQUENCE},
    {"text": "Debug", "value": DEBUG_SEQUENCE},
]

while True:
    hammer.setAngle(0)

    (_, sequence_i) = menu.choice(
        "Choose sequence:",
        list(map(lambda seq: seq.get("text"), SEQUENCES))
    )
    (count, _) = menu.choice("How many?", range(1, 101, 1))

    run(SEQUENCES[sequence_i].get("value"), count)
