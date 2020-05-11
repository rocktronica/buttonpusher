import time
import board
import pulseio
from adafruit_motor import servo
from functools import reduce

pwm = pulseio.PWMOut(board.A1, duty_cycle=2 ** 15, frequency=5)
my_servo = servo.Servo(pwm)

CLICK_PRESS_DURATION = .2

DEFAULT = 0
REST = 90
PRESSED = REST + 8

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
        "seconds": .5,
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
        "seconds": .5,
        "description": 'confirm dialog',
    },
]

CRAFT_SEQUENCE = [
    {
        "seconds": 3,
        "description": 'Wait for menu and select item'
    },
    {
        "seconds": .5,
        "description": 'Craft it!'
    },
    {
        "seconds": .5,
        "description": 'Confirm'
    },
    {
        "seconds": 7,
        "description": 'Make item and receive it'
    },
    {
        "seconds": .5,
        "description": 'Keep crafting'
    },
]

WISH_ON_A_STAR_SEQUENCE = [
    {
        "seconds": 1.5,
        "description": 'Wish on a possible star'
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

def run(sequence = [], count = 0):
    setAngle(REST)

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

        print()

    print("All done!!")

def setAngle(angle):
    my_servo.angle = angle

def click():
    setAngle(PRESSED)
    time.sleep(CLICK_PRESS_DURATION)
    setAngle(REST)

def main():
    print()
    setAngle(DEFAULT)
    time.sleep(1)

    run(CRAFT_SEQUENCE, 10)

    setAngle(PRESSED)
    time.sleep(.1)

def debug():
    while True:
        setAngle(DEFAULT)
        time.sleep(1)
        setAngle(REST)
        time.sleep(1)
        setAngle(PRESSED)
        time.sleep(1)
        setAngle(REST)
        time.sleep(1)

debug()
