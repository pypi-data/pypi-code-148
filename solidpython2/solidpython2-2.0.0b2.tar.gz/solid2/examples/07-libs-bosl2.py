#! /usr/bin/env python

from solid2.extensions.bosl2 import *

#basic stuff
def bolt():
    return metric_screws.metric_bolt(size=20, headtype='hex', l=40)

def bounding_box_wrapper(obj):
    return ~bounding_box()(obj)

def extrude_along_path():
    path = [ [0, 0, 0], [33, 33, 33], [66, 33, 40], [100, 0, 0], [150,0,0] ]
    return path_extrude(path)(circle(r=10, _fn=6))

def heightfield_test():
    def get_data():
        from math import sqrt,sin
        data = []
        for y in range(50):
            yrow = []
            data.append(yrow)
            for x in range(50):
                yrow.append(sin(sqrt((y-25)**2+(x-25)**2)))

        return data

    return heightfield(size=[100,100], bottom=-1, data=get_data())

#a little bit more complicated stuff
def bosl_diff():
    #openscad example from bosl2 wiki:
    #diff()
    #    cuboid(50) {
    #        tag("remove") attach(TOP) sphere(d=40);
    #        tag("keep") attach(CTR) cylinder(h=40, d=10);
    #    }
    return \
    diff() (
        cuboid(50) (
            tag("remove") (attach(TOP) (sphere(d=40))),
            tag("keep") (attach(CTR) (cylinder(h=40, d=10)))
        )
    )

def bosl_diff2():
    #openscad example from bosl2 wiki:
    #diff()
    #    cuboid(50) {
    #        tag("remove") attach(TOP) sphere(d=40);
    #        tag("keep") attach(CTR) cylinder(h=40, d=10);
    #    }
    return \
    diff() (
        cuboid(50) (
            sphere(d=40).attach(TOP).tag("remove"),
            cylinder(h=40, d=10).attach(CTR).tag("keep")
        )
    )

assembly = bounding_box_wrapper(extrude_along_path()) +\
           extrude_along_path().color("purple") +\
           bosl_diff2().back(100) +\
           bolt().left(100) +\
           heightfield_test().fwd(100)

assembly.save_as_scad()

