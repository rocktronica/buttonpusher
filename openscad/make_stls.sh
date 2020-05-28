#!/bin/bash

{

openscad="/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"

dir="../3d-models"

mkdir -pv $dir

$openscad buttonpusher.scad -o "$dir/buttonpusher.stl" \
    -D 'SHOW_PERIPHERALS=false' \
    -D 'SHOW_HORN=false' \
    -D 'SHOW_BUTTONPUSHER=true'

$openscad buttonpusher.scad -o "$dir/horn.stl" \
    -D 'SHOW_PERIPHERALS=false' \
    -D 'SHOW_HORN=true' \
    -D 'SHOW_BUTTONPUSHER=false'

$openscad standoff.scad -o "$dir/standoff.stl"

}
