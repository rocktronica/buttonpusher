include <mount.scad>;
include <servo.scad>;
include <horns.scad>;

module buttonpusher(
    width = 4,

    horn_width = 20,
    horn_length = SERVO_SHAFT_HEIGHT,
    horn_height = 10,
    horn_clearance = 1,

    beam_width = 150,
    beam_length = SERVO_SHAFT_HEIGHT,
    beam_height = 8,
    beam_clearance = 3,

    tolerance = .2,
    $fn = 12
) {
    FILAMENT_DIAMETER = 1.75;

    ZR_BUTTON_STILT = 8;

    BUTTON_X = 23;
    BUTTON_Y = 75;

    BASE_PLANK_LENGTH = 9.4;
    BASE_PLANK_HEIGHT = 6.4;

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

    module _base_plank(
        bleed = 0,
        _width = 100,
        _y = servo_mount_y + SERVO_HEIGHT / 2 - wall,
        _z = wall
    ) {
        translate([
            servo_mount_x - e,
            _y - bleed,
            _z - bleed
        ]) {
            cube([
                _width,
                BASE_PLANK_LENGTH + bleed * 2,
                BASE_PLANK_HEIGHT + bleed * 2
            ]);
        }
    }

    module _horn() {
        _x = servo_x;
        _y = servo_mount_y + wall + SERVO_HEIGHT + tolerance;
        _z = MOUNT_HEIGHT + horn_clearance;
        translate([_x, _y, _z]) oval_horn(
            horn_width,
            horn_length,
            horn_height,
            SERVO_SHAFT_DIAMETER + tolerance * 2
        );
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

            _base_plank(tolerance);

            servo_cavity();
        }
    }

    module beam(_wall = 2, extension = 5) {
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

        difference() {
            union() {
                translate([
                    -beam_width + width + MOUNT_DEPTH + BUTTON_X + extension,
                    _y,
                    _z
                ]) {
                    cube([beam_width, beam_length, beam_height]);
                }

                _c(_wall);
            }

            _c(tolerance, e);
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

        difference() {
            union() {
                fulcrum();
                cube([width, MOUNT_LENGTH, ZR_BUTTON_STILT + MOUNT_HEIGHT]);
                translate([width, 0, 0]) {
                    cube([MOUNT_DEPTH, MOUNT_LENGTH, ZR_BUTTON_STILT]);
                }
            }

            _base_plank(tolerance);
        }
    }

    # _servo();
    # _base_plank();

    _horn();
    beam();

    servo_mount();
    # base();
    translate([width, 0, ZR_BUTTON_STILT]) mount(3, fdm = true, tolerance = tolerance);
}

buttonpusher();
