include <mount.scad>;
include <servo.scad>;
include <horns.scad>;

module buttonpusher(
    horn_width = 20,
    horn_length = SERVO_SHAFT_HEIGHT,
    horn_height = 10,
    horn_clearance = 1,
    wall = 2,

    VISUALIZE_PERIPHERALS = true,

    tolerance = .2,
    $fn = 12
) {
    width = SERVO_LENGTH + wall * 2 + tolerance * 2;

    ZR_BUTTON_STILT = 8;

    JOYCON_WIDTH = 33;
    JOYCON_LENGTH = 101;
    JOYCON_HEIGHT = 14;
    JOYCON_BUTTON_X = 23;
    JOYCON_BUTTON_Y = 75;
    JOYCON_BUTTON_DIAMETER = 8;
    JOYCON_BUTTON_HEIGHT = 2;

    e = .005678;

    servo_x = wall + SERVO_LENGTH / 2;
    servo_y = JOYCON_BUTTON_Y - SERVO_SHAFT_DIAMETER / 2 - SERVO_FULL_HEIGHT;
    servo_z = ZR_BUTTON_STILT + MOUNT_HEIGHT
        + JOYCON_BUTTON_HEIGHT + horn_clearance
        + horn_height / 2;

    horn_y = servo_y + SERVO_FULL_HEIGHT + tolerance;

    servo_tabs_y = servo_y - tolerance;

    module _servo(
        bleed = 0,
        show_fins = true,
        show_shaft = true,
        show_cable = true,
        show_base = true
    ) {
        translate([
            servo_x,
            servo_y,
            servo_z
        ]) rotate([-90, 90, 0]) {
            servo(
                bleed = bleed,
                show_fins = show_fins,
                show_shaft = show_shaft,
                show_cable = show_cable,
                show_base = show_base
            );
        }
    }

    module _horn() {
        translate([
            servo_x + tolerance,
            horn_y + tolerance,
            servo_z
        ]) {
            hammer_horn(
                distance = (width - servo_x) + MOUNT_DEPTH + JOYCON_BUTTON_X
                    - tolerance,
                extension = JOYCON_BUTTON_HEIGHT
            );
        }
    }

    module servo_tabs(
        _width = wall,
        _length = SERVO_FULL_HEIGHT + tolerance * 2,
        _support_width = wall * 3
    ) {
        _height = (servo_z + SERVO_SHAFT_X) + e;

        module _wall() {
            cube([_width, _length, _height]);

            translate([_width / 2, 0, _height + _width / 3]) {
                rotate([-90, 0, 0]) {
                    cylinder(
                        d = _width + tolerance * 4,
                        h = _length,
                        $fn = 24
                    );
                }
            }
        }

        module _side_supports() {
            for (_y = [
                servo_tabs_y,
                servo_tabs_y + SERVO_FULL_HEIGHT - _width
            ]) {
                translate([-_support_width, _y, 0]) {
                    cube([
                        _support_width + e,
                        _width,
                        _height
                    ]);
                }
            }
        }

        difference() {
            union() {
                for (_x = [0, width - _width]) {
                    translate([_x, servo_tabs_y, 0]) {
                        _wall();
                    }
                }

                _side_supports();
            }

            _servo(
                bleed = tolerance,
                show_fins = true,
                show_shaft = false,
                show_cable = false,
                show_base = false
            );
        }
    }

    module base() {
        difference() {
            union() {
                translate([0, servo_y - wall, 0]) {
                    cube([
                        width,
                        SERVO_FULL_HEIGHT + tolerance * 2 + wall * 2,
                        ZR_BUTTON_STILT + MOUNT_HEIGHT
                    ]);
                }

                translate([width - wall, 0, 0]) {
                    cube([wall, MOUNT_LENGTH, ZR_BUTTON_STILT + MOUNT_HEIGHT]);
                }

                translate([width, 0, 0]) {
                    cube([MOUNT_DEPTH, MOUNT_LENGTH, ZR_BUTTON_STILT]);
                }
            }

            _servo(bleed = tolerance);
        }

        translate([width + MOUNT_DEPTH, servo_tabs_y - e, 0]) {
            cube([
                JOYCON_WIDTH,
                SERVO_FULL_HEIGHT + tolerance * 2,
                ZR_BUTTON_STILT
            ]);
        }
    }

    _horn();

    servo_tabs();
    base();
    translate([width, 0, ZR_BUTTON_STILT]) mount(3, fdm = true, tolerance = tolerance);

    if (VISUALIZE_PERIPHERALS) {
        # translate([tolerance, 0, 0]) _servo();

        # translate([width + MOUNT_DEPTH, 0, ZR_BUTTON_STILT]) {
            cube([
                JOYCON_WIDTH,
                JOYCON_LENGTH,
                JOYCON_HEIGHT
            ]);

            translate([JOYCON_BUTTON_X, JOYCON_BUTTON_Y, JOYCON_HEIGHT]) {
                cylinder(
                    d = JOYCON_BUTTON_DIAMETER,
                    h = JOYCON_BUTTON_HEIGHT
                );
            }
        }
    }
}

buttonpusher(
    VISUALIZE_PERIPHERALS = false
);
