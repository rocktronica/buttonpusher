include <mount.scad>;
include <servo.scad>;
include <horn.scad>;

module buttonpusher(
    width = 4,

    horn_width = 43, // TODO: derive
    horn_length = SERVO_SHAFT_HEIGHT,
    horn_height = 8, // must be > SERVO_SHAFT_DIAMETER
    horn_clearance = 1,

    beam_width = 200,
    beam_length = SERVO_SHAFT_HEIGHT,
    beam_height = 2,
    beam_clearance = 3,

    tolerance = .2,
    $fn = 12
) {
    FILAMENT_DIAMETER = 1.75;

    ZR_BUTTON_STILT = 8;

    BUTTON_X = 23;
    BUTTON_Y = 75;

    e = .005678;

    wall = 2;

    mount_width = SERVO_WIDTH + wall * 2;

    servo_cavity_z = SERVO_LENGTH / 2 + wall;

    servo_mount_x = -50; // aribtrary for now
    servo_mount_y = BUTTON_Y - beam_length / 2 - SERVO_HEIGHT - SERVO_SHAFT_HEIGHT;

    servo_x = servo_mount_x + wall - (SERVO_SHAFT_X - SERVO_WIDTH);

    module _servo(bleed = 0, shaft_bleed = 0) {
        translate([
            servo_x,
            servo_mount_y + wall,
            ZR_BUTTON_STILT + servo_cavity_z
        ]) rotate([-90, 180, 0]) {
            servo(bleed, shaft_bleed);
        }
    }

    module servo_cavity(bleed = tolerance, shaft_bleed = 0) {
        _servo(bleed, shaft_bleed);
    }

    module servo_mount() {
        difference() {
            translate([servo_mount_x, servo_mount_y, 0]) {
                cube([
                    mount_width,
                    SERVO_HEIGHT + wall,
                    ZR_BUTTON_STILT + SERVO_LENGTH
                ]);
            }

            servo_cavity();
        }
    }

    module beam(_wall = 1) {
        _y = BUTTON_Y - beam_length / 2;
        _z = ZR_BUTTON_STILT + MOUNT_HEIGHT + beam_clearance;

        module _c(bleed = 0, bleed_y = 0) {
            translate([width / 2, _y - bleed_y, _z])
            rotate([-90, 0, 0])
            cylinder(
                d = FILAMENT_DIAMETER + bleed * 2,
                h = beam_length + bleed_y * 2
            );
        }

        module _u_beam() {
            difference() {
                # cube([beam_width, beam_length, beam_height]);

                translate([-e, _wall, -e]) {
                    cube([
                        beam_width + e * 2,
                        beam_length - _wall * 2,
                        beam_height - _wall
                    ]);
                }
            }
        }

        difference() {
            union() {
                translate([-beam_width + width + MOUNT_DEPTH + BUTTON_X, _y, _z]) {
                    _u_beam();
                }

                _c(_wall);
            }

            _c(0, e);
        }
    }

    module base() {
        module fulcrum(
            clearance = beam_clearance,
            _wall = 3
        ) {
            _width = width;
            _length = beam_length + _wall * 2 + tolerance * 2;
            _height = beam_height + clearance;

            _y = BUTTON_Y - _length / 2 - tolerance;

            translate([0, _y, ZR_BUTTON_STILT + MOUNT_HEIGHT]) {
                difference() {
                    cube([_width, _length, _height]);

                    translate([-e, _wall + tolerance, -e]) {
                        cube([
                            _width + e * 2,
                            beam_length + tolerance * 2,
                            _height + e * 2
                        ]);
                    }

                    translate([_width / 2, -e, _height - _width / 2]) {
                        rotate([-90, 0, 0]) {
                            cylinder(
                                d = FILAMENT_DIAMETER + tolerance * 2,
                                h = _length + e * 2
                            );
                        }
                    }
                }
            }
        }

        fulcrum();
        cube([width, MOUNT_LENGTH, ZR_BUTTON_STILT + MOUNT_HEIGHT]);
        translate([width, 0, 0]) {
            cube([MOUNT_DEPTH, MOUNT_LENGTH, ZR_BUTTON_STILT]);
        }
    }

    # _servo();
    servo_mount();
    beam();

    base();

    translate([width, 0, ZR_BUTTON_STILT]) mount(3, fdm = true, tolerance = tolerance);
}

buttonpusher();
