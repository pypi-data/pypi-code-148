import math


def area_square(side):
    return side * side


def area_rectangle(length, breadth):
    return length * breadth


def area_triangle(base, height):
    return 0.5 * base * height


def area_circle(radius):
    return math.pi * radius * radius


def volume_cube(side):
    return side * side * side


def volume_cuboid(length, breadth, height):
    return length * breadth * height


def volume_cylinder(radius, height):
    return math.pi * radius * radius * height


def volume_cone(radius, height):
    return (1/3) * math.pi * radius * radius * height


def volume_sphere(radius):
    return (4/3) * math.pi * radius * radius * radius
