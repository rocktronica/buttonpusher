MOUNT_LENGTH = 100.9;
MOUNT_HEIGHT = 14;
MOUNT_DEPTH = 3;

MIN_WALL = .6;
MAX_BRIDGE = 10;

module mount(
    width = MOUNT_DEPTH,
    fdm = false,
    supports_count = undef,
    tolerance = 0
) {
    MOUNT_WALL = 2.1;
    MOUNT_DEPTH = MOUNT_DEPTH + tolerance;
    MOUNT_LIP_DEPTH = 1 - tolerance;
    MOUNT_LIP_BEYOND_WALL = 3 - MOUNT_WALL - tolerance;
    MOUNT_STOP = 10 - tolerance;

    supports_count = supports_count != undef
        ? supports_count
        : ceil((MOUNT_LENGTH - MOUNT_STOP) / MAX_BRIDGE);

    e = .005678;

    cavity_length = MOUNT_LENGTH - MOUNT_STOP;
    cavity_height = MOUNT_HEIGHT - MOUNT_WALL * 2 + tolerance * 2;
    cavity_z = (cavity_height - MOUNT_HEIGHT) / -2;

    module cavity(overage = e) {
        translate([
            width - MOUNT_DEPTH + e,
            MOUNT_STOP,
            cavity_z
        ]) {
            cube([
                MOUNT_DEPTH + overage,
                cavity_length + overage,
                cavity_height
            ]);
        }
    }

    module lips() {
        module lip() {
            cube([
                MOUNT_LIP_DEPTH + e,
                cavity_length + e,
                MOUNT_LIP_BEYOND_WALL
            ]);
        }

        for (z = [
            cavity_z - e,
            MOUNT_HEIGHT - cavity_z - MOUNT_LIP_BEYOND_WALL
        ]) {
            translate([
                width - MOUNT_LIP_DEPTH,
                MOUNT_STOP,
                z
            ]) {
                lip();
            }
        }
    }

    module lips_support(count = supports_count, length = MIN_WALL) {
        start = MOUNT_STOP - length;
        end = MOUNT_LENGTH - length;
        plot = (end - start) / (count);

        // Intentionally 0 indexed to skip overlap w/ MOUNT_STOP
        for (i = [1 : count]) {
            translate([width - MOUNT_LIP_DEPTH, start + i * plot, 0]) {
                cube([MOUNT_LIP_DEPTH, length, MOUNT_HEIGHT]);
            }
        }
    }

    difference() {
        cube([width, MOUNT_LENGTH, MOUNT_HEIGHT]);
        cavity();
    }

    lips();
    # if (fdm) lips_support();
}
