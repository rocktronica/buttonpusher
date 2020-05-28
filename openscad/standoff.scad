module glued_standoff(
    height = 10.8,
    diameter = 8,
    $fn = 24
) {
    cylinder(h = height, d = diameter);
}

glued_standoff();
