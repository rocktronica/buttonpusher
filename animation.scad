function undulate(
    offset = 0,
    cycles = 1
) = (
    abs(
        (((
            ($t + offset) % 1
        ) % (1 / cycles)) * cycles)
        - 1 / 2
    ) * 2
);

function ease_in_out_quad(t) = (
    t < .5
        ? 2 * pow(t, 2)
        : -1 + (4 - 2 * t) * t
);
