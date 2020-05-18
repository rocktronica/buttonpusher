from time import monotonic, sleep

class Wait():
	def __init__(self, cancel_button):
		self.cancel_button = cancel_button

	def sleep(self, seconds):
		sleep(seconds)

	def interruptible_sleep(self, seconds, fn, increment = .25):
		start_time = monotonic()
		interrupted = False
		sleeping = True

		while sleeping:
			sleep(increment)

			if fn: fn()

			if self.cancel_button.is_pressed():
				interrupted = True
				break

			sleeping = (
				not interrupted
				and monotonic() - start_time < seconds
			)

		return interrupted
