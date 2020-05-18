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

	def get_total_expected_time(self):
		return sum(self.sequence) * self.count

	def get_sequence_percent_complete(self):
		total_expected_time = self.get_total_expected_time()
		return round(self.seconds_elapsed / total_expected_time * 100)

	def start_sequence(self, sequence, count):
		self.sequence = sequence
		self.count = count
		self.item_index = 0
		self.step_index = 0
		self.seconds_elapsed = 0

	def start_item(self, item_index):
		self.item_index = item_index
		self.update()

	def start_step(self, step_index):
		self.step_index = step_index
		self.update()

	def set_seconds_elapsed(self, seconds_elapsed):
		self.seconds_elapsed = seconds_elapsed
		self.update()

	def update(self):
		self.print(
			"I:{}/{} S:{}/{}\n{}%".format(
				self.item_index + 1,
				self.count,
				self.step_index + 1,
				len(self.sequence),
				self.get_sequence_percent_complete()
			),
			clear = False
		)

	def choice(self, prompt, selection):
		self.print("{}:\n{}".format(prompt, selection))
