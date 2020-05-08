include <mount.scad>;
include <servo.scad>;
include <horns.scad>;

module buttonpusher(
    horn_width = 20,
    horn_length = SERVO_SHAFT_HEIGHT,
    horn_height = 10,
    horn_clearance = 1,
    wall = 2,

    VISUALIZE_JOYCON = true,

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
    servo_y = JOYCON_BUTTON_Y - SERVO_SHAFT_DIAMETER / 2 - SERVO_HEIGHT;
    servo_z = ZR_BUTTON_STILT + MOUNT_HEIGHT
        + JOYCON_BUTTON_HEIGHT + horn_clearance
        + horn_height / 2;

    horn_y = servo_y + SERVO_HEIGHT + tolerance;

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

    module servo_tab(
        _width = wall,
        _length = SERVO_HEIGHT + tolerance * 2
    ) {
        _y = servo_y - tolerance;
        _z = ZR_BUTTON_STILT + MOUNT_HEIGHT - e;
        _height = (servo_z + SERVO_SHAFT_X) - _z + e;

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

        difference() {
            union() {
                for (_x = [0, width - _width]) {
                    translate([_x, _y, _z]) {
                        _wall();
                    }
                }
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
                cube([width, MOUNT_LENGTH, ZR_BUTTON_STILT + MOUNT_HEIGHT]);
                translate([width, 0, 0]) {
                    cube([MOUNT_DEPTH, MOUNT_LENGTH, ZR_BUTTON_STILT]);
                }
            }

            _servo(bleed = tolerance);
        }
    }

    # translate([tolerance, 0, 0]) _servo();

    _horn();

    servo_tab();
    base();
    translate([width, 0, ZR_BUTTON_STILT]) mount(3, fdm = true, tolerance = tolerance);

    if (VISUALIZE_JOYCON) {
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

buttonpusher();
