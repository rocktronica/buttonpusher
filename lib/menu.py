import rotaryio

class Menu():
    def __init__(self, pin_up, pin_down, confirm_button, cancel_button):
        self.encoder_previous_position = None
        self.encoder = rotaryio.IncrementalEncoder(pin_up, pin_down)
        self.confirm_button = confirm_button
        self.cancel_button = cancel_button

    def choice(self, prompt, options = [], is_cancelable = False):
        i = 0
        offset = self.encoder_previous_position or 0

        self.confirm_button.reset()
        self.cancel_button.reset()

        selection = options[0]

        display.choice(prompt, selection)

        while True:
            position = self.encoder.position

            if position != self.encoder_previous_position:
                i = (position - offset) % len(options)

                selection = options[i]
                self.encoder_previous_position = position

                display.choice(prompt, selection)

            if self.confirm_button.is_pressed():
                break

            if is_cancelable and self.cancel_button.is_pressed():
                return (None, 0)

        return (selection, i)
