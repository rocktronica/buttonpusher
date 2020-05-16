import board

from button import Button
from sequences import SEQUENCES
from wait import Wait
from hammer import Hammer, CLICK_PRESS_DURATION
from display import Display
from menu import Menu

display = Display()

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
