import board
import rotaryio

from button import Button
from sequences import SEQUENCES
from wait import Wait
from hammer import Hammer, CLICK_PRESS_DURATION
from display import Display

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
