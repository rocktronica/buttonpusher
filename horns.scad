include <servo.scad>;

module stock_horn_cavity(
    bleed = 0,
    diameter = 7.3,
    height = 4.2,
    fin_count = 1,
    fin_length = 16.2,
    fin_width = 5.8,
    fin_height = 1.7,
    fin_end_diameter = 4.2,

    $fn = 24
) {
    module _c(diameter, height, distance = 0) {
        translate([0, distance > 0 ? distance + bleed : 0, 0]) {
            cylinder(
                d = diameter + bleed * 2,
                h = height + bleed
            );
        }
    }

    _c(diameter, height);
    for (i = [0 : fin_count]) {
        hull() {
            rotate([0, 0, (i / fin_count) * 360 - 90]) {
                _c(fin_width, fin_height);
                _c(
                    fin_end_diameter,
                    fin_height,
                    fin_length - fin_end_diameter / 2
                );
            }
        }
    }
}

module hammer_horn(
    angle = 0, // 12 o'clock, straight up
    distance = 33.5,
    extension = 2,
    tolerance = .1 // snap fit
) {
    HEIGHT = 4;
    TARGET_DIAMETER = 8;
    DIAMETER = 10;
    SCREW_HOLE_DIAMETER = 2;
    CLEARANCE = 1;

    SERVO_SHAFT_RECESS = SERVO_SHAFT_HEIGHT - CLEARANCE;

    $fn = 24;
    e = 0.012345;

    module _c(h = DIAMETER) {
        translate([distance, DIAMETER / 2, HEIGHT / 2]) {
            rotate([90, 0, 0]) {
                cylinder(
                    d = TARGET_DIAMETER,
                    h = h
                );
            }
        }
    }

    module _head(h = DIAMETER + extension) {
        render() {
            difference() {
                _c(h);

                translate([
                    distance - TARGET_DIAMETER / 2,
                    DIAMETER / -2 - extension,
                    HEIGHT
                ]) {
                    cube([
                        TARGET_DIAMETER,
                        h,
                        TARGET_DIAMETER
                    ]);
                }
            }
        }
    }

    translate([0, HEIGHT, 0]) {
        rotate([90, angle - 90, 0]) {
            difference() {
                union() {
                    cylinder(
                        d = DIAMETER,
                        h = HEIGHT
                    );

                    translate([0, DIAMETER / -2, 0]) {
                        cube([distance, DIAMETER, HEIGHT]);
                    }

                    _head();
                }

                translate([0, 0, -e]) {
                    cylinder(
                        d = SCREW_HOLE_DIAMETER + tolerance * 2,
                        h = HEIGHT + e * 2
                    );
                }

                translate([0, 0, -e]) {
                    stock_horn_cavity(tolerance);
                }
            }
        }
    }
}
