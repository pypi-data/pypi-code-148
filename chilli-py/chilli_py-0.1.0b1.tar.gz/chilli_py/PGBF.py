import numpy as np 
from chilli_py.alias import dist2 
from chilli_py.overlap import overlap, overlap_pgbf 

class PGBF: 
    """
        PGBF class 
        Primitive Gaussian basis function (PGBF)
        Class to construct PGBFs. 

        primitive_gto = NORM * x**k * y**l * z**m * exp (-expn *r(x,y,z)**2) 

        Input
            - center: array()/list(), center of Gaussian center= [x,y,z]
            - power: array()/list(), power of [x,y,z], [k,l,m]
            - expn: float(), exponent may called alpha
            - NORM: float(), norm of the PGBF 
    """
    def __init__(self,center,power,expn,NORM=None): 
        """
            __init__
            Initialize instance of the class. 
        """
        self.center = np.array(center)
        self.power = np.array(power)
        self.expn = expn 
        if NORM is None: 
            self.normalize()
        if NORM is not None:
            self.NORM = NORM 

    def normalize(self):
        """
            normalize 
            Calculate norm for a primitive Gaussian. 
        """
        O = overlap(self,self)
        NORM = 1.0 / np.sqrt(O)
        self.NORM = NORM
        return NORM

    def eval(self,coord): 
        """
            eval 
            Evaluate Gaussian at 3d coordinate, i.e., coord (x,y,z)
        """
        x,y,z = coord 
        xo = self.center[0]
        yo = self.center[1]
        zo = self.center[2]
        I = self.power[0]
        J = self.power[1]
        K = self.power[2]
        expn = self.expn
        NORM = self.NORM

        dx, dy, dz = x-xo, y-yo, z-zo
        r2 = dist2(self.center - coord)
        return NORM*(dx**I)*(dy**J)*(dz**K)*np.exp(-expn*r2)

    def grad(self,coord):
        """
           grad
           Evaluate gradient of a Gaussian at 3d coordinate, i.e., coord (x,y,z)
	"""
        x,y,z = coord
        expn = self.expn
        I,J,K = self.power
        C = self.NORM
        xo,yo,zo = self.center
        dx, dy, dz = x-xo, y-yo, z-zo
        fx = ((dx)**I)*np.exp(-expn*(dx**2))
        fy = ((dy)**J)*np.exp(-expn*(dy**2))
        fz = ((dz)**K)*np.exp(-expn*(dz**2))
        gx = -2*expn*dx*fx
        gy = -2*expn*dy*fy
        gz = -2*expn*dz*fz
        if I > 0: 
            gx += dx**(I-1)*np.exp(-expn*(dx**2))
        if J > 0: 
            gy += dy**(J-1)*np.exp(-expn*(dy**2))
        if K > 0: 
            gz += dz**(K-1)*np.exp(-expn*(dz**2))
        return C*np.array([gx*fy*fz,fx*gy*fz,fx*fy*gz])


    def __repr__(self): 
        """
            __repr__ 
            Representation of an instance of the class. 
            Display the basic information about PGBF. 
        """
        s = '' 
        s += "\n"
        s += "Primitive Gaussian:\n"
        s += f"Exponent: {self.expn: 18.10f}\n"
        s += f"Center  : ({self.center[0]: 18.10f} ,{self.center[1]: 18.10f},{self.center[2]: 18.10f})\n"
        s += f"Angular Moment : ({self.power[0]: 2d},{self.power[1]: 2d},{self.power[2]: 2d})\n"
        s += f"Norm    : {self.NORM: 18.10f}\n"
        return s  

    def show(self): 
        """
            show 
            Show the representation of an instance of the class. 
        """
        print(self.__repr__)

    def overlap(self): 
        """
            overlap 
            Calculate overlap for itself.
        """
        return overlap_pgbf(self,self)  
    

def main():
    """
        main 
        Main function to test this routine. 
    """
    pg = PGBF([0,0,0],[1,1,1],1,1)
    print(pg)
    print(pg.overlap())

if __name__ == '__main__':
    main() 

