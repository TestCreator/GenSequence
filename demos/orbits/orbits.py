from planets import *
from copy import copy
from time import sleep
from Canvas import *


def step_system(bodies, dt=86459, nsteps=1):
    for i in range(nsteps):
        for planet in bodies:
            for ext in bodies:
                if planet != ext:
                    planet.add_force(ext)
                
        for planet in bodies:
            planet.move(dt)
            planet.clear_force()

def test():
    sys = make_system('solarsystem.txt')
    step_system(sys, nsteps = 2)

    ss = make_system('solarsystem.txt')
    mercury = copy(ss[1])
    step_system(ss, nsteps=1000, dt=7600.5216)

    assert abs(mercury.position().x() - ss[1].position().x()) < 1e10
    assert abs(mercury.position().y() - ss[1].position().y()) < 1e10
    assert abs(mercury.position().z() - ss[1].position().z()) < 1e10
    assert 4900000 < ss[0].position().norm() < 4900100

"""
#Name,mass,position_1,position_2,position_3,velocity_1,velocity_2,velocity_3,diameter,Color
body,2.9587159771767398e+26,-1755178546759.3, 210310194670.73, 580076141483.48,-6486.89, -2417.21, 6698.43,2.0000690802966985,#ffffbf
body,1.701583303983211e+26,-4549807980066.04, -2530791359836.99, 328790807142.88,-2887.5, -6300.17, 5268.5,4.503210783092609,#ffffbf
"""

def read_bodies(filename, cls):
    '''
    Read descriptions of planets, return a list of body objects.  The
    type of object to make is defined by cls, which must be Body or VBody.
    '''
    if cls not in [Body, VBody]:
        raise TypeError('cls must be Body or VBody')
        
    bodies = [ ]
    
    with open(filename) as bodyfile:
        for line in bodyfile:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':  
                continue
            name, m, rx, ry, rz, vx, vy, vz, diam, color = line.split(",")
            args = {
                'name': name,
                'mass' : float(m),
                'position' : Vector(float(rx), float(ry), float(rz)),
                'velocity' : Vector(float(vx), float(vy), float(vz)),
            }
            if cls == VBody:
                args.update({ 'color' : color, 'size' : float(diam) })
            bodies.append(cls(**args))

    return bodies


def view_system(lst, size=1000):
    Canvas.init(size, size, "Solar System")
    VBody.set_center(Vector(size//2, size//2, 0))
    VBody.set_scale((size/2) * (1 / max([b.position().norm() for b in lst])))
    for body in lst:
        body.draw()


class VBody(Body):
    def __init__(self, mass, position, velocity, name, size, color):
        Body.__init__(self, mass, position, velocity, name)
        self._size = size
        self._color = color
        self._graphic = None
    
    def size(self):
        return self._size
    def color(self):
        return self._color
    def graphic(self):
        return self._graphic
    
    scale = 0
    center = Vector(0, 0, 0)
    
    @staticmethod
    def set_scale(ratio):
        VBody.scale = ratio
        
    @staticmethod
    def set_center(vector):
        VBody.center = vector
    
    def draw(self):
        #loc=position×scale+center
        loc = (self._position * VBody.scale) + VBody.center
        self._graphic = Canvas.Circle(self._size, (loc._x, loc._y), fill=self._color)
        
        
    def move(self, dt):
        cur = self._position
        Body.move(self, dt)
        delta = (self._position - cur) * VBody.scale
        
        if self._graphic != None:
            self._graphic.move(delta._x, delta._y, track=True)



if __name__=="__main__":
    bodies = read_bodies('../../cases2/13-70-mass|right_slanted-position|right_slanted-velocity|uniform-diameter|left_slanted-.csv', VBody)
    view_system(bodies[:70])

    for i in range(665):
        step_system(bodies, nsteps = 1)
        Canvas.update()
        sleep(20)

    sleep(20)
