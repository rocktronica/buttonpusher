from functools import reduce
from math import floor


def get_expected_seconds_elapsed_per_item_at_step(step_index, sequence):
    return reduce(
        lambda a, b: a + b,
        map(lambda x: x[1] if (x[0] < step_index) else 0, enumerate(sequence)),
    )


def get_expected_seconds_elapsed(sequence, item_index, step_index):
    return sum(sequence) * item_index + get_expected_seconds_elapsed_per_item_at_step(
        step_index, sequence
    )


def get_seconds_to_wait(item_index, step_index, sequence, seconds_elapsed):
    is_end_of_item = step_index == len(sequence) - 1
    next_item_index = item_index + 1 if is_end_of_item else item_index
    next_step_index = 0 if is_end_of_item else step_index + 1
    expected_seconds_elapsed_at_next_step = get_expected_seconds_elapsed(
        sequence, next_item_index, next_step_index
    )

    return expected_seconds_elapsed_at_next_step - seconds_elapsed


def get_sequence_percent_complete(sequence, count, seconds_elapsed):
    total_expected_time = sum(sequence) * count
    return min(floor(seconds_elapsed / total_expected_time * 100), 100)
