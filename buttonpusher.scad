include <mount.scad>;
include <servo.scad>;
include <horn.scad>;

module buttonpusher(
    width = SERVO_LENGTH + 4,

    horn_width = 43, // TODO: derive
    horn_length = SHAFT_SERVO_HEIGHT,
    horn_height = 8, // must be > SERVO_SHAFT_DIAMETER
    horn_clearance = 1,

    tolerance = .2
) {
    BUTTON_Y = 75;

    e = .005678;

    wall = 2;

    mount_width = SERVO_LENGTH + wall * 2;

    servo_cavity_z = MOUNT_HEIGHT + horn_clearance
        + horn_height / 2;

    x = width - mount_width;
    y = BUTTON_Y - SERVO_HEIGHT - horn_height / 2;
    z = servo_cavity_z - SERVO_LENGTH / 2 - tolerance;

    servo_x = x + wall - (SERVO_SHAFT_X - SERVO_LENGTH);

    module _servo(bleed = 0, shaft_bleed = 0) {
        translate([
            servo_x,
            y + wall,
            servo_cavity_z
        ]) rotate([-90, 90, 0]) {
            servo(bleed, shaft_bleed);
        }
    }

    module _horn() {
        _x = servo_x - horn_height / 2;
        _y = y + wall + SERVO_HEIGHT + tolerance;
        _z = MOUNT_HEIGHT + horn_clearance;
        translate([_x, _y, _z]) horn(
            width = horn_width,
            length = horn_length,
            height = horn_height,
            clearance = horn_clearance,
            cavity_diameter = SERVO_SHAFT_DIAMETER + tolerance * 2,
            wall = wall
        );
    }

    module servo_cavity(bleed = tolerance, shaft_bleed = 0) {
        _servo(bleed, shaft_bleed);
    }

    module servo_mount() {
        difference() {
            translate([x, y, z]) {
                cube([
                    mount_width,
                    SERVO_HEIGHT + wall,
                    SERVO_LENGTH
                ]);
            }

            servo_cavity();
        }
    }

    # _servo();
    _horn();

    servo_mount();

    difference() {
        cube([width, MOUNT_LENGTH, MOUNT_HEIGHT]);
        servo_cavity();
    }

    translate([width, 0, 0]) mount(3, fdm = true, tolerance = tolerance);
}

buttonpusher();
