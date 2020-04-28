MOUNT_LENGTH = 100.9;
MOUNT_HEIGHT = 14;

module mount(width) {
    MOUNT_WALL = 2.1;
    MOUNT_DEPTH = 3;
    MOUNT_LIP_DEPTH = 1;
    MOUNT_LIP_BEYOND_WALL = 3.4 - MOUNT_WALL;
    MOUNT_STOP = 14.5;

    e = .005678;

    cavity_length = MOUNT_LENGTH - MOUNT_STOP;
    cavity_height = MOUNT_HEIGHT - MOUNT_WALL * 2;
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
                # lip();
            }
        }
    }

    difference() {
        cube([width, MOUNT_LENGTH, MOUNT_HEIGHT]);
        cavity();
    }

    lips();
}

mount(5);
