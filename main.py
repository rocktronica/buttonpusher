import board

from time import monotonic
from button import Button
from display import Display
from hammer import Hammer, CLICK_PRESS_DURATION
from menu import Menu
from sequences import SEQUENCES
from wait import Wait

cancel_button = Button(board.A3)
confirm_button = Button(board.A4)

display = Display(
	pin_lcd_rs = board.D7,
	pin_lcd_en = board.D8,
	pin_lcd_d7 = board.D12,
	pin_lcd_d6 = board.D11,
	pin_lcd_d5 = board.D10,
	pin_lcd_d4 = board.D9,
	pin_lcd_backlight = board.D13
)
wait = Wait(cancel_button)
hammer = Hammer(board.A2, wait)
menu = Menu(board.A5, board.A1, confirm_button, cancel_button, display)

def run(sequence = [], count = 0):
	hammer.rest()
	halt = False
	start_time = monotonic()

	display.start_sequence(sequence, count)

	def update_display():
		display.set_seconds_elapsed(monotonic() - start_time)

	for item_index in range(0, count, 1):
		if halt: break

		display.start_item(item_index)

		for step_index, seconds in enumerate(sequence):
			display.start_step(step_index)

			halt = wait.interruptible_sleep(
				seconds - CLICK_PRESS_DURATION,
				update_display
			)
			if halt: break

			hammer.click()

	display.set_seconds_elapsed(monotonic() - start_time)
	wait.sleep(1)

sequence_i = 0
count_i = 0

while True:
	hammer.default()

	count = None
	while count is None:
		(_, sequence_i) = menu.choice(
			"Sequence",
			list(map(lambda seq: seq.get("text"), SEQUENCES)),
			default_selected_index = sequence_i
		)
		(count, count_i) = menu.choice(
			"Count",
			range(1, 101, 1),
			is_cancelable = True,
			default_selected_index = count_i
		)

	run(SEQUENCES[sequence_i].get("value"), count)
