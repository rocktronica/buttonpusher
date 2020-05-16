from time import sleep

class Wait():
    def __init__(self, cancel_button):
        self.cancel_button = cancel_button

    def sleep(self, seconds):
        sleep(seconds)

    def interruptible_sleep(self, seconds, increment = .01):
        interrupted = False

        while seconds > 0 and not self.cancel_button.is_pressed():
            sleep(increment)
            seconds = seconds - increment

            if self.cancel_button.is_pressed():
                interrupted = True
                break

        return interrupted
