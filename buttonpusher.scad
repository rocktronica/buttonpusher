include <mount.scad>;
include <servo.scad>;

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

    module horn(
        button_diameter = 8,
        $fn = 18
    ) {
        module cavity(
            diameter,
            shim_count = 0,
            shim_width = 1,
            shim_length = .5,
            height = horn_length + e * 2
        ) {
            difference() {
                cylinder(
                    h = height,
                    d = diameter
                );

                if (shim_count > 0) {
                    for (i = [0 : shim_count - 1]) {
                        rotate([0, 0, i * 360 / shim_count]) {
                            translate([
                                shim_width / -2,
                                diameter / 2 - shim_length,
                                -e
                            ]) {
                                cube([shim_width, shim_length, height + e * 2]);
                            }
                        }
                    }
                }
            }
        }

        module armpit(height = 3) {
            x = horn_height;

            translate([x, -e, -e]) {
                cube([
                    horn_width - x - button_diameter,
                    horn_length + e * 2,
                    height + e
                ]);
            }
        }

        _x = servo_x - horn_height / 2;
        _y = y + wall + SERVO_HEIGHT + tolerance;
        _z = MOUNT_HEIGHT + horn_clearance;

        difference() {
            translate([_x, _y, _z]) cube([horn_width, horn_length, horn_height]);
            translate([_x, _y, _z]) armpit();
            servo_cavity(0, tolerance + e);
        }
    }

    /* # _servo(); */
    horn();

    servo_mount();

    difference() {
        cube([width, MOUNT_LENGTH, MOUNT_HEIGHT]);
        servo_cavity();
    }

    translate([width, 0, 0]) mount(3, fdm = true, tolerance = tolerance);
}

buttonpusher();
