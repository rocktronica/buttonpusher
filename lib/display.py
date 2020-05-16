from functools import reduce

class Display():
    def get_time_per_item(self, sequence):
        return reduce(
            lambda a, b: a + b,
            map(
                lambda x: x.get("seconds"),
                sequence
            )
        )

    def get_time_per_item_at_step(self, sequence, step_index):
        return reduce(
            lambda a, b: a + b,
            map(
                lambda x: x[1].get("seconds") if (x[0] < step_index) else 0,
                enumerate(sequence)
            )
        )

    def get_item_percent_complete(
        self,
        step_index,
        sequence,
        by_time = True
    ):
        if (by_time):
            completed_time = self.get_time_per_item_at_step(sequence, step_index)
            return round(completed_time / self.get_time_per_item(sequence) * 100)
        else:
            return round(step_index / len(sequence) * 100)

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

    def start_sequence(self):
        print()

    def start_item(self, item_index, count):
        print(
            "Making item {} of {}:".format(
                item_index + 1,
                count
            )
        )
        print()

    def start_step(self, step_index, item):
        print(
            "  {}: {} seconds to {}".format(
                step_index + 1,
                item.get("seconds"),
                item.get("description")
            )
        )

    def end_step(self, step_index, sequence, item_index, count):
        print(
            "  Item {}% complete. Sequence {}% complete.".format(
                self.get_item_percent_complete(step_index + 1, sequence),
                self.get_sequence_percent_complete(
                    item_index,
                    step_index + 1,
                    sequence,
                    count
                )
            )
        )
        print()

    def end_sequence(self, halt):
        if halt:
            print("Halted prematurely")
        else:
            print("All done!!")
        print()

    def choice(self, prompt, selection):
        print(prompt, selection)
