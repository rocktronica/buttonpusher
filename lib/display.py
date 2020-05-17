from functools import reduce

import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

class Display():
	def __init__(self):
		# Modify this if you have a different sized character LCD
		lcd_columns = 16
		lcd_rows = 4

		# Metro M0/M4 Pin Config:
		lcd_rs = digitalio.DigitalInOut(board.D7) # 4
		lcd_en = digitalio.DigitalInOut(board.D8) # 6?
		lcd_d7 = digitalio.DigitalInOut(board.D12) # 14
		lcd_d6 = digitalio.DigitalInOut(board.D11) # 13
		lcd_d5 = digitalio.DigitalInOut(board.D10) # 12
		lcd_d4 = digitalio.DigitalInOut(board.D9) # 11
		lcd_backlight = digitalio.DigitalInOut(board.D13) # 15

		# Initialise the LCD class
		lcd = characterlcd.Character_LCD_Mono(
			lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
		)
		lcd.backlight = True

		self.lcd = lcd

		self.start_sequence([], 0)

	def print(self, line = ""):
		print(line)
		self.lcd.clear()
		self.lcd.message = line

	def debug(self):
		while True:
			self.print("Hello world.")
			time.sleep(2)

			self.print("0123456789012345\n0123456789012345")
			time.sleep(2)

	def get_time_per_item(self, sequence):
		return reduce(
			lambda a, b: a + b,
			map(
				lambda x: x,
				sequence
			)
		)

	def get_time_per_item_at_step(self, sequence, step_index):
		return reduce(
			lambda a, b: a + b,
			map(
				lambda x: x[1] if (x[0] < step_index) else 0,
				enumerate(sequence)
			)
		)

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

	def start_sequence(self, sequence, count):
		self.sequence = sequence
		self.count = count
		self.item_index = 0
		self.step_index = 0

	def start_item(self, item_index):
		self.item_index = item_index
		self.update()

	def start_step(self, step_index):
		self.step_index = step_index
		self.update()

	def update(self):
		self.print(
			"I: {}/{}  S:{}/{}\n{}% complete".format(
				self.item_index + 1,
				self.count,
				self.step_index + 1,
				len(self.sequence),
				self.get_sequence_percent_complete(
					self.item_index,
					self.step_index,
					self.sequence,
					self.count
				)
			)
		)

	def end_sequence(self):
		self.print()

	def choice(self, prompt, selection):
		self.print("{}:\n{}".format(prompt, selection))
