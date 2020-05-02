include <mount.scad>;
include <servo.scad>;

module buttonpusher(
    width = SERVO_WIDTH + 4 + 3,

    arm_length = 5,
    arm_diameter = 8,
    arm_clearance = 1,

    tolerance = .2
) {
    BUTTON_Y = 75;

    e = .005678;

    wall = 2;

    mount_width = SERVO_WIDTH + wall * 2;

    x = width - mount_width - (SERVO_FIN_WIDTH - wall);
    y = BUTTON_Y - SERVO_HEIGHT - arm_diameter / 2;

    servo_cavity_z = MOUNT_HEIGHT + arm_clearance
        + arm_diameter / 2;

    module _servo(bleed = 0) {
        translate([
            x + wall - (SERVO_SHAFT_X - SERVO_WIDTH),
            y + wall,
            servo_cavity_z
        ]) rotate([-90, 180, 0]) {
            servo(bleed);
        }
    }

    module servo_cavity() {
        _servo(tolerance);
    }

    module servo_mount() {
        difference() {
            translate([
                x,
                y,
                servo_cavity_z - SERVO_LENGTH / 2 - tolerance
            ]) {
                cube([
                    mount_width,
                    SERVO_HEIGHT + wall,
                    SERVO_LENGTH
                ]);
            }

            servo_cavity();
        }
    }

    /* # _servo(); */

    servo_mount();

    difference() {
        cube([width, MOUNT_LENGTH, MOUNT_HEIGHT]);
        servo_cavity();
    }

    translate([width, 0, 0]) mount(3, fdm = true, tolerance = tolerance);
}

buttonpusher();
