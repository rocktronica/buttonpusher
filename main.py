from button import Button
from display import Display
from hammer import Hammer
from menu import Menu
from sequences import SEQUENCES
from time import monotonic
from utils import get_seconds_to_wait
from wait import Wait
import board

cancel_button = Button(board.A3)
confirm_button = Button(board.A4)

display = Display(
	pin_lcd_rs = board.D7, # pin 4 on LCD
	pin_lcd_en = board.D8, # pin 6 on LCD
	pin_lcd_d7 = board.D12, # pin 14 on LCD
	pin_lcd_d6 = board.D11, # pin 13 on LCD
	pin_lcd_d5 = board.D10, # pin 12 on LCD
	pin_lcd_d4 = board.D9, # pin 11 on LCD
	pin_lcd_backlight = board.D13 # 15
)
wait = Wait(confirm_button, cancel_button)
hammer = Hammer(board.A2, wait)
menu = Menu(board.A1, board.A5, confirm_button, cancel_button, display)

def run(sequence = [], count = 0):
	hammer.rest()
	halt = False

	display.start_sequence(sequence, count)

	start_time = monotonic()
	def get_seconds_elapsed():
		return monotonic() - start_time

	def update_display():
		display.set_seconds_elapsed(get_seconds_elapsed())

	for item_index in range(0, count, 1):
		if halt: break

		display.start_item(item_index)

		for step_index, seconds in enumerate(sequence):
			display.start_step(step_index)

			halt = wait.interruptible_sleep(
				get_seconds_to_wait(
					item_index,
					step_index,
					sequence,
					get_seconds_elapsed()
				),
				update_display
			)
			if halt: break

			hammer.click()

	display.print("Stopped." if halt else "All done!")
	hammer.default()

	wait.idle(5)

sequence_i = 0
count_i = 0

COUNT_MAX = 120

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
			range(1, COUNT_MAX + 1, 1),
			is_cancelable = True,
			default_selected_index = count_i
		)

	run(SEQUENCES[sequence_i].get("value"), count)
