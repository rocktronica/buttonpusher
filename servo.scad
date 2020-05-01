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
SHAFT_SERVO_HEIGHT = 3;
SERVO_SHAFT_X = 6;

SERVO_CABLE_Y = 4.6;
SERVO_CABLE_HEIGHT = 2;

module servo(bleed = 0) {
    width = 22.7 + bleed * 2;
    length =12.5 + bleed * 2;
    height = 26.9 + bleed * 2;

    fin_width = 4.8 + bleed;
    fin_height = 2.4 + bleed;
    fin_z = 15.8 + bleed / 2;

    shaft_diameter = 5 + bleed;
    shaft_height = 3 + bleed;
    shaft_x = 6 + bleed;

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

    translate([
        -bleed - shaft_x,
        -bleed - length / 2,
        -bleed
    ]) {
        fins();
        shaft();
        cube([width, length, height]);
    }
}

servo();
