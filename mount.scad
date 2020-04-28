MOUNT_WALL = 2.1;
MOUNT_DEPTH = 3;
MOUNT_LIP_DEPTH = 1; // TODO: use it or lose it
MOUNT_LIP_BEYOND_WALL = 3.4 - MOUNT_WALL;
MOUNT_STOP = 14.5;

MOUNT_WIDTH = MOUNT_DEPTH + 2;
MOUNT_LENGTH = 100.9;
MOUNT_HEIGHT = 14;

BUTTON_X = 23;
BUTTON_Y = 76;
BUTTON_DIAMETER = 7.4;

e = .005678;

module rail() {
    cube([RAIL_WIDTH, RAIL_LENGTH, RAIL_HEIGHT]);

    translate([
        RAIL_WIDTH - e,
        RAIL_STANDOFF_Y,
        RAIL_STANDOFF_DEPTH
    ]) {
        cube([
            RAIL_STANDOFF_WIDTH + e,
            RAIL_STANDOFF_LENGTH,
            RAIL_STANDOFF_HEIGHT
        ]);
    }
}

module mount() {
    cavity_length = MOUNT_LENGTH - MOUNT_STOP;
    cavity_height = MOUNT_HEIGHT - MOUNT_WALL * 2;
    cavity_z = (cavity_height - MOUNT_HEIGHT) / -2;

    module cavity(overage = e) {
        translate([
            MOUNT_WIDTH - MOUNT_DEPTH,
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
                MOUNT_WIDTH - MOUNT_LIP_DEPTH,
                MOUNT_STOP,
                z
            ]) {
                # lip();
            }
        }
    }

    difference() {
        cube([MOUNT_WIDTH, MOUNT_LENGTH, MOUNT_HEIGHT]);
        cavity();
    }

    lips();
}

mount();

/* # rail(); */
