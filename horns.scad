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
