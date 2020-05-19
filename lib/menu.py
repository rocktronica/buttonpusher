from rotaryio import IncrementalEncoder

class Menu():
	def __init__(
		self,
		pin_up,
		pin_down,
		confirm_button,
		cancel_button,
		display
	):
		self.encoder_previous_position = None
		self.encoder = IncrementalEncoder(pin_up, pin_down)
		self.confirm_button = confirm_button
		self.cancel_button = cancel_button
		self.display = display

	def choice(
		self,
		prompt,
		options = [],
		is_cancelable = False,
		default_selected_index = 0
	):
		i = 0
		offset = self.encoder_previous_position or 0

		self.confirm_button.reset()
		self.cancel_button.reset()

		selection = options[default_selected_index]

		self.display.choice(prompt, selection)

		while True:
			position = self.encoder.position

			if position != self.encoder_previous_position:
				i = (position - offset) % len(options)

				selection = options[i]
				self.encoder_previous_position = position

				self.display.choice(prompt, selection)

			if self.confirm_button.is_pressed():
				break

			if is_cancelable and self.cancel_button.is_pressed():
				return (None, 0)

		return (selection, i)
