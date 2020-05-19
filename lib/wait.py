from time import monotonic, sleep

class Wait():
	def __init__(self, confirm_button, cancel_button):
		self.confirm_button = confirm_button
		self.cancel_button = cancel_button

	def sleep(self, seconds):
		sleep(seconds)

	def idle(self):
		while True:
			if (self.confirm_button.is_pressed() or
					self.cancel_button.is_pressed()):
				break

	def interruptible_sleep(self, seconds, fn, increment = .25):
		start_time = monotonic()
		interrupted = False
		sleeping = True

		while sleeping:
			sleep(increment)

			if fn: fn()

			if self.cancel_button.is_pressed():
				interrupted = True
				self.cancel_button.reset()
				break

			sleeping = (
				not interrupted
				and monotonic() - start_time < seconds
			)

		return interrupted
