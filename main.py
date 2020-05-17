import board

from button import Button
from display import Display
from hammer import Hammer, CLICK_PRESS_DURATION
from menu import Menu
from sequences import SEQUENCES
from wait import Wait

cancel_button = Button(board.A3)
confirm_button = Button(board.A4)

display = Display()
wait = Wait(cancel_button)
hammer = Hammer(board.A2, wait)
menu = Menu(board.A5, board.A1, confirm_button, cancel_button, display)

def run(sequence = [], count = 0):
    display.start_sequence(sequence, count)

    hammer.default()
    wait.sleep(1)

    hammer.rest()

    halt = False

    for item_index in range(0, count, 1):
        if halt: break

        display.start_item(item_index)

        for step_index, seconds in enumerate(sequence):
            display.start_step(step_index)

            halt = wait.interruptible_sleep(seconds - CLICK_PRESS_DURATION)

            if halt: break

            hammer.click()

    display.end_sequence()

    hammer.default()
    wait.sleep(1)

while True:
    hammer.default()

    count = None
    while count is None:
        (_, sequence_i) = menu.choice(
            "Sequence",
            list(map(lambda seq: seq.get("text"), SEQUENCES))
        )
        (count, _) = menu.choice(
            "Count",
            range(1, 101, 1),
            True
        )

    run(SEQUENCES[sequence_i].get("value"), count)
