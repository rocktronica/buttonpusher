from time import monotonic, sleep


class Wait:
    def __init__(self, confirm_button, cancel_button):
        self.confirm_button = confirm_button
        self.cancel_button = cancel_button

    # Intentionally obscuring over native sleep for a consistent interface.
    # ie, it's only ever called via Wait, making it easier to debug, if needed
    # pylint: disable=R0201
    def sleep(self, seconds):
        sleep(seconds)

    def _interruptible_sleep(self, seconds, fn=None, buttons=None, increment=0.1):
        buttons = buttons or []

        start_time = monotonic()
        interrupted = False
        sleeping = True

        while sleeping:
            sleep(increment)

            if fn:
                fn()

            for button in buttons:
                if button.is_pressed():
                    interrupted = True
                    button.reset()
                    break

            sleeping = not interrupted and monotonic() - start_time < seconds

        return interrupted

    def interruptible_sleep(self, seconds, fn):
        return self._interruptible_sleep(seconds, fn=fn, buttons=[self.cancel_button])

    def idle(self, seconds):
        return self._interruptible_sleep(
            seconds, buttons=[self.confirm_button, self.cancel_button]
        )
