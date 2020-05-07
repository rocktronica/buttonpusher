include <servo.scad>;

module cavity(
    diameter,
    length,
    shim_count = 3,
    shim_width = 1,
    shim_length = .5,
) {
    e = .005678;
    _height = length + e * 2;

    difference() {
        cylinder(
            h = _height,
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
                        cube([shim_width, shim_length, _height + e * 2]);
                    }
                }
            }
        }
    }
}

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
        translate([0, distance, 0]) {
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
                _c(fin_end_diameter, fin_height, fin_length);
            }
        }
    }
}

module arm_horn(
    width,
    length,
    height,
    clearance,
    cavity_diameter,
    wall,
    button_diameter = 8,
    $fn = 18
) {
    e = .005678;

    module armpit(_height = 3) {
        x = height;

        translate([x, -e, -e]) {
            cube([
                width - x - button_diameter,
                length + e * 2,
                _height + e
            ]);
        }
    }

    difference() {
        cube([width, length, height]);
        armpit();
        translate([height / 2, -e, height / 2])
            rotate([-90, 0, 0]) cavity(cavity_diameter, length);
    }
}

module svg_horn(height = 0, bleed = 0) {
    linear_extrude(height) {
        offset(bleed) {
            import(
                file = "horn_scan_2.svg",
                center = true,
                dpi = 300
            );
        }
    }
}

module oval_horn(
    width,
    length,
    height,
    cavity_diameter
) {
    e = .005678;

    module oval_cylinder($fn = 24) {
        scale([width / height, 1, 1]) {
            rotate([-90, 0, 0]) {
                translate([height / 2, height / -2, 0]) {
                    cylinder(d = height, h = length);
                }
            }
        }
    }

    difference() {
        translate([width / -2, 0, 0]) {
            oval_cylinder();
        }

        translate([0, -e, height / 2]) {
            rotate([-90, 0, 0]) cavity(cavity_diameter, length);
        }
    }
}

module screw_horn(
    tolerance = .2,
    cap = 0
) {
    HEIGHT = 4;
    TARGET_DIAMETER = 8;
    DISTANCE = 33.5;
    DIAMETER = 10;
    SCREW_HOLE_DIAMETER = 2;
    EXTENSION = 2;
    CLEARANCE = 1;

    SERVO_SHAFT_RECESS = SERVO_SHAFT_HEIGHT - CLEARANCE;

    $fn = 24;
    e = 0.012345;

    module _c(h = DIAMETER) {
        translate([DISTANCE, DIAMETER / 2, HEIGHT / 2])
        rotate([90, 0, 0])
        cylinder(
            d = TARGET_DIAMETER,
            h = h
        );
    }

    translate([0, HEIGHT, 0])
    rotate([90, 0, 0])
    difference() {
        union() {
            cylinder(
                d = DIAMETER,
                h = HEIGHT
            );

            translate([0, DIAMETER / -2, 0]) {
                cube([DISTANCE, DIAMETER, HEIGHT]);
            }

            _c();
            _c(DIAMETER + EXTENSION);

            if (cap > 0) {
                translate([0, 0, HEIGHT]) {
                    cylinder(
                        d = DIAMETER,
                        h = cap
                    );
                }
            }
        }

        translate([0, 0, -e])
        cylinder(
            d = SCREW_HOLE_DIAMETER + tolerance * 2,
            h = HEIGHT + cap + e * 2
        );

        translate([0, 0, -e])
        stock_horn_cavity(tolerance);
    }
}
