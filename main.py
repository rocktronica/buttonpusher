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

class Menu():
    def __init__(self, pin_up, pin_down, pin_button):
        self.encoder_previous_position = None

        self.encoder = rotaryio.IncrementalEncoder(pin_up, pin_down)

        self.button = digitalio.DigitalInOut(pin_button)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP

    def choice(self, prompt, options = []):
        i = 0
        offset = self.encoder_previous_position or 0
        button_pressed = False

        selection = options[0]

        print(prompt)

        # TODO: or if inheriting a encoder_previous_position?
        if offset > 0:
            print(selection)

        while True:
            position = self.encoder.position

            if position != self.encoder_previous_position:
                i = (position - offset) % len(options)

                selection = options[i]
                self.encoder_previous_position = position

                print(selection)

            if not self.button.value and not button_pressed:
                button_pressed = True
            if self.button.value and button_pressed:
                break
                button_pressed = False

        return (selection, i)

hammer = Hammer(board.A1)
menu = Menu(board.A3, board.A2, board.A4)

CLICK_PRESS_DURATION = .2

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

def get_time_per_item(sequence):
    return reduce(
        lambda a, b: a + b,
        map(
            lambda x: x.get("seconds"),
            sequence
        )
    )

def get_time_per_item_at_step(sequence, step_index):
    return reduce(
        lambda a, b: a + b,
        map(
            lambda x: x[1].get("seconds") if (x[0] < step_index) else 0,
            enumerate(sequence)
        )
    )

def get_item_percent_complete(
    step_index,
    sequence,
    by_time = True
):
    if (by_time):
        completed_time = get_time_per_item_at_step(sequence, step_index)
        return round(completed_time / get_time_per_item(sequence) * 100)
    else:
        return round(step_index / len(sequence) * 100)

def get_sequence_percent_complete(
    item_index,
    step_index,
    sequence,
    count,
    by_time = True
):
    if (by_time):
        time_per_item = get_time_per_item(sequence)
        time_elapsed = (
            time_per_item * item_index
            + get_time_per_item_at_step(sequence, step_index)
        )
        time_total = time_per_item * count
        return round(time_elapsed / time_total * 100)
    else:
        return round(
            (item_index * len(sequence) + step_index)
            / (len(sequence) * count)
            * 100
        )

def click():
    hammer.pressed()
    time.sleep(CLICK_PRESS_DURATION)
    hammer.rest()

def run(sequence = [], count = 0):
    print()

    hammer.default()
    time.sleep(1)

    hammer.rest()

    for item_index in range(0, count, 1):
        print(
            "Making item {} of {}:".format(
                item_index + 1,
                count
            )
        )
        print()

        for step_index, item in enumerate(sequence):
            print(
                "  {}: {} seconds to {}".format(
                    step_index + 1,
                    item.get("seconds"),
                    item.get("description")
                )
            )

            time.sleep(item.get("seconds") - CLICK_PRESS_DURATION)
            click()

            print(
                "  Item {}% complete. Sequence {}% complete.".format(
                    get_item_percent_complete(step_index + 1, sequence),
                    get_sequence_percent_complete(
                        item_index,
                        step_index + 1,
                        sequence,
                        count
                    )
                )
            )
            print()

    print("All done!!")

    hammer.default()
    time.sleep(1)

while True:
    hammer.setAngle(0)

    (_, sequence_i) = menu.choice("Choose sequence:", [
        "Redeem Nook Miles",
        "Craft item",
        "Wish on a star",
        "Debug"
    ])
    (count, _) = menu.choice("How many?", range(1, 101, 1))

    run([
        REDEEM_NOOK_MILES_SEQUENCE,
        CRAFT_SEQUENCE,
        WISH_ON_A_STAR_SEQUENCE,
        DEBUG_SEQUENCE
    ][sequence_i], count)

    print()
