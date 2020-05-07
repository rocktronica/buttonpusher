/*
Dimensions here assume orientation like on Adafruit product page,
https://www.adafruit.com/product/169: cables to the left, wide
side facing camera, shaft up
*/

SERVO_WIDTH = 22.7;
SERVO_LENGTH =12.5;
SERVO_HEIGHT = 26.9; // includes cylinder around motor on top

SERVO_FIN_WIDTH = 4.8;
SERVO_FIN_HEIGHT = 2.4;
SERVO_FIN_Z = 15.8;

SERVO_SHAFT_DIAMETER = 5;
SERVO_SHAFT_HEIGHT = 2.5;
SERVO_SHAFT_X = 6;

SERVO_CABLE_Z = 4.6;
SERVO_CABLE_HEIGHT = 2;

module servo(bleed = 0, shaft_bleed = 0) {
    width = SERVO_WIDTH + bleed * 2;
    length = SERVO_LENGTH + bleed * 2;
    height = SERVO_HEIGHT + bleed * 2;

    fin_width = SERVO_FIN_WIDTH + bleed;
    fin_height = SERVO_FIN_HEIGHT + bleed;
    fin_z = SERVO_FIN_Z + bleed / 2;

    cable_width = SERVO_FIN_WIDTH + bleed;
    cable_height = SERVO_CABLE_HEIGHT + bleed;
    cable_z = SERVO_CABLE_Z + bleed / 2;

    shaft_diameter = SERVO_SHAFT_DIAMETER + bleed;
    shaft_height = SERVO_SHAFT_HEIGHT + shaft_bleed;
    shaft_x = SERVO_SHAFT_X + bleed;

    module fins() {
        translate([-fin_width, 0, fin_z]) {
            cube([fin_width * 2 + width, length, fin_height]);
        }
    }

    module shaft() {
        translate([shaft_x, length / 2, height]) {
            cylinder(d = shaft_diameter, h = shaft_height);
        }
    }

    module cable() {
        translate([-SERVO_FIN_WIDTH, 0, cable_z]) {
            cube([
                cable_width,
                SERVO_LENGTH,
                cable_height
            ]);
        }
    }

    translate([
        -bleed - shaft_x,
        -bleed - length / 2,
        -bleed
    ]) {
        fins();
        shaft();
        cable();
        cube([width, length, height]);
    }
}
