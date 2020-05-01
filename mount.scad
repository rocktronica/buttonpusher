MOUNT_LENGTH = 100.9;
MOUNT_HEIGHT = 14;

MIN_WALL = .6;

module mount(
    width,
    fdm = false,

    cavity_height_tolerance = 0,
    mount_depth_tolerance = 0,
    mount_lip_depth_tolerance = 0,
    mount_lip_beyond_wall_tolerance = 0,
    mount_stop_tolerance = 0
) {
    MOUNT_WALL = 2.1;
    MOUNT_DEPTH = 3 + mount_depth_tolerance;
    MOUNT_LIP_DEPTH = 1 - mount_lip_depth_tolerance;
    MOUNT_LIP_BEYOND_WALL = 3.4 - MOUNT_WALL - mount_lip_beyond_wall_tolerance;
    MOUNT_STOP = 10 - mount_stop_tolerance;

    e = .005678;

    cavity_length = MOUNT_LENGTH - MOUNT_STOP;
    cavity_height = MOUNT_HEIGHT - MOUNT_WALL * 2 + cavity_height_tolerance * 2;
    cavity_z = (cavity_height - MOUNT_HEIGHT) / -2;

    module cavity(overage = e) {
        translate([
            width - MOUNT_DEPTH,
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

    module lips_support(count = 4, length = MIN_WALL) {
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

tolerances = [0, .1, .2];

for (i = [0 : len(tolerances) - 1]) {
    translate([i * 10, 0, 0]) mount(
        5,
        fdm = true,
        cavity_height_tolerance = tolerances[i],
        mount_depth_tolerance = tolerances[i],
        mount_lip_depth_tolerance = tolerances[i],
        mount_lip_beyond_wall_tolerance = tolerances[i],
        mount_stop_tolerance = tolerances[i]
    );
}
