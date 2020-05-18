from functools import reduce

import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

class Display():
	def __init__(
		self,
		pin_lcd_rs,
		pin_lcd_en,
		pin_lcd_d7,
		pin_lcd_d6,
		pin_lcd_d5,
		pin_lcd_d4,
		pin_lcd_backlight,
		lcd_columns = 16,
		lcd_rows = 4
	):
		self.lcd = characterlcd.Character_LCD_Mono(
			digitalio.DigitalInOut(pin_lcd_rs),
			digitalio.DigitalInOut(pin_lcd_en),
			digitalio.DigitalInOut(pin_lcd_d4),
			digitalio.DigitalInOut(pin_lcd_d5),
			digitalio.DigitalInOut(pin_lcd_d6),
			digitalio.DigitalInOut(pin_lcd_d7),
			lcd_columns,
			lcd_rows,
			digitalio.DigitalInOut(pin_lcd_backlight)
		)
		self.lcd.backlight = True

		self.start_sequence([], 0)

	def print(self, line = "", clear = True):
		if clear: self.lcd.clear()
		self.lcd.message = line

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
	):
		time_per_item = self.get_time_per_item(sequence)
		time_elapsed = (
			time_per_item * item_index
			+ self.get_time_per_item_at_step(sequence, step_index)
		)
		time_total = time_per_item * count
		return round(time_elapsed / time_total * 100)

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
			),
			clear = False
		)

	def choice(self, prompt, selection):
		self.print("{}:\n{}".format(prompt, selection))
