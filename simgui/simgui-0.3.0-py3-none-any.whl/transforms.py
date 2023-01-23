from math import sin, cos, radians

class Trans2D:
  def __init__(self, dx, dy):
    self.dx=dx
    self.dy=dy
  def trans(self, pt):
    return (pt[0]-self.dx, pt[1]-self.dy)

class Scale2D:
  def __init__(self, fx, fy):
    self.fx=fx
    self.fy=fy
  def scale(self, pt):
    return (pt[0]*self.fx, pt[1]*self.fy)
  
class Map2D:
  def __init__(self, corner1, corner2, new_corner1, new_corner2):
    dx=corner1[0]-new_corner1[0]
    dy=corner1[1]-new_corner1[1]
    fx=(new_corner2[0]-new_corner1[0])/(corner2[0]-corner1[0])
    fy=(new_corner2[1]-new_corner1[1])/(corner2[1]-corner1[1])
    self.trans2d1=Trans2D(corner1[0], corner1[1])
    self.scale2d=Scale2D(fx, fy)
    self.trans2d2=Trans2D(-new_corner1[0], -new_corner1[1])
  def map(self, pt):
    return self.trans2d2.trans(self.scale2d.scale(self.trans2d1.trans(pt)))

class Project3D:
  def __init__(self, ez):
    self.ez=ez
  def proj(self, pt):
    x, y, z=pt
    return (x*self.ez/z, y*self.ez/z)

class Trans3D:
  def __init__(self, dx, dy, dz):
    self.dx=dx
    self.dy=dy
    self.dz=dz
  def trans(self, pt):
    return (pt[0]-self.dx, pt[1]-self.dy, pt[2]-self.dz)

class RoateX3D:
  def __init__(self, angle):
    self.rad=radians(angle)
  def rot(self, pt):
    x, y, z=pt
    cosA=cos(self.rad)
    sinA=sin(self.rad)
    return (x, y*cosA+z*sinA, z*cosA-y*sinA)

