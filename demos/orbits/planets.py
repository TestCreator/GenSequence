from math import sqrt
G = 6.67E-11

class Vector:
    """
    A Vector is a 3-tuple of (x,y,z) coordinates.
    """

    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
    def __repr__(self):
        return '({:.3g},{:.3g},{:.3g})'.format(self._x, self._y,self._z)
   
    def x(self):
        return self._x
    def y(self):
        return self._y
    def z(self):
        return self._z
    
    def norm(self):
        return sqrt(self._x**2 + self._y**2 + self._z**2)
    def clear(self):
        self._x, self._y, self._z = 0, 0, 0
        
    def __add__(self, other):
        a = self._x + other._x
        b = self._y + other._y
        c = self._z + other._z
        return Vector(a, b, c)
    def __sub__(self, other):
        f = self._x - other._x
        g = self._y - other._y
        h = self._z - other._z
        return Vector(f, g, h)
    def __mul__(self, other):
        return Vector(self._x*other, self._y*other, self._z*other)
    def __eq__(self, other):
        if self._x == other._x:
            if self._y == other._y:
                if self._z == other._z:
                    return True
        return False

class Body:
    """
    A Body object represents the state of a celestial body.  A body has mass 
    (a scalar), position (a vector), and velocity (a vector).  A third vector, 
    named force, is used when calculating forces acting on a body.  An
    optional name can be attached to use in debugging.
    """
    
    def __init__(self, mass = 0, position = Vector(0,0,0), velocity = Vector(0,0,0), name = None):
        """
        Create a new Body object with the specified mass (a scalar), position (a vector), 
        and velocity (another vector).  A fourth argument is an optional name for the body.
       """
        self._mass = mass
        self._position = position
        self._velocity = velocity
        self._name = name #how make optional?
        self._force = Vector(0, 0, 0)
    
    def mass(self):
        return self._mass
    def position(self):
        return self._position
    def velocity(self):
        return self._velocity
    def name(self):
        return self._name
    def force(self):
        return self._force

    def __repr__(self):
        #accounts for name != None
        if self._name != None:
            return '{}: {:.3g}kg {} {}'.format(self._name, self._mass, self._position, self._velocity)
        return '{:.3g}kg {} {}'.format(self._mass, self._position, self._velocity)
    
    def direction(self, other):
        return Vector(other._position._x - self._position._x, other._position._y - self._position._y, other._position._z - self._position._z)
    
    def add_force(self, other):
        d = self.direction(other).norm()
        f = (self.direction(other) * other._mass) * (1 / (d * d * d))
        self._force = self._force + f
    
    def clear_force(self):
        self._force.clear()
                
    def move(self, dt):
        a = self._force * G
        self._velocity = self._velocity + (a * dt)
        self._position = self._position + (self._velocity * dt)


def make_system(file):
    planet = open(file)
    
    #create list of lists
    info = []
    for line in planet:
        if line[0].isalnum():
            info.append(line.rstrip().split())
    
    #create list of class instances
    body_list = []
    for line in info:
        name = line[0]
        mass = float(line[1])
        position = Vector(float(line[2]), float(line[3]), float(line[4])) #SHOULD THESE BE FLOATS??
        velocity = Vector(float(line[5]), float(line[6]), float(line[7]))
        radius = line[8]
        color = line[9]
        body_list.append(Body(mass, position, velocity, name))
    
    return body_list

melon = Body(name='melon', mass=3.0, position=Vector(0,6371000,0))
earth = Body(name='earth', mass=5.9736E+24)
melon.add_force(earth)
melon.force()
print(melon.position())
melon.move(3000)
melon.position()
ss = make_system('solarsystem.txt')
print(ss)
