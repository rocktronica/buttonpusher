from adafruit_character_lcd import character_lcd
from digitalio import DigitalInOut
from time import monotonic
from utils import get_sequence_percent_complete

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
		self.lcd = character_lcd.Character_LCD_Mono(
			DigitalInOut(pin_lcd_rs),
			DigitalInOut(pin_lcd_en),
			DigitalInOut(pin_lcd_d4),
			DigitalInOut(pin_lcd_d5),
			DigitalInOut(pin_lcd_d6),
			DigitalInOut(pin_lcd_d7),
			lcd_columns,
			lcd_rows,
			DigitalInOut(pin_lcd_backlight)
		)
		self.lcd.backlight = True

		self.start_sequence([], 0)

	def print(self, line = "", clear = True):
		if clear: self.lcd.clear()
		self.lcd.message = line

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
			"I:{}/{} S:{}/{}\n{}% complete".format(
				self.item_index + 1,
				self.count,
				self.step_index + 1,
				len(self.sequence),
				get_sequence_percent_complete(
					self.sequence, self.count, self.seconds_elapsed
				),
			),
			clear = False
		)

	def choice(self, prompt, selection):
		self.print("{}:\n{}".format(prompt, selection))
