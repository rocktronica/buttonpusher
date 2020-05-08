include <mount.scad>;
include <servo.scad>;
include <horns.scad>;

module buttonpusher(
    width = SERVO_LENGTH + 4,

    horn_width = 20,
    horn_length = SERVO_SHAFT_HEIGHT,
    horn_height = 10,
    horn_clearance = 1,

    VISUALIZE_JOYCON = true,

    tolerance = .2,
    $fn = 12
) {
    ZR_BUTTON_STILT = 8;

    JOYCON_WIDTH = 33;
    JOYCON_LENGTH = 101;
    JOYCON_HEIGHT = 14;
    BUTTON_X = 23;
    BUTTON_Y = 75;
    BUTTON_HEIGHT = 2;

    e = .005678;

    wall = 2;

    mount_width = SERVO_LENGTH + wall * 2;

    servo_cavity_z = ZR_BUTTON_STILT + MOUNT_HEIGHT + horn_clearance
        + horn_height / 2;

    servo_mount_x = width - mount_width;
    servo_mount_y = BUTTON_Y - SERVO_HEIGHT - horn_height / 2;
    servo_mount_z = servo_cavity_z - SERVO_LENGTH / 2 - tolerance;

    servo_x = servo_mount_x + wall - (SERVO_SHAFT_X - SERVO_LENGTH);

    module _servo(bleed = 0, shaft_bleed = 0) {
        translate([
            servo_x,
            servo_mount_y + wall,
            servo_cavity_z
        ]) rotate([-90, 90, 0]) {
            servo(bleed, shaft_bleed);
        }
    }

    module _horn() {
        translate([
            servo_x,
            servo_mount_y + wall + SERVO_HEIGHT + tolerance,
            servo_cavity_z
        ]) {
            hammer_horn();
        }
    }

    module servo_cavity(bleed = tolerance, shaft_bleed = 0) {
        _servo(bleed, shaft_bleed);
    }

    module servo_mount() {
        difference() {
            translate([servo_mount_x, servo_mount_y, servo_mount_z]) {
                cube([
                    mount_width,
                    SERVO_HEIGHT + wall,
                    SERVO_LENGTH
                ]);
            }

            servo_cavity();
        }
    }

    module base() {
        difference() {
            union() {
                cube([width, MOUNT_LENGTH, ZR_BUTTON_STILT + MOUNT_HEIGHT]);
                translate([width, 0, 0]) {
                    cube([MOUNT_DEPTH, MOUNT_LENGTH, ZR_BUTTON_STILT]);
                }
            }

            servo_cavity();
        }
    }

    # _servo();

    _horn();

    servo_mount();
    base();
    translate([width, 0, ZR_BUTTON_STILT]) mount(3, fdm = true, tolerance = tolerance);

    if (VISUALIZE_JOYCON) {
        # translate([width + MOUNT_DEPTH, 0, ZR_BUTTON_STILT]) {
            cube([
                JOYCON_WIDTH,
                JOYCON_LENGTH,
                JOYCON_HEIGHT
            ]);

            translate([BUTTON_X, BUTTON_Y, JOYCON_HEIGHT]) {
                cylinder(
                    d = 8,
                    h = BUTTON_HEIGHT
                );
            }
        }
    }
}

buttonpusher();
