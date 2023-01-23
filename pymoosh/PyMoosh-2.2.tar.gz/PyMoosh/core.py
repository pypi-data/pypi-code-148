import numpy as np
import scipy.optimize as optim
from math import *
import sys
import copy

from PyMoosh.materials import *

class Structure:
    """Each instance of Structure describes a multilayer completely.
    This includes the materials the multilayer is made of and the
    thickness of each layer.

    Args:
        materials (list) : a list of material definition
        layer_type (list) : how the different materials are stacked
        thickness (list) : thickness of each layer in nm

    Materials can be defined in the list :materials:
    -by giving their permittivity as a real number for non dispersive materials
    -by giving a list of two floats. The first is the permittivity and the
    second one the permeability. It is considered non dispersive.
    -by giving its name for dispersive materials that are in the database.
    -by giving a custom permittivity function, taking as an argument the
    wavelength in nanometer.

    .. warning: the working wavelength always is given in nanometers.

    Example: [1.,'Si','Au'] means we will use a material with a permittivity
    of 1. (air), silicon and gold.

    Each material can then be refered to by its position in the list :materials:
    The list layer_type is used to describe how the different materials are
    placed in the structure, using the place of each material in the list
    :materials:

    Example: [0,1,2,0] describes a superstrate made of air (permittivity 1.),
    on top of Si, on top of gold and a substrate made of air.

    The thickness of each layer is given in the :thickness: list, in nanometers
    typically. The thickness of the superstrate is assumed to be zero by most
    of the routines (like :coefficient:, :absorption:) so that the first
    interface is considered as the phase reference. The reflection coefficient
    of the structure will thus never be impacted by the thickness of the first
    layer.For other routines (like :field:), this thickness define the part
    of the superstrate (or substrate) that must be represented on the figure.

    Example: [0,200,300,500] actually refers to an infinite air superstrate but
    non of it will be represented, a 200 nm thick silicon layer, a 300 nm thick
    gold layer and an infinite substrate, of which a thickness of 500 nm will be
    represented is asked.
    """

    def __init__(self, materials, layer_type, thickness, verbose=True):

        materials_final=list()
        if verbose :
            print("List of materials:")
        for mat in materials:
            if issubclass(mat.__class__,Material):
                materials_final.append(mat)
                if verbose :
                    print("Object:",mat.__class__.__name__)
            elif isinstance(mat,float) or isinstance(mat,complex):
                new_mat = Material(mat)
                materials_final.append(new_mat)
                if verbose :
                    print("Simple, non dispersive: epsilon=",mat)
            elif isinstance(mat,list):
                newmat = MagneticND(mat[0],mat[1])
                materials_final.append(new_mat)
                if verbose :
                    print("Magnetic, non dispersive: epsilon=", mat[0]," mu=",mat[1])
            elif mat.__class__.__name__ == 'function':
                newmat = CustomFunction(mat)
                materials_final.append(new_mat)
                if verbose :
                    print("Custom dispersive material. Epsilon=",mat.__name__,"(wavelength in nm)")
            elif isinstance(mat,str):
                # from file in shipped database
                import pkgutil
                f = pkgutil.get_data(__name__, "data/material_data.json")
                f_str = f.decode(encoding='utf8')
                database = json.loads(f_str)
                if mat in database:
                    if verbose :
                        print("Database material:",mat)
                    material_data = database[mat]
                    model = material_data["model"]
#                    match model:
#                    case "ExpData":
                    if model == "ExpData":
                        wl=np.array(material_data["wavelength_list"])
                        epsilon = np.array(material_data["permittivities"])
                        if "permittivities_imag" in material_data:
                            epsilon = epsilon + 1j*np.array(material_data["permittivities_imag"])
                        new_mat= ExpData(wl,epsilon)
                        materials_final.append(new_mat)
#                    case "BrendelBormann"
                    elif model == "BrendelBormann":
                        f0 = material_data["f0"]
                        Gamma0 = material_data["Gamma0"]
                        omega_p = material_data["omega_p"]
                        ff = material_data["f"]
                        gamma = material_data["Gamma"]
                        omega = material_data["omega"]
                        sigma = material_data["sigma"]
                        new_mat = BrendelBormann(f0,Gamma0,omega_p,ff,gamma,omega,sigma)
                        materials_final.append(new_mat)
#                    case "CustomFunction":
                    elif model == "CustomFunction":
                        permittivity = material_data["function"]
                        new_mat = CustomFunction(authorized[permittivity])
                        materials_final.append(new_mat)
#                    case _:
                    else:
                        print(model," not an existing model.")
                        #sys.exit()
                else:
                    print(mat,"Unknown material")
                    print("Known materials:\n", existing_materials())
                    #sys.exit()
            else:
                print("Whhaaaaat ? That has nothing to do here :",mat)
#                sys.exit( )
        self.materials = materials_final
        self.layer_type = layer_type
        self.thickness = thickness

    def polarizability(self, wavelength):
        """ Computes the actual permittivity of each material considered in
        the structure. This method is called before each calculation.

        Args:
            wavelength (float): the working wavelength (in nanometers)
        """

        # Create empty mu and epsilon arrays
        mu = np.ones_like(self.materials, dtype=complex)
        epsilon = np.ones_like(self.materials, dtype=complex)
        # Loop over all materials
        for k in range(len(self.materials)):
            # Populate epsilon and mu arrays from the material.
            material = self.materials[k]
            epsilon[k] = material.get_permittivity(wavelength)
            mu[k] = material.get_permeability(wavelength)

        return epsilon, mu


class Beam:
    """ An object of the class contains all the parameters defining an incident
    beam. At initialization, a few messages will be displayed to inform the
    user.

    Args:
        wavelength (float): Wavelength in vacuum in nanometers
        incidence (float): Incidence angle in radians
        polarization (int) : '0' for TE polarization, TM otherwise
        waist (float): waist of the incident beam along the $x$ direction

    """

    def __init__(self, wavelength, incidence, polarization, horizontal_waist):
        self.wavelength = wavelength
        self.incidence = incidence
        tmp = incidence * 180 / np.pi
        print("Incidence in degrees:", tmp)
        self.polarization = polarization
        if (polarization == 0):
            print("E//, TE, s polarization")
        else:
            print("H//, TM, p polarization")
        self.waist = horizontal_waist


class Window:
    """An object containing all the parameters defining the spatial domain
    which is represented.

    Args:
        width (float): width of the spatial domain (in nm)
        beam_relative_position (float): relative position of the beam center
        horizontal_pixel_size (float): size in nm of a pixel, horizontally
        vertical_pixel_size (float): size in nm of a pixel, vertically

    The number of pixel for each layer will be computed later, but the number of
    pixel horizontally is computed and stored in nx.

    The position of the center of the beam is automatically deduced from
    the relative position: 0 means complete left of the domain, 1 complete
    right and 0.5 in the middle of the domaine, of course.
    """

    def __init__(self, width, beam_relative_position, horizontal_pixel_size,
                 vertical_pixel_size):
        self.width = width
        self.C = beam_relative_position
        self.ny = 0
        self.px = float(horizontal_pixel_size)
        self.py = float(vertical_pixel_size)
        self.nx = int(np.floor(width / self.px))
        print("Pixels horizontally:", self.nx)


""" There we go for the most fundamental functions... """


def cascade(A, B):
    """
    This function takes two 2x2 matrixes A and B, that are assumed to be scattering matrixes
    and combines them assuming A is the "upper" one, and B the "lower" one, physically.
    The result is a 2x2 scattering matrix.

    Args:
        A (2x2 numpy array):
        B (2x2 numpy array):

    """
    t = 1 / (1 - B[0, 0] * A[1, 1])
    S = np.zeros((2, 2), dtype=complex)
    S[0, 0] = A[0, 0] + A[0, 1] * B[0, 0] * A[1, 0] * t
    S[0, 1] = A[0, 1] * B[0, 1] * t
    S[1, 0] = B[1, 0] * A[1, 0] * t
    S[1, 1] = B[1, 1] + A[1, 1] * B[0, 1] * B[1, 0] * t
    return (S)


def coefficient(struct, wavelength, incidence, polarization):
    """
    This function computes the reflection and transmission coefficients
    of the structure.

    Args:
        struct (Structure): belongs to the Structure class
        wavelength (float): wavelength of the incidence light (in nm)
        incidence (float): incidence angle in radians
        polarization (float): 0 for TE, 1 (or anything) for TM

    returns:
        r (complex): reflection coefficient, phase origin at first interface
        t (complex): transmission coefficient
        R (float): Reflectance (energy reflection)
        T (float): Transmittance (energie transmission)


    R and T are the energy coefficients (real quantities)

    .. warning: The transmission coefficients have a meaning only if the lower medium
    is lossless, or they have no true meaning.
    """
    # In order to get a phase that corresponds to the expected reflected coefficient,
    # we make the height of the upper (lossless) medium vanish. It changes only the
    # phase of the reflection coefficient.

    # The medium may be dispersive. The permittivity and permability of each
    # layer has to be computed each time.
    Epsilon, Mu = struct.polarizability(wavelength)
    thickness = copy.deepcopy(struct.thickness)
    # In order to ensure that the phase reference is at the beginning
    # of the first layer.
    thickness[0] = 0
    Type = struct.layer_type
    # The boundary conditions will change when the polarization changes.
    if polarization == 0:
        f = Mu
    else:
        f = Epsilon
    # Wavevector in vacuum.
    k0 = 2 * np.pi / wavelength
    # Number of layers
    g = len(struct.layer_type)
    # Wavevector k_x, horizontal
    alpha = np.sqrt(Epsilon[Type[0]] * Mu[Type[0]]) * k0 * np.sin(incidence)
    # Computation of the vertical wavevectors k_z
    gamma = np.sqrt(
        Epsilon[Type] * Mu[Type] * k0 ** 2 - np.ones(g) * alpha ** 2)
    # Be cautious if the upper medium is a negative index one.
    if np.real(Epsilon[Type[0]]) < 0 and np.real(Mu[Type[0]]) < 0:
        gamma[0] = -gamma[0]

    # Changing the determination of the square root to achieve perfect stability
    if g > 2:
        gamma[1:g - 2] = gamma[1:g - 2] * (
                    1 - 2 * (np.imag(gamma[1:g - 2]) < 0))
    # Outgoing wave condition for the last medium
    if np.real(Epsilon[Type[g - 1]]) < 0 and np.real(
            Mu[Type[g - 1]]) < 0 and np.real(np.sqrt(Epsilon[Type[g - 1]] * Mu[
        Type[g - 1]] * k0 ** 2 - alpha ** 2)) != 0:
        gamma[g - 1] = -np.sqrt(
            Epsilon[Type[g - 1]] * Mu[Type[g - 1]] * k0 ** 2 - alpha ** 2)
    else:
        gamma[g - 1] = np.sqrt(
            Epsilon[Type[g - 1]] * Mu[Type[g - 1]] * k0 ** 2 - alpha ** 2)
    T = np.zeros(((2 * g, 2, 2)), dtype=complex)

    # first S matrix
    T[0] = [[0, 1], [1, 0]]
    for k in range(g - 1):
        # Layer scattering matrix
        t = np.exp((1j) * gamma[k] * thickness[k])
        T[2 * k + 1] = [[0, t], [t, 0]]
        # Interface scattering matrix
        b1 = gamma[k] / f[Type[k]]
        b2 = gamma[k + 1] / f[Type[k + 1]]
        T[2 * k + 2] = [[(b1 - b2) / (b1 + b2), 2 * b2 / (b1 + b2)],
                        [2 * b1 / (b1 + b2), (b2 - b1) / (b1 + b2)]]
    t = np.exp((1j) * gamma[g - 1] * thickness[g - 1])
    T[2 * g - 1] = [[0, t], [t, 0]]
    # Once the scattering matrixes have been prepared, now let us combine them
    A = np.zeros(((2 * g - 1, 2, 2)), dtype=complex)
    A[0] = T[0]

    for j in range(len(T) - 2):
        A[j + 1] = cascade(A[j], T[j + 1])
    # reflection coefficient of the whole structure
    r = A[len(A) - 1][0, 0]
    # transmission coefficient of the whole structure
    t = A[len(A) - 1][1, 0]
    # Energy reflexion coefficient;
    R = np.real(abs(r) ** 2)
    # Energy transmission coefficient;
    T = np.real(
        abs(t) ** 2 * gamma[g - 1] * f[Type[0]] / (gamma[0] * f[Type[g - 1]]))

    return r, t, R, T


# def fcoefficient(struct,wavelength)
#    '''Computation of the reflection coefficient of the structure using
#    the formalism of impedances...

def absorption(struct, wavelength, incidence, polarization):
    """
    This function computes the percentage of the incoming energy
    that is absorbed in each layer when the structure is illuminated
    by a plane wave.

    Args:
        struct (Structure): belongs to the Structure class
        wavelength (float): wavelength of the incidence light (in nm)
        incidence (float): incidence angle in radians
        polarization (float): 0 for TE, 1 (or anything) for TM

    returns:
        absorb (numpy array): absorption in each layer
        r (complex): reflection coefficient, phase origin at first interface
        t (complex): transmission coefficient
        R (float): Reflectance (energy reflection)
        T (float): Transmittance (energie transmission)
    R and T are the energy coefficients (real quantities)

    .. warning: The transmission coefficients have a meaning only if the lower medium
    is lossless, or they have no true meaning.

    """
    # The medium may be dispersive. The permittivity and permability of each
    # layer has to be computed each time.
    Epsilon, Mu = struct.polarizability(wavelength)

    thickness = copy.deepcopy(struct.thickness)
    # In order to ensure that the phase reference is at the beginning
    # of the first layer.
    thickness[0] = 0
    Type = struct.layer_type
    # The boundary conditions will change when the polarization changes.
    if polarization == 0:
        f = Mu
    else:
        f = Epsilon
    # Wavevector in vacuum.
    k0 = 2 * np.pi / wavelength
    # Number of layers
    g = len(struct.layer_type)
    # Wavevector k_x, horizontal
    alpha = np.sqrt(Epsilon[Type[0]] * Mu[Type[0]]) * k0 * np.sin(incidence)
    # Computation of the vertical wavevectors k_z
    gamma = np.sqrt(
        Epsilon[Type] * Mu[Type] * k0 ** 2 - np.ones(g) * alpha ** 2)
    # Be cautious if the upper medium is a negative index one.
    if np.real(Epsilon[Type[0]]) < 0 and np.real(Mu[Type[0]]) < 0:
        gamma[0] = -gamma[0]

    # Changing the determination of the square root to achieve perfect stability
    if g > 2:
        gamma[1:g - 2] = gamma[1:g - 2] * (
                1 - 2 * (np.imag(gamma[1:g - 2]) < 0))
    # Outgoing wave condition for the last medium
    if np.real(Epsilon[Type[g - 1]]) < 0 and np.real(
            Mu[Type[g - 1]]) < 0 and np.real(np.sqrt(Epsilon[Type[g - 1]] * Mu[
        Type[g - 1]] * k0 ** 2 - alpha ** 2)) != 0:
        gamma[g - 1] = -np.sqrt(
            Epsilon[Type[g - 1]] * Mu[Type[g - 1]] * k0 ** 2 - alpha ** 2)
    else:
        gamma[g - 1] = np.sqrt(
            Epsilon[Type[g - 1]] * Mu[Type[g - 1]] * k0 ** 2 - alpha ** 2)
    T = np.zeros(((2 * g, 2, 2)), dtype=complex)

    # first S matrix
    T[0] = [[0, 1], [1, 0]]
    for k in range(g - 1):
        # Layer scattering matrix
        t = np.exp((1j) * gamma[k] * thickness[k])
        T[2 * k + 1] = [[0, t], [t, 0]]
        # Interface scattering matrix
        b1 = gamma[k] / f[Type[k]]
        b2 = gamma[k + 1] / f[Type[k + 1]]
        T[2 * k + 2] = np.array(
            [[b1 - b2, 2 * b2], [2 * b1, b2 - b1]] / (b1 + b2))
    t = np.exp((1j) * gamma[g - 1] * thickness[g - 1])
    T[2 * g - 1] = [[0, t], [t, 0]]
    # Once the scattering matrixes have been prepared, now let us combine them
    H = np.zeros(((2 * g - 1, 2, 2)), dtype=complex)
    A = np.zeros(((2 * g - 1, 2, 2)), dtype=complex)
    H[0] = T[2 * g - 1]
    A[0] = T[0]
    for k in range(len(T) - 2):
        A[k + 1] = cascade(A[k], T[k + 1])
        H[k + 1] = cascade(T[2 * g - 2 - k], H[k])

    I = np.zeros(((2 * g, 2, 2)), dtype=complex)
    for k in range(len(T) - 1):
        I[k] = np.array(
            [[A[k][1, 0], A[k][1, 1] * H[len(T) - k - 2][0, 1]],
             [A[k][1, 0] * H[len(T) - k - 2][0, 0],
              H[len(T) - k - 2][0, 1]]] / (
                    1 - A[k][1, 1] * H[len(T) - k - 2][0, 0]))
#        I[k][0, 0] = A[k][1, 0] / (1 - A[k][1, 1] * H[len(T) - 2 - k][0, 0])
#        I[k][0, 1] = A[k][1, 1] * H[len(T) - 2 - k][0, 1] / (
#                1 - A[k][1, 1] * H[len(T) - 2 - k][0, 0])
#        I[k][1, 0] = A[k][1, 0] * H[len(T) - 2 - k][0, 0] / (
#                1 - A[k][1, 1] * H[len(T) - 2 - k][0, 0])
#        I[k][1, 1] = H[len(T) - 2 - k][0, 1] / (
#                1 - A[k][1, 1] * H[len(T) - 2 - k][0, 0])
    I[2 * g - 1][0, 0] = I[2 * g - 2][0, 0] * np.exp(
        1j * gamma[g - 1] * thickness[g - 1])
    I[2 * g - 1][0, 1] = I[2 * g - 2][0, 1] * np.exp(
        1j * gamma[g - 1] * thickness[g - 1])
    I[2 * g - 1][1, 0] = 0
    I[2 * g - 1][1, 1] = 0

    w = 0
    poynting = np.zeros(2 * g, dtype=complex)
    if polarization == 0:  # TE
        for k in range(2 * g):
            poynting[k] = np.real((I[k][0, 0] + I[k][1, 0]) * np.conj(
                (I[k][0, 0] - I[k][1, 0]) * gamma[w] / Mu[Type[w]])) * Mu[
                              Type[0]] / (gamma[0])
            w = w + 1 - np.mod(k + 1, 2)
    else:  # TM
        for k in range(2 * g):
            poynting[k] = np.real((I[k][0, 0] - I[k][1, 0]) * np.conj(
                (I[k][0, 0] + I[k][1, 0]) * gamma[w] / Epsilon[Type[w]]) *
                                  Epsilon[Type[0]] / (gamma[0]))
            w = w + 1 - np.mod(k + 1, 2)
    # Absorption in each layer
    tmp = abs(-np.diff(poynting))
    # absorb=np.zeros(g,dtype=complex)
    absorb = tmp[np.arange(0, 2 * g, 2)]
    # reflection coefficient of the whole structure
    r = A[len(A) - 1][0, 0]
    # transmission coefficient of the whole structure
    t = A[len(A) - 1][1, 0]
    # Energy reflexion coefficient;
    R = np.real(abs(r) ** 2)
    # Energy transmission coefficient;
    T = np.real(
        abs(t) ** 2 * gamma[g - 1] * f[Type[0]] / (gamma[0] * f[Type[g - 1]]))

    return absorb, r, t, R, T


def field(struct, beam, window):
    """Computes the electric (TE polarization) or magnetic (TM) field inside
    a multilayered structure illuminated by a gaussian beam.

    Args:
        struct (Structure): description (materials,thicknesses)of the multilayer
        beam (Beam): description of the incidence beam
        window (Window): description of the simulation domain

    Returns:
        En (np.array): a matrix with the complex amplitude of the field

    Afterwards the matrix may be used to represent either the modulus or the
    real part of the field.
    """

    # Wavelength in vacuum.
    lam = beam.wavelength
    # Computation of all the permittivities/permeabilities
    Epsilon, Mu = struct.polarizability(lam)
    thickness = np.array(struct.thickness)
    w = beam.waist
    pol = beam.polarization
    d = window.width
    theta = beam.incidence
    C = window.C
    ny = np.floor(thickness / window.py)
    nx = window.nx
    Type = struct.layer_type
    print("Pixels vertically:", int(sum(ny)))

    # Number of modes retained for the description of the field
    # so that the last mode has an amplitude < 1e-3 - you may want
    # to change it if the structure present reflexion coefficients
    # that are subject to very swift changes with the angle of incidence.

    nmod = int(np.floor(0.83660 * d / w))

    # ----------- Do not touch this part ---------------
    l = lam / d
    w = w / d
    thickness = thickness / d

    if pol == 0:
        f = Mu
    else:
        f = Epsilon
    # Wavevector in vacuum, no dimension
    k0 = 2 * pi / l
    # Initialization of the field component
    En = np.zeros((int(sum(ny)), int(nx)))
    # Total number of layers
    # g=Type.size-1
    g = len(struct.layer_type) - 1
    # Amplitude of the different modes
    nmodvect = np.arange(-nmod, nmod + 1)
    # First factor makes the gaussian beam, the second one the shift
    # a constant phase is missing, it's just a change in the time origin.
    X = np.exp(-w ** 2 * pi ** 2 * nmodvect ** 2) * np.exp(
        -2 * 1j * pi * nmodvect * C)

    # Scattering matrix corresponding to no interface.
    T = np.zeros((2 * g + 2, 2, 2), dtype=complex)
    T[0] = [[0, 1], [1, 0]]
    for nm in np.arange(2 * nmod + 1):

        alpha = np.sqrt(Epsilon[Type[0]] * Mu[Type[0]]) * k0 * sin(
            theta) + 2 * pi * (nm - nmod)
        gamma = np.sqrt(
            Epsilon[Type] * Mu[Type] * k0 ** 2 - np.ones(g + 1) * alpha ** 2)

        if np.real(Epsilon[Type[0]]) < 0 and np.real(Mu[Type[0]]) < 0:
            gamma[0] = -gamma[0]

        if g > 2:
            gamma[1:g - 1] = gamma[1:g - 1] * (
                    1 - 2 * (np.imag(gamma[1:g - 1]) < 0))
        if np.real(Epsilon[Type[g]]) < 0 and np.real(
                Mu[Type[g]]) < 0 and np.real(
            np.sqrt(Epsilon[Type[g]] * k0 ** 2 - alpha ** 2)) != 0:
            gamma[g] = -np.sqrt(
                Epsilon[Type[g]] * Mu[Type[g]] * k0 ** 2 - alpha ** 2)
        else:
            gamma[g] = np.sqrt(
                Epsilon[Type[g]] * Mu[Type[g]] * k0 ** 2 - alpha ** 2)

        for k in range(g):
            t = np.exp(1j * gamma[k] * thickness[k])
            T[2 * k + 1] = np.array([[0, t], [t, 0]])
            b1 = gamma[k] / f[Type[k]]
            b2 = gamma[k + 1] / f[Type[k + 1]]
            T[2 * k + 2] = np.array([[b1 - b2, 2 * b2], [2 * b1, b2 - b1]]) / (
                    b1 + b2)
        t = np.exp(1j * gamma[g] * thickness[g])
        T[2 * g + 1] = np.array([[0, t], [t, 0]])

        H = np.zeros((len(T) - 1, 2, 2), dtype=complex)
        A = np.zeros((len(T) - 1, 2, 2), dtype=complex)

        H[0] = T[2 * g + 1]
        A[0] = T[0]

        for k in range(len(T) - 2):
            A[k + 1] = cascade(A[k], T[k + 1])
            H[k + 1] = cascade(T[len(T) - k - 2], H[k])

        I = np.zeros((len(T), 2, 2), dtype=complex)
        for k in range(len(T) - 1):
            I[k] = np.array(
                [[A[k][1, 0], A[k][1, 1] * H[len(T) - k - 2][0, 1]],
                 [A[k][1, 0] * H[len(T) - k - 2][0, 0],
                  H[len(T) - k - 2][0, 1]]] / (
                        1 - A[k][1, 1] * H[len(T) - k - 2][0, 0]))

        h = 0
        t = 0



        E = np.zeros((int(np.sum(ny)), 1), dtype=complex)
        for k in range(g + 1):
            for m in range(int(ny[k])):
                h = h + float(thickness[k]) / ny[k]
                #The expression for the field used here is based on the assumption
                # that the structure is illuminated from above only, with an Amplitude
                # of 1 for the incident wave. If you want only the reflected
                # field, take off the second term.
                E[t, 0] = I[2 * k][0, 0] * np.exp(1j * gamma[k] * h) + \
                          I[2 * k + 1][1, 0] * np.exp(
                    1j * gamma[k] * (thickness[k] - h))
                t += 1
            h = 0
        E = E * np.exp(1j * alpha * np.arange(0, nx) / nx)
        En = En + X[int(nm)] * E

    return En


def Angular(structure, wavelength, polarization, theta_min, theta_max,
            n_points):
    """Represents the reflexion coefficient (reflectance and phase) for a
    multilayered structure. This is an automated call to the :coefficient:
    function making the angle of incidence vary.

    Args:
        structure (Structure): the object describing the multilayer
        wavelength (float): the working wavelength in nm
        polarization (float): 0 for TE, 1 for TM
        theta_min (float): minimum angle of incidence in degrees
        theta_max (float): maximum angle of incidence in degrees
        n_points (int): number of different angle of incidence

    Returns:
        incidence (numpy array): angles of incidence considered
        r (numpy complex array): reflexion coefficient for each angle
        t (numpy complex array): transmission coefficient
        R (numpy array): Reflectance
        T (numpy array): Transmittance

    .. warning: The incidence angle is in degrees here, contrarily to
    other functions.

    """

    # theta min and max in degrees this time !
    import matplotlib.pyplot as plt
    r = np.zeros(n_points, dtype=complex)
    t = np.zeros(n_points, dtype=complex)
    R = np.zeros(n_points)
    T = np.zeros(n_points)
    incidence = np.zeros(n_points)
    incidence = np.linspace(theta_min, theta_max, n_points)
    for k in range(n_points):
        r[k], t[k], R[k], T[k] = coefficient(structure, wavelength,
                                             incidence[k] / 180 * np.pi,
                                             polarization)

    return incidence, r, t, R, T


def Spectrum(structure, incidence, polarization, wl_min, wl_max, n_points):
    """Represents the reflexion coefficient (reflectance and phase) for a
    multilayered structure. This is an automated call to the :coefficient:
    function making the angle of incidence vary.

    Args:
        structure (Structure): the object describing the multilayer
        incidence (float): incidence angle in degrees
        polarization (float): 0 for TE, 1 for TM
        wl_min (float): minimum wavelength of the spectrum
        theta_max (float): maximum wavelength of the spectrum
        n_points (int): number of points in the spectrum

    Returns:
        wl (numpy array): wavelength considered
        r (numpy complex array): reflexion coefficient for each wavelength
        t (numpy complex array): transmission coefficient
        R (numpy array): Reflectance
        T (numpy array): Transmittance


    .. warning: The incidence angle is in degrees here, contrarily to
    other functions.

    """
    # incidence in degrees
    import matplotlib.pyplot as plt
    r = np.zeros(n_points, dtype=complex)
    t = np.zeros(n_points, dtype=complex)
    R = np.zeros(n_points)
    T = np.zeros(n_points)
    wl = np.linspace(wl_min, wl_max, n_points)
    theta = incidence / 180 * np.pi
    for k in range(n_points):
        r[k], t[k], R[k], T[k] = coefficient(structure, wl[k], theta,
                                             polarization)
    return wl, r, t, R, T


def solar(wavelength):
    wavelength_list=[280,280.5,281,281.5,282,282.5,283,283.5,284,284.5,285,285.5,286,286.5,287,287.5,288,288.5,289,289.5,290,290.5,291,291.5,292,292.5,293,293.5,294,294.5,295,295.5,296,296.5,297,297.5,298,298.5,299,299.5,300,300.5,301,301.5,302,302.5,303,303.5,304,304.5,305,305.5,306,306.5,307,307.5,308,308.5,309,309.5,310,310.5,311,311.5,312,312.5,313,313.5,314,314.5,315,315.5,316,316.5,317,317.5,318,318.5,319,319.5,320,320.5,321,321.5,322,322.5,323,323.5,324,324.5,325,325.5,326,326.5,327,327.5,328,328.5,329,329.5,330,330.5,331,331.5,332,332.5,333,333.5,334,334.5,335,335.5,336,336.5,337,337.5,338,338.5,339,339.5,340,340.5,341,341.5,342,342.5,343,343.5,344,344.5,345,345.5,346,346.5,347,347.5,348,348.5,349,349.5,350,350.5,351,351.5,352,352.5,353,353.5,354,354.5,355,355.5,356,356.5,357,357.5,358,358.5,359,359.5,360,360.5,361,361.5,362,362.5,363,363.5,364,364.5,365,365.5,366,366.5,367,367.5,368,368.5,369,369.5,370,370.5,371,371.5,372,372.5,373,373.5,374,374.5,375,375.5,376,376.5,377,377.5,378,378.5,379,379.5,380,380.5,381,381.5,382,382.5,383,383.5,384,384.5,385,385.5,386,386.5,387,387.5,388,388.5,389,389.5,390,390.5,391,391.5,392,392.5,393,393.5,394,394.5,395,395.5,396,396.5,397,397.5,398,398.5,399,399.5,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,586,587,588,589,590,591,592,593,594,595,596,597,598,599,600,601,602,603,604,605,606,607,608,609,610,611,612,613,614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,629,630,631,632,633,634,635,636,637,638,639,640,641,642,643,644,645,646,647,648,649,650,651,652,653,654,655,656,657,658,659,660,661,662,663,664,665,666,667,668,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691,692,693,694,695,696,697,698,699,700,701,702,703,704,705,706,707,708,709,710,711,712,713,714,715,716,717,718,719,720,721,722,723,724,725,726,727,728,729,730,731,732,733,734,735,736,737,738,739,740,741,742,743,744,745,746,747,748,749,750,751,752,753,754,755,756,757,758,759,760,761,762,763,764,765,766,767,768,769,770,771,772,773,774,775,776,777,778,779,780,781,782,783,784,785,786,787,788,789,790,791,792,793,794,795,796,797,798,799,800,801,802,803,804,805,806,807,808,809,810,811,812,813,814,815,816,817,818,819,820,821,822,823,824,825,826,827,828,829,830,831,832,833,834,835,836,837,838,839,840,841,842,843,844,845,846,847,848,849,850,851,852,853,854,855,856,857,858,859,860,861,862,863,864,865,866,867,868,869,870,871,872,873,874,875,876,877,878,879,880,881,882,883,884,885,886,887,888,889,890,891,892,893,894,895,896,897,898,899,900,901,902,903,904,905,906,907,908,909,910,911,912,913,914,915,916,917,918,919,920,921,922,923,924,925,926,927,928,929,930,931,932,933,934,935,936,937,938,939,940,941,942,943,944,945,946,947,948,949,950,951,952,953,954,955,956,957,958,959,960,961,962,963,964,965,966,967,968,969,970,971,972,973,974,975,976,977,978,979,980,981,982,983,984,985,986,987,988,989,990,991,992,993,994,995,996,997,998,999,1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019,1020,1021,1022,1023,1024,1025,1026,1027,1028,1029,1030,1031,1032,1033,1034,1035,1036,1037,1038,1039,1040,1041,1042,1043,1044,1045,1046,1047,1048,1049,1050,1051,1052,1053,1054,1055,1056,1057,1058,1059,1060,1061,1062,1063,1064,1065,1066,1067,1068,1069,1070,1071,1072,1073,1074,1075,1076,1077,1078,1079,1080,1081,1082,1083,1084,1085,1086,1087,1088,1089,1090,1091,1092,1093,1094,1095,1096,1097,1098,1099,1100,1101,1102,1103,1104,1105,1106,1107,1108,1109,1110,1111,1112,1113,1114,1115,1116,1117,1118,1119,1120,1121,1122,1123,1124,1125,1126,1127,1128,1129,1130,1131,1132,1133,1134,1135,1136,1137,1138,1139,1140,1141,1142,1143,1144,1145,1146,1147,1148,1149,1150,1151,1152,1153,1154,1155,1156,1157,1158,1159,1160,1161,1162,1163,1164,1165,1166,1167,1168,1169,1170,1171,1172,1173,1174,1175,1176,1177,1178,1179,1180,1181,1182,1183,1184,1185,1186,1187,1188,1189,1190,1191,1192,1193,1194,1195,1196,1197,1198,1199,1200,1201,1202,1203,1204,1205,1206,1207,1208,1209,1210,1211,1212,1213,1214,1215,1216,1217,1218,1219,1220,1221,1222,1223,1224,1225,1226,1227,1228,1229,1230,1231,1232,1233,1234,1235,1236,1237,1238,1239,1240,1241,1242,1243,1244,1245,1246,1247,1248,1249,1250,1251,1252,1253,1254,1255,1256,1257,1258,1259,1260,1261,1262,1263,1264,1265,1266,1267,1268,1269,1270,1271,1272,1273,1274,1275,1276,1277,1278,1279,1280,1281,1282,1283,1284,1285,1286,1287,1288,1289,1290,1291,1292,1293,1294,1295,1296,1297,1298,1299,1300,1301,1302,1303,1304,1305,1306,1307,1308,1309,1310,1311,1312,1313,1314,1315,1316,1317,1318,1319,1320,1321,1322,1323,1324,1325,1326,1327,1328,1329,1330,1331,1332,1333,1334,1335,1336,1337,1338,1339,1340,1341,1342,1343,1344,1345,1346,1347,1348,1349,1350,1351,1352,1353,1354,1355,1356,1357,1358,1359,1360,1361,1362,1363,1364,1365,1366,1367,1368,1369,1370,1371,1372,1373,1374,1375,1376,1377,1378,1379,1380,1381,1382,1383,1384,1385,1386,1387,1388,1389,1390,1391,1392,1393,1394,1395,1396,1397,1398,1399,1400,1401,1402,1403,1404,1405,1406,1407,1408,1409,1410,1411,1412,1413,1414,1415,1416,1417,1418,1419,1420,1421,1422,1423,1424,1425,1426,1427,1428,1429,1430,1431,1432,1433,1434,1435,1436,1437,1438,1439,1440,1441,1442,1443,1444,1445,1446,1447,1448,1449,1450,1451,1452,1453,1454,1455,1456,1457,1458,1459,1460,1461,1462,1463,1464,1465,1466,1467,1468,1469,1470,1471,1472,1473,1474,1475,1476,1477,1478,1479,1480,1481,1482,1483,1484,1485,1486,1487,1488,1489,1490,1491,1492,1493,1494,1495,1496,1497,1498,1499,1500,1501,1502,1503,1504,1505,1506,1507,1508,1509,1510,1511,1512,1513,1514,1515,1516,1517,1518,1519,1520,1521,1522,1523,1524,1525,1526,1527,1528,1529,1530,1531,1532,1533,1534,1535,1536,1537,1538,1539,1540,1541,1542,1543,1544,1545,1546,1547,1548,1549,1550,1551,1552,1553,1554,1555,1556,1557,1558,1559,1560,1561,1562,1563,1564,1565,1566,1567,1568,1569,1570,1571,1572,1573,1574,1575,1576,1577,1578,1579,1580,1581,1582,1583,1584,1585,1586,1587,1588,1589,1590,1591,1592,1593,1594,1595,1596,1597,1598,1599,1600,1601,1602,1603,1604,1605,1606,1607,1608,1609,1610,1611,1612,1613,1614,1615,1616,1617,1618,1619,1620,1621,1622,1623,1624,1625,1626,1627,1628,1629,1630,1631,1632,1633,1634,1635,1636,1637,1638,1639,1640,1641,1642,1643,1644,1645,1646,1647,1648,1649,1650,1651,1652,1653,1654,1655,1656,1657,1658,1659,1660,1661,1662,1663,1664,1665,1666,1667,1668,1669,1670,1671,1672,1673,1674,1675,1676,1677,1678,1679,1680,1681,1682,1683,1684,1685,1686,1687,1688,1689,1690,1691,1692,1693,1694,1695,1696,1697,1698,1699,1700,1702,1705,1710,1715,1720,1725,1730,1735,1740,1745,1750,1755,1760,1765,1770,1775,1780,1785,1790,1795,1800,1805,1810,1815,1820,1825,1830,1835,1840,1845,1850,1855,1860,1865,1870,1875,1880,1885,1890,1895,1900,1905,1910,1915,1920,1925,1930,1935,1940,1945,1950,1955,1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010,2015,2020,2025,2030,2035,2040,2045,2050,2055,2060,2065,2070,2075,2080,2085,2090,2095,2100,2105,2110,2115,2120,2125,2130,2135,2140,2145,2150,2155,2160,2165,2170,2175,2180,2185,2190,2195,2200,2205,2210,2215,2220,2225,2230,2235,2240,2245,2250,2255,2260,2265,2270,2275,2280,2285,2290,2295,2300,2305,2310,2315,2320,2325,2330,2335,2340,2345,2350,2355,2360,2365,2370,2375,2380,2385,2390,2395,2400,2405,2410,2415,2420,2425,2430,2435,2440,2445,2450,2455,2460,2465,2470,2475,2480,2485,2490,2495,2500,2505,2510,2515,2520,2525,2530,2535,2540,2545,2550,2555,2560,2565,2570,2575,2580,2585,2590,2595,2600,2605,2610,2615,2620,2625,2630,2635,2640,2645,2650,2655,2660,2665,2670,2675,2680,2685,2690,2695,2700,2705,2710,2715,2720,2725,2730,2735,2740,2745,2750,2755,2760,2765,2770,2775,2780,2785,2790,2795,2800,2805,2810,2815,2820,2825,2830,2835,2840,2845,2850,2855,2860,2865,2870,2875,2880,2885,2890,2895,2900,2905,2910,2915,2920,2925,2930,2935,2940,2945,2950,2955,2960,2965,2970,2975,2980,2985,2990,2995,3000,3005,3010,3015,3020,3025,3030,3035,3040,3045,3050,3055,3060,3065,3070,3075,3080,3085,3090,3095,3100,3105,3110,3115,3120,3125,3130,3135,3140,3145,3150,3155,3160,3165,3170,3175,3180,3185,3190,3195,3200,3205,3210,3215,3220,3225,3230,3235,3240,3245,3250,3255,3260,3265,3270,3275,3280,3285,3290,3295,3300,3305,3310,3315,3320,3325,3330,3335,3340,3345,3350,3355,3360,3365,3370,3375,3380,3385,3390,3395,3400,3405,3410,3415,3420,3425,3430,3435,3440,3445,3450,3455,3460,3465,3470,3475,3480,3485,3490,3495,3500,3505,3510,3515,3520,3525,3530,3535,3540,3545,3550,3555,3560,3565,3570,3575,3580,3585,3590,3595,3600,3605,3610,3615,3620,3625,3630,3635,3640,3645,3650,3655,3660,3665,3670,3675,3680,3685,3690,3695,3700,3705,3710,3715,3720,3725,3730,3735,3740,3745,3750,3755,3760,3765,3770,3775,3780,3785,3790,3795,3800,3805,3810,3815,3820,3825,3830,3835,3840,3845,3850,3855,3860,3865,3870,3875,3880,3885,3890,3895,3900,3905,3910,3915,3920,3925,3930,3935,3940,3945,3950,3955,3960,3965,3970,3975,3980,3985,3990,3995,4000]
    current_density=[1.065339187763039e-27,2.776330532212098e-26,1.285779581177973e-25,3.545779475655973e-24,2.709303897354827e-23,1.032296954384578e-22,4.199677915412361e-22,8.062160180999874e-22,1.659814687331175e-20,5.687214571918009e-20,1.836923792658453e-19,9.784402854278547e-19,3.147496107181308e-18,1.931407570427873e-17,6.316771859540225e-17,2.52098327311767e-16,1.44385801681531e-15,3.981986819181418e-15,1.307742593258595e-14,4.830942204138283e-14,1.403297257868835e-13,3.220149210694188e-13,8.203362347209513e-13,2.558402184944362e-12,6.300711974951335e-12,1.004123795885795e-11,2.037506917686444e-11,5.359866448601682e-11,9.870235051825085e-11,1.561094892829915e-10,2.915815242187597e-10,6.612936752093509e-10,1.140380001795021e-09,1.701274306010775e-09,2.312160138097572e-09,4.45218057478768e-09,6.94737305172433e-09,8.59171776509539e-09,1.183367074819127e-08,2.073120952303742e-08,2.4621832174311e-08,3.008845797038599e-08,4.672076095058792e-08,6.526069094513509e-08,7.094303020930719e-08,1.042223698612163e-07,1.728822971526271e-07,2.19177996732974e-07,2.315337210964514e-07,2.927186000776409e-07,4.038265982071959e-07,4.599175285378684e-07,4.571756705813024e-07,5.203117905555669e-07,6.875971749020835e-07,8.812679708670868e-07,9.372458249409015e-07,1.027912635648721e-06,1.007312087911933e-06,1.077940595628125e-06,1.269983889692768e-06,1.636643705564915e-06,2.074035856640881e-06,2.10638065239525e-06,2.343019822785696e-06,2.487717862916464e-06,2.701789875535308e-06,2.712156941602365e-06,3.022550864557215e-06,3.30331454573901e-06,3.451700995039068e-06,3.003750127312763e-06,3.13812187638517e-06,3.827296730469889e-06,4.374334890532242e-06,4.658796068804397e-06,4.499640433035939e-06,4.762097582946535e-06,5.251636144700268e-06,5.033490250295404e-06,5.282768306172342e-06,6.321543822342978e-06,6.460228312719803e-06,6.164927576909008e-06,5.749811850554473e-06,5.630612506345189e-06,5.513873334751327e-06,6.46813359768983e-06,7.175426790697917e-06,7.391105274320132e-06,7.290885208813495e-06,8.491108447040252e-06,9.994396963907359e-06,1.06929709802531e-05,1.046845027112573e-05,1.013125261069887e-05,9.263284168925642e-06,9.818472505282442e-06,1.117517928921073e-05,1.242254551480948e-05,1.251066537531927e-05,1.13763078503511e-05,1.071789359848761e-05,1.114572316557145e-05,1.164768764984713e-05,1.174438272791558e-05,1.15009265712093e-05,1.092275946663808e-05,1.114677591678217e-05,1.197374657515674e-05,1.249788598896455e-05,1.222648005164243e-05,1.121946802597398e-05,1.034174132842133e-05,1.013106964591626e-05,1.087109383111216e-05,1.180055935010378e-05,1.239406614162508e-05,1.263811743652534e-05,1.295464409772109e-05,1.372131318283047e-05,1.371164258929854e-05,1.292768755449658e-05,1.289061486833545e-05,1.345931404805701e-05,1.398389579430629e-05,1.420347725854395e-05,1.342856269460501e-05,1.157623567997306e-05,1.116749597470224e-05,1.273500030482122e-05,1.359649983569802e-05,1.329505590651589e-05,1.355921885116899e-05,1.37872512777613e-05,1.332362816951301e-05,1.329717910223499e-05,1.354751352840626e-05,1.306958538900054e-05,1.343713268459846e-05,1.486180706512316e-05,1.599451629856621e-05,1.557442232164303e-05,1.498882322781418e-05,1.466165726503965e-05,1.388047645888655e-05,1.477400005428562e-05,1.626987025398872e-05,1.722385586869311e-05,1.743578136260958e-05,1.745580535011492e-05,1.687655412894168e-05,1.585783678051049e-05,1.489238671316378e-05,1.311335619468687e-05,1.328755595891042e-05,1.238221042583224e-05,1.151147740629978e-05,1.355638510870072e-05,1.634970522786961e-05,1.731861795399229e-05,1.63899655224522e-05,1.51041762903846e-05,1.481459330456052e-05,1.555244081202395e-05,1.705784689492454e-05,1.757212511013017e-05,1.711396561177495e-05,1.774846214428687e-05,1.760574880960897e-05,1.830535305842296e-05,2.017320151842639e-05,2.164430110140669e-05,2.17110088547857e-05,2.133537853700036e-05,2.095923511358291e-05,1.975803472278089e-05,1.965181301028419e-05,2.057025600695456e-05,2.212972757993628e-05,2.246854980678456e-05,2.033981327067659e-05,2.068861049620061e-05,2.152707053868239e-05,2.017773261110874e-05,1.924889439994323e-05,1.856467487556427e-05,1.675721846591633e-05,1.673573638983571e-05,1.663371965037588e-05,1.777271643841435e-05,1.967843016388997e-05,2.040558368140005e-05,2.010267040427141e-05,2.15953332916534e-05,2.41226097490521e-05,2.602113878931691e-05,2.539286828697899e-05,2.267430757798521e-05,2.035227739463665e-05,2.141633743740301e-05,2.29739729286322e-05,2.340495391330137e-05,2.112042145737816e-05,1.802705437530141e-05,1.56155133969748e-05,1.401479432382519e-05,1.358587219561089e-05,1.57403693688698e-05,1.897407968797892e-05,2.08553111170595e-05,1.995477172701819e-05,1.927813458492698e-05,2.007087876534113e-05,2.027642984665549e-05,2.000874714212942e-05,1.984047262201968e-05,1.97266886332553e-05,2.144365508474793e-05,2.379773868740806e-05,2.499790321605621e-05,2.524099746440129e-05,2.677233830258657e-05,2.718629552006483e-05,2.506115353822447e-05,2.091498377401698e-05,1.516329683603104e-05,1.207391597349281e-05,1.570633872354483e-05,2.169671387663831e-05,2.565925455533112e-05,2.736672935687043e-05,2.409455581925232e-05,1.754390228976182e-05,1.360754769160455e-05,2.012261758678009e-05,2.728716822698285e-05,3.227013405945135e-05,3.431299014356464e-05,3.540983385629141e-05,3.584018713101407e-05,3.741974019471853e-05,3.89937922513326e-05,3.76387832197388e-05,3.834301667861305e-05,3.749334431298058e-05,3.665859865664603e-05,3.609096549810843e-05,3.778091669679795e-05,4.045565271597162e-05,3.457310574637821e-05,3.879913380744985e-05,4.134550495210639e-05,3.976185026030823e-05,3.94286130837142e-05,4.091229260133016e-05,4.223538131546527e-05,4.129055922046671e-05,3.959105364104125e-05,4.130662795170442e-05,3.793957732235236e-05,4.319333666277171e-05,4.270539572537253e-05,4.144921984602111e-05,4.131873981819292e-05,4.268427636189392e-05,4.157530871906663e-05,4.026148485897851e-05,4.075162137376904e-05,3.782446633626353e-05,3.024641890644205e-05,2.752016643841137e-05,4.588534777438714e-05,4.279127255828361e-05,3.962307850980432e-05,4.356266816659039e-05,4.78951455403059e-05,4.900312396694589e-05,4.310926937166667e-05,4.157301663277897e-05,4.776836502017007e-05,4.721724292531168e-05,5.065510695734049e-05,5.149295698317343e-05,5.029155794489314e-05,5.231952351054463e-05,4.701726844972315e-05,5.357563505063183e-05,5.43368248431525e-05,5.432811491525937e-05,5.643960893067814e-05,5.866150912348996e-05,5.627967760465547e-05,5.208698532485526e-05,5.599196849990166e-05,5.570911700959609e-05,5.766522365952737e-05,5.82694819442194e-05,5.714462250313099e-05,5.68153421912862e-05,5.656917212399126e-05,5.867939543894176e-05,5.935659032202961e-05,5.969359134558022e-05,5.800519233163988e-05,5.740469789390442e-05,5.873867602850793e-05,5.623566150552432e-05,5.878752561486324e-05,5.915076901580557e-05,5.69900313360382e-05,5.8073432163748e-05,6.121456350921684e-05,5.895911039011684e-05,5.973944111374148e-05,6.1829027609695e-05,5.983837881728823e-05,6.032085895963717e-05,6.239251892809876e-05,6.131342078868333e-05,6.246441805585911e-05,6.257907866709841e-05,6.293789070121794e-05,6.229933958869925e-05,6.124499598119056e-05,6.117260626654057e-05,4.970188858836186e-05,5.577705123019919e-05,6.049132584017504e-05,5.709941612761187e-05,6.393521363581599e-05,6.158188441102881e-05,5.883462195626867e-05,6.305391852182183e-05,6.168004200099694e-05,6.562665267999051e-05,6.253210296181338e-05,6.372939232959192e-05,6.211539363230832e-05,6.223209701518648e-05,6.213162321170657e-05,6.035005290077478e-05,6.042206462224751e-05,6.332156986095657e-05,5.912656136764465e-05,6.350023999768188e-05,6.61856724195313e-05,6.344591353146026e-05,6.195726380568368e-05,6.505935730259001e-05,6.349730451875206e-05,6.480539414191701e-05,6.664930115746522e-05,6.27362353623518e-05,6.153157914882063e-05,6.342813980972085e-05,6.413643468464868e-05,5.236490681904036e-05,6.000242785622065e-05,5.825665430341651e-05,6.371774692276901e-05,6.430119145548746e-05,6.586876937363988e-05,6.220518711792851e-05,6.702719782583253e-05,6.663155156294987e-05,6.489713389027971e-05,5.68659289377753e-05,6.521183331637175e-05,6.837300634264358e-05,6.583820822313771e-05,6.957529004580681e-05,6.844842000271169e-05,6.123841729142459e-05,6.571667135303543e-05,6.684226265325428e-05,6.982952664835273e-05,6.473409015235065e-05,6.809542262959562e-05,6.654873888749705e-05,6.438349745923461e-05,6.200528502401223e-05,6.761221867052425e-05,6.662337243398654e-05,6.909110491295619e-05,6.765333950276573e-05,6.714514778195485e-05,6.814356448404454e-05,6.632454872133955e-05,6.852517674492029e-05,6.811477266330831e-05,6.816328446852648e-05,6.968540669651094e-05,6.782363749273502e-05,6.92784769351666e-05,6.978292893624495e-05,6.87102808080671e-05,6.714056360937949e-05,6.870613092552521e-05,6.51113112584437e-05,6.638525281712651e-05,7.036137913357872e-05,6.710596517004784e-05,6.976550908045872e-05,6.851957922893356e-05,6.907274409543081e-05,6.543049030580671e-05,6.985989478106227e-05,6.93435721857362e-05,6.775875938718214e-05,6.791910087601416e-05,6.581103292641489e-05,6.962029536112529e-05,7.003694035136613e-05,6.979447783417155e-05,6.833453146264296e-05,6.788358560216744e-05,6.971377226962177e-05,6.768233238370265e-05,6.877730623656318e-05,7.006224176701871e-05,7.050545083097236e-05,7.170804014564064e-05,7.257675693348077e-05,7.255564561241017e-05,7.209648845333921e-05,7.047126255445006e-05,7.213997375354058e-05,7.062192902642576e-05,6.107859855911432e-05,6.504948926794104e-05,6.968941181570833e-05,6.834090909220828e-05,6.944356344473447e-05,6.922626562225603e-05,6.846711055896618e-05,7.067684258843332e-05,7.100188455124796e-05,7.025032152113545e-05,7.036297957277609e-05,7.11897873723881e-05,7.046741024100519e-05,6.952436551818058e-05,7.111412439767118e-05,7.248046518217485e-05,7.24739588740811e-05,7.223797049534819e-05,7.279165007595914e-05,7.267197100211107e-05,7.223804287702042e-05,7.204759061253575e-05,7.179715806898657e-05,7.299749550940729e-05,7.208147327755303e-05,7.000163418012809e-05,7.269255152425185e-05,7.089350506067762e-05,7.010547775257125e-05,7.288313246726497e-05,7.334456562780755e-05,7.349297218312767e-05,7.39261523642718e-05,7.13789287243644e-05,7.097260214362206e-05,7.085065511071038e-05,7.050175936568803e-05,7.05440785167255e-05,7.269901762030547e-05,6.884516807549402e-05,7.13981339947326e-05,7.054896830080586e-05,7.186366878336889e-05,6.931925194386287e-05,7.385796882901987e-05,7.28324974663277e-05,7.383598088547435e-05,7.226431742404427e-05,7.484723327077498e-05,7.546244531519964e-05,7.526723998757106e-05,7.38100039075475e-05,7.396657350701493e-05,7.422653630407598e-05,7.511267294770235e-05,7.490319234582606e-05,7.556417373433171e-05,7.351484753296082e-05,7.329562757496394e-05,7.27105745606401e-05,7.056272886093983e-05,7.106352156636599e-05,7.563882336563728e-05,7.273466961508865e-05,7.515697053111446e-05,7.444102732615302e-05,7.110972520048046e-05,6.252373885746541e-05,6.548290267891794e-05,7.33193365938272e-05,7.369576150152559e-05,7.426938625404323e-05,7.406826975651488e-05,7.357338017858047e-05,7.381782112814963e-05,7.458599977324567e-05,7.601933381661333e-05,7.60747299231025e-05,7.564716334276115e-05,7.601844915173038e-05,7.744505974198754e-05,7.649391631427985e-05,7.646238203240646e-05,7.551164876750812e-05,7.628434724591527e-05,7.628928528444376e-05,7.577275358650898e-05,7.676574970558859e-05,7.617694088671619e-05,7.669841866558751e-05,7.616170856591329e-05,7.639419045474648e-05,7.621078333969333e-05,7.668469831749365e-05,7.596770155708071e-05,7.557833641486706e-05,7.573841250423422e-05,7.413868103879028e-05,5.349656048642988e-05,6.200477835230651e-05,6.249386935405356e-05,6.559782064721411e-05,6.853822957314794e-05,7.061867989358287e-05,7.02748589080255e-05,6.956695811109097e-05,7.106456707940951e-05,7.099889277546194e-05,7.513129916469262e-05,7.405462179009324e-05,7.262038699702661e-05,7.218945869013001e-05,7.136799909185587e-05,7.155449449159135e-05,7.206915230845584e-05,7.404574297163161e-05,7.492202766542503e-05,7.463084424040359e-05,7.442951059785852e-05,7.429563667384299e-05,7.46685711764577e-05,7.523069528549691e-05,7.52222909691088e-05,7.484708850743049e-05,7.407487257350497e-05,7.481615740615909e-05,7.237929973160465e-05,7.322335849643435e-05,6.383988697347333e-05,5.945372652617835e-05,5.33828038418528e-05,5.706571039557119e-05,6.297833597118515e-05,7.204271691327145e-05,6.654298052334978e-05,6.145863450801679e-05,6.052314160632941e-05,6.313481710416425e-05,6.343811239567417e-05,6.08906796531581e-05,6.136127311644329e-05,6.625375944588692e-05,6.292293986469596e-05,6.790115022129816e-05,7.051700777130698e-05,7.294494641535963e-05,7.198622703929062e-05,7.137978121961524e-05,7.135821952369518e-05,7.282016041241447e-05,7.075545712689611e-05,7.257710275702592e-05,7.239508697856144e-05,7.252262348505178e-05,7.412619117912452e-05,7.481234530475434e-05,7.487694996843434e-05,7.481546575906879e-05,7.495780833873663e-05,7.460095865217568e-05,7.443564695518306e-05,7.443851809484862e-05,7.42055777887579e-05,7.457049401056985e-05,7.428207717390964e-05,7.531457760121731e-05,7.518979964068017e-05,7.437129964855995e-05,7.440270525190491e-05,7.495210627144557e-05,7.29145219857939e-05,1.626097695919259e-05,9.422771554025209e-06,4.214197035471458e-05,2.328870331799514e-05,3.310479687898324e-05,4.220636832850827e-05,5.01839231813061e-05,6.009193905331909e-05,6.879462958345309e-05,6.975005157223107e-05,7.188432972958995e-05,7.246134033588694e-05,7.312652790379065e-05,7.317773391569784e-05,7.32724011005823e-05,7.336706828546679e-05,7.363024000333055e-05,7.328144880961255e-05,7.328816422031499e-05,7.370814680988701e-05,7.299353864465806e-05,7.290496760505797e-05,7.334421980426239e-05,7.313574450338945e-05,7.273733969455359e-05,7.314578142860703e-05,7.32768887642613e-05,7.247134509147236e-05,7.164450512222823e-05,7.143084246817793e-05,6.931671054292637e-05,7.034596183739118e-05,6.976608813383665e-05,6.935672152286014e-05,7.006359289156722e-05,6.989608561718325e-05,6.876767143174695e-05,6.995013864153194e-05,7.137281649426398e-05,7.007426516701891e-05,6.900386087068056e-05,6.985026801865408e-05,7.002132199497791e-05,6.882347770104551e-05,6.971744765009005e-05,6.826979007802653e-05,7.113545286375845e-05,7.047733457251037e-05,7.03177329852168e-05,6.862853777288184e-05,6.878502694826896e-05,6.870036451896994e-05,6.705450984349182e-05,6.59470863430057e-05,5.9151737321732e-05,5.867841024395844e-05,5.461137335141112e-05,5.59707453893595e-05,5.411564414607869e-05,5.962244096600717e-05,5.683904316774142e-05,6.587234341976703e-05,6.290695477450173e-05,4.452601433999728e-05,6.196590456886779e-05,6.431624282210978e-05,6.203326938698258e-05,6.548977491657691e-05,5.65884835541454e-05,6.195788307110176e-05,6.114548726667391e-05,6.174780089710505e-05,5.98374716336628e-05,6.407905210337686e-05,6.265486871186218e-05,6.736900016697517e-05,6.537482397440782e-05,6.793425277273683e-05,6.732865783983071e-05,6.756352188992147e-05,6.861686019642678e-05,6.831978168632166e-05,6.751595587188726e-05,6.815682641488089e-05,6.694867497082123e-05,6.907966056633393e-05,6.931109694212361e-05,6.7553806661025e-05,6.766561704285957e-05,6.732139232841922e-05,6.109511766520153e-05,6.672507913861695e-05,6.641565633643135e-05,6.619107530924376e-05,5.84567638914599e-05,6.278024341907491e-05,6.699595467912967e-05,6.834861532757965e-05,6.844906982928027e-05,6.851157622870601e-05,6.834579887628863e-05,6.833040490308436e-05,6.89435733716294e-05,6.944068426266084e-05,6.803830866475187e-05,6.700955278262154e-05,5.913051823239384e-05,6.383289972937956e-05,6.695993112509565e-05,6.636334851462448e-05,6.769845741179656e-05,6.681799629551478e-05,6.780569648890867e-05,6.720592667213642e-05,6.610272945706844e-05,6.522483386894721e-05,6.712407023899798e-05,6.743909377413351e-05,6.724907660392307e-05,6.620801744599319e-05,6.649636672642595e-05,6.437830286789004e-05,6.61424444763868e-05,6.599160991808336e-05,6.633508427585478e-05,6.720586394135382e-05,6.466600473447664e-05,6.496013328931752e-05,6.586608642632212e-05,6.68175282273676e-05,6.613253622969769e-05,6.634370895422281e-05,6.519646588311398e-05,6.27171193627127e-05,6.120772746239398e-05,5.856040399097995e-05,5.494789343896171e-05,4.802097866477617e-05,5.184010752565395e-05,3.967241787880846e-05,5.375062980688884e-05,4.342870818880896e-05,4.845187480204066e-05,5.002922022474175e-05,6.140308398729346e-05,5.947090913092778e-05,5.651202920647864e-05,4.657807093889332e-05,4.762475656547879e-05,5.148892693251116e-05,4.571704430160849e-05,4.894777450642326e-05,5.053078419709767e-05,4.61372376022708e-05,4.605178219154033e-05,4.991917836843226e-05,4.246691902559609e-05,5.384922088264963e-05,4.375936777363036e-05,5.460229106002635e-05,5.505903308396684e-05,5.781134536672704e-05,5.192498066604328e-05,5.530538169271999e-05,5.361599989651878e-05,5.290034621824632e-05,5.237739346174289e-05,5.870461964747728e-05,4.400990969392872e-05,4.118757055599682e-05,3.231865792828157e-05,3.063952457262901e-05,2.255103435198991e-05,1.863961001235478e-05,1.080169388164616e-05,1.886229383548882e-05,1.215120351463118e-05,1.231188600156355e-05,1.513131137506731e-05,3.012194897013235e-05,3.566819219295109e-05,2.814882619329778e-05,3.070683389812842e-05,2.110927990741811e-05,2.169727161763498e-05,2.798423831302756e-05,1.480615842702192e-05,2.826509448190166e-05,2.090785136445833e-05,3.770023847643545e-05,1.125108755737249e-05,3.700109103639738e-05,2.058875113269398e-05,2.633646230627183e-05,3.253965847541557e-05,2.620356070938674e-05,2.523456394010017e-05,2.083234521669792e-05,3.551910042446706e-05,2.88338141697637e-05,3.247794586166207e-05,3.564501397301761e-05,3.417652495568283e-05,3.911376004762884e-05,3.555471381569172e-05,3.909487727782253e-05,3.905847733909284e-05,3.907169101548101e-05,5.076631737553627e-05,5.347776537887106e-05,4.950678781203764e-05,5.575518955245971e-05,5.375511747056785e-05,4.745865510401791e-05,4.50642227402869e-05,4.625375842248673e-05,4.489144768864532e-05,5.018070782657696e-05,4.837975048685555e-05,5.024485166027699e-05,4.765821619983384e-05,5.628284470493646e-05,5.466591696264946e-05,5.286137673015205e-05,5.834951033801334e-05,5.4515257728841e-05,5.953942481763125e-05,5.868298717836657e-05,5.837216419294349e-05,5.957979448896299e-05,5.830321984589218e-05,6.006052460332526e-05,5.991689202140992e-05,5.888000043931957e-05,6.028391213716166e-05,6.015730855000244e-05,5.998386919545781e-05,5.931202492643023e-05,5.930409430787493e-05,5.93394141512066e-05,5.913743470329698e-05,5.992916312757733e-05,5.866985714302187e-05,5.924224819014816e-05,5.840826495409455e-05,5.5102454044904e-05,5.764758826720601e-05,5.892050763582859e-05,5.892389268536711e-05,5.840376442256272e-05,5.841453481539232e-05,5.876833482082949e-05,5.850009316894555e-05,5.846339485687806e-05,5.877146653451514e-05,5.780822973785745e-05,5.81201215593073e-05,5.752953938946497e-05,5.84744153685973e-05,5.64469934697284e-05,5.733747944761572e-05,5.76227878935735e-05,5.668879490098315e-05,5.718689661668353e-05,5.687220362451789e-05,5.750066392768524e-05,5.746021946195883e-05,5.72428323687513e-05,5.736471104119475e-05,5.679404750331262e-05,5.720295408854998e-05,5.699398498382421e-05,5.709159408156493e-05,5.617157879412531e-05,5.656025309348942e-05,5.67972467732257e-05,5.682546114906564e-05,5.629234359305702e-05,5.607531679972909e-05,5.651706053694024e-05,5.618168890525589e-05,5.624073304802609e-05,5.631487118218113e-05,5.580271053300897e-05,5.611481789099393e-05,5.584836326217358e-05,5.443973871322774e-05,5.531698367053956e-05,5.585866719533763e-05,5.559306827873133e-05,5.528041644972295e-05,5.538208937623961e-05,5.509382132412795e-05,5.497766562923645e-05,5.479846228085896e-05,5.502099651520369e-05,5.489819779128197e-05,5.481502159898629e-05,5.430189183964693e-05,5.269838124667118e-05,5.420591052529085e-05,5.300781772095042e-05,5.403572673751552e-05,5.320861734760248e-05,5.407758907977707e-05,5.388601972481745e-05,5.290783209163775e-05,5.323120605902761e-05,5.320550895690009e-05,5.040273136801199e-05,5.203585169462033e-05,5.311120287613602e-05,5.305302490071035e-05,5.209027386549746e-05,5.368925979971728e-05,5.122684174397179e-05,5.319473534710728e-05,5.234595729724741e-05,5.229659299677839e-05,5.247787530763083e-05,5.187333875562102e-05,5.049644874450848e-05,5.12889130491233e-05,5.209756269989221e-05,5.043520178617973e-05,5.177143340351237e-05,4.839539940439427e-05,4.956507033876767e-05,5.190320504206968e-05,5.072651630245199e-05,4.871654079931582e-05,5.162340082016549e-05,5.104629611769463e-05,4.488177910571541e-05,4.748053527929585e-05,4.585247443157723e-05,4.435710366541261e-05,5.104005199210256e-05,4.440978948039673e-05,4.487537252348117e-05,4.297436601942369e-05,4.400427357438348e-05,4.155115415079868e-05,4.137063828143123e-05,4.152179453605573e-05,4.500661818855354e-05,3.539459912276607e-05,4.30047888405078e-05,3.703852201183611e-05,3.681597410539774e-05,4.275978653085835e-05,2.962348132486677e-05,3.698621740699246e-05,2.40339723595858e-05,2.686428876203956e-05,2.240655490450932e-05,1.807271916807806e-05,7.152379340318946e-06,1.955901890222918e-05,1.018468275054589e-05,1.278073747927012e-05,1.67562815253812e-05,7.371003034184689e-06,1.157583275533091e-05,9.8261176183528e-06,1.305403458883976e-05,4.671771609490895e-06,1.425281582330729e-05,9.001438804993652e-06,9.616499491299246e-06,6.413709416210689e-06,2.688766804217371e-05,2.131338818073245e-05,1.396968124023917e-05,3.806725859218719e-06,1.411391941547896e-06,1.176373959767509e-05,2.632163130162945e-05,1.860563003420039e-05,2.734350368672958e-05,2.347004675114858e-05,1.774438062221323e-05,2.064568012215309e-05,2.866488660612218e-05,1.042050304295104e-05,1.344817692142138e-05,1.452904760756594e-05,5.458774153966491e-06,2.503257725402333e-05,2.019468439874782e-05,1.125020289248953e-05,1.882835487361536e-05,2.294163159111328e-05,2.208062103864452e-05,1.322348169203982e-05,2.908937374843004e-05,2.611533951453581e-05,2.927187689682095e-05,2.902989049018159e-05,3.140575373801931e-05,2.672627299789017e-05,3.244969529498602e-05,3.271034250097017e-05,4.382685403210637e-05,3.762144539651443e-05,3.640950919523732e-05,3.515980262890274e-05,3.847675549017374e-05,3.940962656684434e-05,3.977806375489042e-05,4.316473785982811e-05,4.222031064706368e-05,4.287092135041868e-05,4.30574971742344e-05,3.181126883979175e-05,4.275102834851708e-05,4.509418714411347e-05,4.471224594874945e-05,3.410624396041748e-05,4.586537767101558e-05,4.182166376174621e-05,4.322957897030407e-05,3.072189893684439e-05,4.173865806850071e-05,3.997900331944217e-05,3.88272058326677e-05,4.551197898173895e-05,4.350743692946575e-05,3.201099721769466e-05,3.975003676715753e-05,4.425287566586576e-05,4.277761654945395e-05,4.537889482219166e-05,4.35920728188183e-05,4.502675637825286e-05,4.295588456577791e-05,4.148650123267054e-05,4.59340968306421e-05,4.180734505849513e-05,3.51857852365152e-05,4.326011277661894e-05,4.221726016169908e-05,4.226111219570649e-05,4.199828067170222e-05,3.509818491556394e-05,4.23423614270389e-05,4.663930422512842e-05,4.172731183925638e-05,4.211163117467397e-05,4.028156836030324e-05,4.411788384713448e-05,4.113124876834374e-05,4.141572160810753e-05,4.580764846195778e-05,4.238035215407631e-05,4.180258716990643e-05,4.5611905901473e-05,4.456103339726874e-05,4.499535238338948e-05,4.378624469701543e-05,4.494266495992375e-05,4.569241925247096e-05,4.436180847410833e-05,4.367714219396349e-05,4.410858038952898e-05,4.555147524755898e-05,4.616349767296019e-05,4.273253724398166e-05,4.607980033262439e-05,4.6179594552626e-05,4.550691226468202e-05,4.673193426805969e-05,4.620512678538896e-05,4.501697761433296e-05,4.66602370047408e-05,4.618951164596395e-05,4.66285048796299e-05,4.610016290550767e-05,4.659343837215109e-05,4.610793589286564e-05,4.595068429719757e-05,4.610750884099941e-05,4.619460570720818e-05,4.573896147196335e-05,4.55496512294185e-05,4.571342923920041e-05,4.604075122469064e-05,4.58781273004606e-05,4.60293390477005e-05,4.617269818774296e-05,4.594728235860218e-05,4.553431114034802e-05,4.540859704351655e-05,4.511836664384631e-05,4.474088255101077e-05,4.549015188635399e-05,4.446879662808999e-05,4.400783475265779e-05,4.501815743559051e-05,4.326073606324103e-05,4.368523446492014e-05,4.172811929702227e-05,4.015860155005377e-05,4.064954471836939e-05,3.776318479558026e-05,4.025711783141991e-05,3.922699152296178e-05,3.955857357198388e-05,3.778377014316589e-05,2.515937707593843e-05,3.957257218739549e-05,4.173090920836681e-05,4.181898403139163e-05,4.159181576154182e-05,4.161321741354216e-05,4.228060779700445e-05,4.278582623956782e-05,4.313567822690456e-05,4.395265579118534e-05,4.367125997673262e-05,4.344598891093634e-05,4.25846590748689e-05,3.846282443098957e-05,4.20299774102178e-05,4.345164433226084e-05,4.381722244425337e-05,4.417711135680769e-05,4.369289968401055e-05,4.349481597854916e-05,4.243697553203038e-05,4.283197518530769e-05,4.338535397985842e-05,4.116623646022389e-05,4.290246769590412e-05,4.206563342620499e-05,4.219500038476226e-05,4.060472839963959e-05,3.873031492196379e-05,4.090331244852734e-05,4.267844400759281e-05,3.691915659190106e-05,3.790598257554243e-05,4.102726847496413e-05,3.628023794133556e-05,3.152692146159318e-05,4.028322348787518e-05,4.038866589103407e-05,3.21586606545131e-05,3.649835206822872e-05,4.043933225736265e-05,3.172676886713488e-05,3.517976549410708e-05,3.517600003866889e-05,3.310671418905685e-05,3.046991903399081e-05,3.022659839185979e-05,3.431165027838735e-05,3.30645824261264e-05,3.532732598810277e-05,2.848761263143035e-05,2.746565982224995e-05,3.172970112910147e-05,3.212690601065974e-05,2.476910233737693e-05,2.795032428261899e-05,3.433850870423395e-05,2.991424011074437e-05,2.841493339009138e-05,2.504534538100682e-05,1.898145899946399e-05,2.451936385364045e-05,1.550003648132077e-05,1.561773551431263e-05,2.176696390863276e-05,1.815810863106272e-05,2.481983223872892e-05,1.971429689096747e-05,1.769249180986456e-05,1.915842494992839e-05,1.904028760569905e-05,1.813847711306909e-05,1.837633856863147e-05,1.920922401598941e-05,1.372909260411488e-05,8.176465317804397e-06,1.179489910333446e-05,6.298681749469031e-06,6.512765584427675e-06,5.144241688265086e-07,1.753123589923988e-06,1.739874446516416e-06,5.030413466256556e-07,1.648832618322302e-07,1.045656906089945e-08,3.158911983679152e-08,3.9267917728929e-10,5.242276390238578e-09,7.834399346526627e-09,4.581388615362344e-10,8.026612817945118e-11,2.341099939141518e-10,5.268502119845691e-13,1.980001609268123e-15,3.459873609651909e-10,1.490692175719077e-10,9.963969317378439e-16,1.405210225042111e-09,5.471040112992777e-10,1.629398300173493e-17,5.688565937738767e-11,3.217284907075413e-11,2.175567960593023e-12,3.034179864867771e-10,4.902858864348141e-09,1.979876630247386e-08,3.575373124472504e-08,2.849364685017292e-08,1.358828371165775e-08,1.228931578767689e-07,5.785238336216584e-09,9.054952022915587e-09,2.634033070453276e-10,2.853342138331069e-10,4.895856983071775e-12,6.86641302538456e-11,2.327884252151338e-10,2.810659952995262e-10,2.219362973927511e-08,4.494391635861272e-10,6.490072241274131e-08,5.514351053788125e-08,3.84653449216652e-08,2.662402503919956e-09,1.297988197835027e-08,8.46730806642181e-09,7.532094718837461e-11,7.097275494937455e-13,5.511673655731896e-09,1.428347106998337e-07,9.139004355141695e-08,3.65546746601226e-13,1.186233308615829e-12,2.069384449534451e-07,2.68547263388956e-07,8.343545379473988e-08,4.118020129752178e-11,2.31218330023269e-07,1.975376179139621e-08,1.867619573070989e-07,7.016508084269929e-08,5.290354709664103e-08,2.399159852017373e-07,2.997498120160823e-07,2.653816831230853e-06,4.136893409517032e-08,2.090052151378263e-08,4.050159899302921e-06,1.340066478752094e-06,1.54628660799021e-06,2.44699899022818e-07,9.446577081784792e-07,1.047251627135188e-06,5.296609933779255e-06,1.055145869878994e-06,1.944043037890954e-06,2.962521526803736e-06,3.187318251374593e-06,5.686154743388227e-06,5.235580603011712e-07,4.369486926973634e-06,7.084511389157986e-06,5.772296493219719e-06,2.901524526516464e-07,4.129786333543673e-06,2.417508284234392e-06,2.471589617859346e-06,4.42911784383346e-06,3.453213771988926e-06,1.53386366115924e-06,5.90675630666002e-06,4.58621856392697e-06,3.685336969424115e-06,4.211737827944999e-06,5.229648924971483e-06,7.175935392581536e-06,5.781702813223885e-06,2.685791917488226e-06,4.214471522857416e-06,1.347257115344853e-05,1.190166769957698e-05,3.196648088078423e-06,1.31527318243865e-06,7.2822534531264e-06,9.579636631563531e-06,1.60893085428955e-05,7.740676983737154e-06,1.036417916427186e-05,1.370981253935203e-05,1.599755110123516e-05,1.913442720861697e-05,1.003006182654339e-05,1.060739219898349e-05,1.535594869911107e-05,5.085872062256116e-06,1.787777119750635e-05,1.100250436554907e-05,7.686837244049327e-06,4.25372756194969e-06,9.08396870938027e-06,1.120527036096372e-05,5.873101965606633e-06,2.111486616403359e-06,5.536949576951032e-06,8.315982921228726e-06,1.153906093565407e-05,2.190182946155801e-05,8.164357311671763e-06,8.283686058226197e-06,7.545663869660422e-06,1.427485523826417e-05,7.217478933788898e-06,1.373196856922529e-05,6.971334602199634e-06,1.772216749124297e-05,1.640695309880699e-05,1.493230279268282e-05,1.474755661669321e-05,7.250658933616858e-06,1.127061774102498e-05,2.272044365587225e-05,2.09442159165927e-05,2.371625542200206e-05,1.97280043712085e-05,2.180168217984403e-05,2.447167880796745e-05,2.194631202035472e-05,2.027538674633441e-05,2.751022280512692e-05,2.285174963900481e-05,2.623171396292566e-05,3.023261813426792e-05,3.205265689127392e-05,2.821333997776705e-05,2.235385622167234e-05,1.938832844274816e-05,2.227345707286837e-05,3.121591350078548e-05,3.092273555857338e-05,2.947334726030247e-05,2.268217224879471e-05,3.285204651344069e-05,3.217141269668052e-05,3.169900325766285e-05,2.949441113116568e-05,2.748291400443084e-05,3.237720263751328e-05,3.131345986774358e-05,3.041421007782938e-05,3.077853518265132e-05,2.985326016036212e-05,3.233369723129185e-05,3.364549842576122e-05,3.228810964563224e-05,3.430094422482196e-05,3.375353289702717e-05,3.174587762860675e-05,3.282337532882484e-05,3.220014500359738e-05,3.43201591460798e-05,3.350151599909666e-05,3.140452566231361e-05,3.321165715867727e-05,3.430034586966478e-05,3.416862248555561e-05,3.317680538349276e-05,3.294412404294051e-05,3.392666020614033e-05,3.379052475698763e-05,3.364676188806223e-05,3.378374741974338e-05,3.280992038019585e-05,3.33430709100774e-05,3.339323140894108e-05,3.376359234098718e-05,3.378795762034545e-05,3.442490427246277e-05,3.416867395696699e-05,3.397677968872308e-05,3.320943504133944e-05,3.406181608999536e-05,3.364501186007558e-05,3.37515399883181e-05,3.392807566995306e-05,3.388748724512298e-05,3.308694595012675e-05,3.346465683886865e-05,3.292429950715422e-05,3.388711568587213e-05,3.364073651596849e-05,3.36121763165834e-05,3.333262864749528e-05,3.389884795070175e-05,3.361153292394126e-05,3.35211756655184e-05,3.303571581099549e-05,3.364084589271764e-05,3.305403159103592e-05,3.315453434718471e-05,3.243671726115304e-05,3.211670341183684e-05,3.052475860584454e-05,2.970020831016566e-05,3.005793703192396e-05,2.961151180900035e-05,3.056455244076158e-05,3.036736868075839e-05,3.127895793730825e-05,2.739755188563346e-05,2.984396715788706e-05,3.006098349608455e-05,3.108641625521817e-05,3.162232211408971e-05,3.078351504170158e-05,3.151591703469e-05,3.172563971304791e-05,3.298214854809162e-05,3.261392207113584e-05,3.229498188329121e-05,3.206501324696642e-05,2.96903483179247e-05,3.091872400544957e-05,3.096120159192518e-05,3.22968630025287e-05,3.309609258077574e-05,3.28489389269791e-05,3.312481684528456e-05,3.138581258731665e-05,3.171372729827847e-05,3.267047950134411e-05,3.112331321476392e-05,3.063835761922431e-05,2.874286096890604e-05,2.88767694752761e-05,2.887416775627941e-05,2.946623133768028e-05,3.057017006276835e-05,3.117948300090529e-05,3.010809913926924e-05,2.973110965452737e-05,2.940927098282986e-05,2.817545058507078e-05,2.938493224341809e-05,2.991656114970093e-05,3.076924539713947e-05,3.094278849874762e-05,3.130745379742911e-05,2.995700481118654e-05,3.051523237353669e-05,3.168832293980315e-05,3.137978721522291e-05,3.055100098323628e-05,3.054508981333651e-05,3.098658423589883e-05,3.164788732072557e-05,3.169742694568958e-05,3.108048900050235e-05,3.134676991330934e-05,3.150605784668983e-05,3.158826895002227e-05,3.162208325457131e-05,3.100439173575195e-05,3.122672893110004e-05,3.126556250249866e-05,3.055713814480159e-05,3.059556235763165e-05,3.072605605755348e-05,3.097115568034005e-05,2.988550780382752e-05,2.899084299072945e-05,2.903358678091075e-05,2.837203920687998e-05,2.898191109237478e-05,2.916068095495962e-05,2.845565210193151e-05,2.955715236890583e-05,2.886998489986462e-05,2.879089907629143e-05,3.015814221897574e-05,2.870129539150069e-05,2.899986415981321e-05,2.989194173024902e-05,2.769130164305627e-05,2.972489769856741e-05,2.961526761354891e-05,2.871001497028344e-05,2.958987290596322e-05,2.943461502324498e-05,2.961497004445191e-05,2.998486853803648e-05,2.951328907552719e-05,2.981410730536483e-05,2.990153149758029e-05,2.92832890738111e-05,2.973825533405925e-05,2.957279646099973e-05,2.835863251269916e-05,2.396214883046087e-05,2.824522330014884e-05,2.878668324600375e-05,2.888045128967081e-05,2.977344489038089e-05,2.940289013630133e-05,2.843617258544958e-05,2.910170838962088e-05,2.904640316234239e-05,2.877412743859218e-05,2.850150589129679e-05,2.863180335646278e-05,2.822512853945286e-05,2.876587351523417e-05,2.777641846840882e-05,2.629095916589651e-05,2.75497608914687e-05,2.82970501859557e-05,2.681189890767082e-05,2.889306258969776e-05,2.851020455981867e-05,2.779175373203448e-05,2.852637623387913e-05,2.814255874472243e-05,2.789418344914651e-05,2.625152402237748e-05,2.817893777319124e-05,2.877562493496678e-05,2.789753552481212e-05,2.858332935056233e-05,2.853744902125055e-05,2.471237279963689e-05,2.832119671181562e-05,2.808099169855421e-05,2.73100070572976e-05,2.79184087906051e-05,2.712019818545506e-05,2.584098080710663e-05,2.615791200142613e-05,2.586483458931438e-05,2.470531236963008e-05,2.421899599865232e-05,2.254060978270546e-05,2.35347559661329e-05,2.172603850690634e-05,2.33153429903434e-05,2.159648335600124e-05,2.264459007608507e-05,1.885643896244525e-05,2.017393016059364e-05,1.639372494608437e-05,1.438706371929609e-05,1.105116012987093e-05,1.279854015367844e-05,6.775016607420541e-06,4.607527728235007e-06,2.150626362275563e-06,1.410710025771296e-06,4.790141861856688e-07,1.445494968545102e-07,1.870487174077055e-07,7.65918969712714e-10,9.47304384236047e-10,9.278809233380743e-12,9.297346179641911e-10,4.462494963082159e-10,4.236304650048405e-11,1.668064589485155e-09,2.547145628549531e-09,4.009778968599927e-14,6.805385142250464e-14,1.17185444815272e-08,6.653697284455371e-09,3.394649760977944e-08,1.973169824921524e-08,1.317506478723636e-10,8.681830534314238e-11,3.53994229591006e-09,3.07207963227039e-09,6.959295117383387e-08,1.449313302816067e-07,8.574578991469695e-08,5.592226092832863e-07,5.120821552698153e-07,1.699242994803385e-06,2.62324450178153e-06,1.577951016025504e-06,3.45306900864444e-06,4.513905654273629e-06,7.739095846319068e-06,1.077824020923775e-05,1.202450663553883e-05,1.326032677805379e-05,1.370184010027498e-05,1.302661399867209e-05,6.137322413477125e-06,2.418915464366857e-06,6.425359648478434e-06,4.318428895374147e-06,7.307462220238512e-06,1.205317701591388e-05,1.385366548324733e-05,1.577482224061617e-05,1.472993087526149e-05,1.497868979370029e-05,1.119908132586663e-05,9.074396152802191e-06,1.146345377524883e-05,1.027593553110255e-05,1.093359902417672e-05,1.292368525014199e-05,1.452209253310429e-05,1.427026141479921e-05,1.497649180358655e-05,1.512133275730795e-05,1.454705134217493e-05,1.577012185524486e-05,1.521381843901513e-05,1.559329584268013e-05,1.493367080628819e-05,1.51473125500776e-05,1.537858164378034e-05,1.546104206176161e-05,1.562168433665383e-05,1.54371987346843e-05,1.46350795192332e-05,1.470395068037144e-05,1.46216768462564e-05,1.328695478891041e-05,1.430996276202393e-05,1.407215519059534e-05,1.43429462858238e-05,1.310041917713482e-05,1.392614688134883e-05,1.394452539217188e-05,1.259798179926717e-05,1.312457052843956e-05,1.409722739761916e-05,1.358722171167781e-05,1.387802754564237e-05,1.350182983597074e-05,1.358956165029323e-05,1.335508323366736e-05,1.31722032984604e-05,1.278994684070171e-05,1.301730089017695e-05,1.227600801511481e-05,1.21649093863906e-05,1.24118728372374e-05,1.184229220959609e-05,1.171358834758063e-05,1.215502526692556e-05,1.159214999697666e-05,1.164329971202766e-05,1.130788103225635e-05,1.088099202479125e-05,1.096897234952177e-05,1.186574467564329e-05,1.082479288386058e-05,9.708145143488016e-06,1.051141723812976e-05,1.064814179367044e-05,1.088563611330638e-05,8.625984455095944e-06,9.693755667046314e-06,7.850162305411162e-06,8.991324913931281e-06,9.535024268301272e-06,9.397737548439523e-06,5.873876449499623e-06,8.432394445119571e-06,8.144849003369105e-06,5.912779185607275e-06,7.132852695325991e-06,7.819040599069522e-06,8.52173554528824e-06,6.498715658452865e-06,6.553704416975493e-06,5.302319400085701e-06,5.175112632324447e-06,6.451149238298251e-06,8.813720798389949e-06,2.913597950294584e-06,8.486956956016777e-06,4.089653752400548e-06,2.681897783521609e-06,4.907004082293359e-06,6.60064393142441e-06,4.787228901669349e-06,3.322776368923271e-06,3.275361146039563e-06,1.603492095437288e-06,1.121220010184009e-06,7.03158751889626e-07,5.773334285551509e-07,1.420329469588174e-06,3.060414119427392e-07,4.473921616406761e-07,1.049358923013616e-07,7.509685353111345e-08,8.405709735286363e-09,1.293945359743991e-10,3.568221011014194e-11,7.704517513007473e-11,1.100314896455243e-14,5.787807403036691e-17,2.144220584282149e-13,6.386572723046371e-15,3.291321304768917e-18,3.153674285027561e-22,2.233694384183261e-31,7.92918057275692e-26,3.574568079429013e-38,1.141329247214434e-34,4.76630175174259e-37,9.391216361890923e-32,1.216237803846414e-38,1.247833248232878e-37,2.354619227034713e-41,1.190623015765063e-32,8.167336782573479e-32,5.927928669607519e-49,8.270502380019963e-20,2.494754969939989e-20,1.914239964769401e-22,3.046604902724827e-23,2.804236079583786e-31,5.57667649903328e-29,2.383994524473315e-41,0,0,0,0,2.212300774590942e-33,1.545030062160089e-36,0,6.377394324885687e-46,2.451929147196821e-39,8.418974078845108e-30,1.226157108846574e-48,1.598411505226504e-25,1.333461972856335e-22,1.207315677017507e-24,5.137519200243572e-31,2.902164863043563e-27,3.681975242868877e-32,1.49031297618061e-47,0,5.954470626698249e-31,1.866651508416793e-27,8.924841141615824e-42,1.074676906026735e-37,8.705248015886521e-31,2.7307433486729e-20,8.138351944044585e-20,3.711989509625214e-16,1.522233132791159e-17,9.092322680294117e-14,6.494105750171854e-14,4.660202283847899e-15,3.999821261101438e-11,8.878226540451192e-10,4.850976244653658e-14,4.478781643577408e-11,9.283824076905906e-09,2.651027000310408e-10,1.03019454829023e-10,5.832206320789918e-09,3.862446476871794e-08,1.457125336065023e-09,9.056857269377155e-08,5.726606286433696e-08,1.051808801346767e-07,4.328461799387687e-08,6.20322874089625e-07,1.892706738973736e-07,2.592380152496751e-08,6.370407482912332e-07,2.949441756509211e-07,6.798099524818907e-07,2.548830110910762e-07,1.38694495132409e-06,1.532000757975933e-06,3.847698711152491e-07,3.431703949600617e-07,1.240253519939779e-06,5.551815405220169e-07,1.094363916635748e-06,1.773622280563115e-06,8.415737411734686e-08,2.043988254103271e-07,3.206940761871232e-07,1.671530706496582e-06,2.472011040039955e-06,1.029840199792565e-06,1.893311528057358e-06,6.985839085076124e-07,1.657715538412078e-06,1.346992882029129e-06,1.539110849852302e-07,1.825375497912447e-06,1.480459257017908e-06,6.09875987122901e-07,4.948950467718786e-07,1.030747584478199e-06,2.531673643987408e-07,7.112149526462778e-08,1.5507107366458e-06,7.176348852778198e-07,4.318808497033016e-07,1.489289700395309e-06,8.972908201670114e-07,4.384321550699626e-07,5.915790263172542e-07,1.630625973758798e-07,1.097233769516062e-06,2.301264886883349e-07,2.115230437763954e-07,5.681064944620252e-07,2.46398986397026e-06,7.612390522698293e-07,1.450302076670933e-06,2.885874161344303e-06,8.394403315961767e-07,8.224646177932267e-07,1.690864816241376e-06,1.430219460011077e-06,2.346221344573039e-06,3.567918214351983e-06,3.190883290004751e-06,2.356898847589934e-06,2.716305617783034e-06,2.070286767503028e-06,1.087476076705202e-06,6.919025574031565e-07,1.128330544392819e-07,7.983574997326362e-08,3.519771132337827e-08,1.286404717553903e-07,4.166496548375035e-07,5.154932219982985e-08,8.852954077467505e-08,1.897693836191208e-06,9.762145087943742e-07,1.915799749594176e-07,6.81334712619708e-07,2.601521073036029e-06,3.211211280533509e-07,6.424132779133933e-07,3.204756443851129e-07,1.560974095861351e-06,7.556028925125471e-07,2.93994085778665e-06,2.317086836830762e-06,3.24197751244036e-07,4.722518078203421e-07,1.047683528573456e-06,1.044450239274406e-06,4.30115179233039e-09,1.60170056862522e-08,9.409358023797568e-07,1.248433292295764e-06,2.432542842223933e-06,9.294665645046552e-07,9.525408765264329e-07,2.162828303733955e-06,9.796725833977744e-07,1.41603257182757e-06,1.945997785373929e-06,1.067556720928292e-06,2.295222826792951e-06,1.389476379674632e-06,2.038935088503858e-06,2.686898391984566e-06,2.606573997363201e-06,3.420484388282711e-06,1.221179903790976e-06,1.941717334337739e-06,1.998725058971436e-06,3.621037917249162e-06,2.756177464057926e-06,2.396955749673525e-06,3.191593836753927e-06,2.222898416496129e-06,3.135775905963728e-06,3.094545696973094e-06,2.308754138086146e-06,3.486689491160035e-06,2.735948676632181e-06,3.422533593847961e-06,3.058280468577859e-06,3.141325971743081e-06,3.389681161298935e-06,2.924405338201114e-06,3.447472699018933e-06,3.35444817597395e-06,3.328796513451797e-06,3.3770175856198e-06,3.24924624081506e-06,3.431650467587238e-06,3.239779522326613e-06,3.158921956265105e-06,2.688218794534419e-06,2.571136935934535e-06,2.720798428603173e-06,3.008656800449967e-06,2.589779680073297e-06,3.090713489548284e-06,3.111110242665669e-06,2.393841407589194e-06,2.485404062127128e-06,2.933022778401922e-06,2.643061276644058e-06,2.729091196791937e-06,2.7958345780385e-06,2.971122882188491e-06,3.003372536255901e-06,2.751959784016386e-06,2.753997891058559e-06,3.381243871037929e-06,2.98505032228905e-06,2.906256840247643e-06,3.010825435774416e-06,3.360697127010841e-06,3.107052043575303e-06,2.971585320650037e-06,3.226983246915034e-06,3.212559188118814e-06,3.022115368162559e-06,2.331823906147389e-06,1.427133748899321e-06,2.465707078932161e-06,2.797071500393035e-06,2.876304339184951e-06,3.010895806844652e-06,3.236956637109175e-06,3.209150011356218e-06,2.79396793513546e-06,2.756323112067292e-06,3.104266555555191e-06,3.204903619918021e-06,2.781041453137927e-06,2.578405624097193e-06,2.661776161182822e-06,3.111575093849624e-06,2.801864373456658e-06,2.715455454830512e-06,2.680213542432618e-06,2.588972021247196e-06,2.766476652201237e-06,2.748225734181544e-06,2.910707348001561e-06,2.682509448864094e-06,2.364207064188046e-06,2.706963074074522e-06,3.01308495030957e-06,2.847426183198532e-06,2.526428465896353e-06,2.379955506526093e-06,2.966208970884064e-06,2.924132700569002e-06,2.954722401619664e-06,2.372292096977473e-06,2.771920799466877e-06,2.715075491263283e-06,2.733251775736485e-06,2.637931346260028e-06,2.481632977003321e-06,2.517454545959753e-06,2.290859659590205e-06,2.107332069264829e-06,2.038904849049677e-06,2.115801086825502e-06,2.152968874461554e-06,2.341870401830494e-06,2.485832722474962e-06,2.48949077155395e-06,2.243753265174727e-06,2.199865764147931e-06,2.190001750702956e-06,2.162933257158706e-06,2.228332993296218e-06,2.327342877455008e-06,2.345700035684736e-06,2.392619122417268e-06,2.423130490413747e-06,2.4555244654932e-06,2.467641760607109e-06,2.489093154901101e-06,2.452289607924586e-06,2.400743844490309e-06,2.364552887733202e-06,2.382105724736161e-06,2.365712683394759e-06,2.316531186860184e-06,2.285427173816204e-06]
    return np.interp(wavelength,wavelength_list,current_density)

def am1_5(wavelength):
    wavelength_list = [280,280.5,281,281.5,282,282.5,283,283.5,284,284.5,285,285.5,286,286.5,287,287.5,288,288.5,289,289.5,290,290.5,291,291.5,292,292.5,293,293.5,294,294.5,295,295.5,296,296.5,297,297.5,298,298.5,299,299.5,300,300.5,301,301.5,302,302.5,303,303.5,304,304.5,305,305.5,306,306.5,307,307.5,308,308.5,309,309.5,310,310.5,311,311.5,312,312.5,313,313.5,314,314.5,315,315.5,316,316.5,317,317.5,318,318.5,319,319.5,320,320.5,321,321.5,322,322.5,323,323.5,324,324.5,325,325.5,326,326.5,327,327.5,328,328.5,329,329.5,330,330.5,331,331.5,332,332.5,333,333.5,334,334.5,335,335.5,336,336.5,337,337.5,338,338.5,339,339.5,340,340.5,341,341.5,342,342.5,343,343.5,344,344.5,345,345.5,346,346.5,347,347.5,348,348.5,349,349.5,350,350.5,351,351.5,352,352.5,353,353.5,354,354.5,355,355.5,356,356.5,357,357.5,358,358.5,359,359.5,360,360.5,361,361.5,362,362.5,363,363.5,364,364.5,365,365.5,366,366.5,367,367.5,368,368.5,369,369.5,370,370.5,371,371.5,372,372.5,373,373.5,374,374.5,375,375.5,376,376.5,377,377.5,378,378.5,379,379.5,380,380.5,381,381.5,382,382.5,383,383.5,384,384.5,385,385.5,386,386.5,387,387.5,388,388.5,389,389.5,390,390.5,391,391.5,392,392.5,393,393.5,394,394.5,395,395.5,396,396.5,397,397.5,398,398.5,399,399.5,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,586,587,588,589,590,591,592,593,594,595,596,597,598,599,600,601,602,603,604,605,606,607,608,609,610,611,612,613,614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,629,630,631,632,633,634,635,636,637,638,639,640,641,642,643,644,645,646,647,648,649,650,651,652,653,654,655,656,657,658,659,660,661,662,663,664,665,666,667,668,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691,692,693,694,695,696,697,698,699,700,701,702,703,704,705,706,707,708,709,710,711,712,713,714,715,716,717,718,719,720,721,722,723,724,725,726,727,728,729,730,731,732,733,734,735,736,737,738,739,740,741,742,743,744,745,746,747,748,749,750,751,752,753,754,755,756,757,758,759,760,761,762,763,764,765,766,767,768,769,770,771,772,773,774,775,776,777,778,779,780,781,782,783,784,785,786,787,788,789,790,791,792,793,794,795,796,797,798,799,800,801,802,803,804,805,806,807,808,809,810,811,812,813,814,815,816,817,818,819,820,821,822,823,824,825,826,827,828,829,830,831,832,833,834,835,836,837,838,839,840,841,842,843,844,845,846,847,848,849,850,851,852,853,854,855,856,857,858,859,860,861,862,863,864,865,866,867,868,869,870,871,872,873,874,875,876,877,878,879,880,881,882,883,884,885,886,887,888,889,890,891,892,893,894,895,896,897,898,899,900,901,902,903,904,905,906,907,908,909,910,911,912,913,914,915,916,917,918,919,920,921,922,923,924,925,926,927,928,929,930,931,932,933,934,935,936,937,938,939,940,941,942,943,944,945,946,947,948,949,950,951,952,953,954,955,956,957,958,959,960,961,962,963,964,965,966,967,968,969,970,971,972,973,974,975,976,977,978,979,980,981,982,983,984,985,986,987,988,989,990,991,992,993,994,995,996,997,998,999,1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019,1020,1021,1022,1023,1024,1025,1026,1027,1028,1029,1030,1031,1032,1033,1034,1035,1036,1037,1038,1039,1040,1041,1042,1043,1044,1045,1046,1047,1048,1049,1050,1051,1052,1053,1054,1055,1056,1057,1058,1059,1060,1061,1062,1063,1064,1065,1066,1067,1068,1069,1070,1071,1072,1073,1074,1075,1076,1077,1078,1079,1080,1081,1082,1083,1084,1085,1086,1087,1088,1089,1090,1091,1092,1093,1094,1095,1096,1097,1098,1099,1100,1101,1102,1103,1104,1105,1106,1107,1108,1109,1110,1111,1112,1113,1114,1115,1116,1117,1118,1119,1120,1121,1122,1123,1124,1125,1126,1127,1128,1129,1130,1131,1132,1133,1134,1135,1136,1137,1138,1139,1140,1141,1142,1143,1144,1145,1146,1147,1148,1149,1150,1151,1152,1153,1154,1155,1156,1157,1158,1159,1160,1161,1162,1163,1164,1165,1166,1167,1168,1169,1170,1171,1172,1173,1174,1175,1176,1177,1178,1179,1180,1181,1182,1183,1184,1185,1186,1187,1188,1189,1190,1191,1192,1193,1194,1195,1196,1197,1198,1199,1200,1201,1202,1203,1204,1205,1206,1207,1208,1209,1210,1211,1212,1213,1214,1215,1216,1217,1218,1219,1220,1221,1222,1223,1224,1225,1226,1227,1228,1229,1230,1231,1232,1233,1234,1235,1236,1237,1238,1239,1240,1241,1242,1243,1244,1245,1246,1247,1248,1249,1250,1251,1252,1253,1254,1255,1256,1257,1258,1259,1260,1261,1262,1263,1264,1265,1266,1267,1268,1269,1270,1271,1272,1273,1274,1275,1276,1277,1278,1279,1280,1281,1282,1283,1284,1285,1286,1287,1288,1289,1290,1291,1292,1293,1294,1295,1296,1297,1298,1299,1300,1301,1302,1303,1304,1305,1306,1307,1308,1309,1310,1311,1312,1313,1314,1315,1316,1317,1318,1319,1320,1321,1322,1323,1324,1325,1326,1327,1328,1329,1330,1331,1332,1333,1334,1335,1336,1337,1338,1339,1340,1341,1342,1343,1344,1345,1346,1347,1348,1349,1350,1351,1352,1353,1354,1355,1356,1357,1358,1359,1360,1361,1362,1363,1364,1365,1366,1367,1368,1369,1370,1371,1372,1373,1374,1375,1376,1377,1378,1379,1380,1381,1382,1383,1384,1385,1386,1387,1388,1389,1390,1391,1392,1393,1394,1395,1396,1397,1398,1399,1400,1401,1402,1403,1404,1405,1406,1407,1408,1409,1410,1411,1412,1413,1414,1415,1416,1417,1418,1419,1420,1421,1422,1423,1424,1425,1426,1427,1428,1429,1430,1431,1432,1433,1434,1435,1436,1437,1438,1439,1440,1441,1442,1443,1444,1445,1446,1447,1448,1449,1450,1451,1452,1453,1454,1455,1456,1457,1458,1459,1460,1461,1462,1463,1464,1465,1466,1467,1468,1469,1470,1471,1472,1473,1474,1475,1476,1477,1478,1479,1480,1481,1482,1483,1484,1485,1486,1487,1488,1489,1490,1491,1492,1493,1494,1495,1496,1497,1498,1499,1500,1501,1502,1503,1504,1505,1506,1507,1508,1509,1510,1511,1512,1513,1514,1515,1516,1517,1518,1519,1520,1521,1522,1523,1524,1525,1526,1527,1528,1529,1530,1531,1532,1533,1534,1535,1536,1537,1538,1539,1540,1541,1542,1543,1544,1545,1546,1547,1548,1549,1550,1551,1552,1553,1554,1555,1556,1557,1558,1559,1560,1561,1562,1563,1564,1565,1566,1567,1568,1569,1570,1571,1572,1573,1574,1575,1576,1577,1578,1579,1580,1581,1582,1583,1584,1585,1586,1587,1588,1589,1590,1591,1592,1593,1594,1595,1596,1597,1598,1599,1600,1601,1602,1603,1604,1605,1606,1607,1608,1609,1610,1611,1612,1613,1614,1615,1616,1617,1618,1619,1620,1621,1622,1623,1624,1625,1626,1627,1628,1629,1630,1631,1632,1633,1634,1635,1636,1637,1638,1639,1640,1641,1642,1643,1644,1645,1646,1647,1648,1649,1650,1651,1652,1653,1654,1655,1656,1657,1658,1659,1660,1661,1662,1663,1664,1665,1666,1667,1668,1669,1670,1671,1672,1673,1674,1675,1676,1677,1678,1679,1680,1681,1682,1683,1684,1685,1686,1687,1688,1689,1690,1691,1692,1693,1694,1695,1696,1697,1698,1699,1700,1702,1705,1710,1715,1720,1725,1730,1735,1740,1745,1750,1755,1760,1765,1770,1775,1780,1785,1790,1795,1800,1805,1810,1815,1820,1825,1830,1835,1840,1845,1850,1855,1860,1865,1870,1875,1880,1885,1890,1895,1900,1905,1910,1915,1920,1925,1930,1935,1940,1945,1950,1955,1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010,2015,2020,2025,2030,2035,2040,2045,2050,2055,2060,2065,2070,2075,2080,2085,2090,2095,2100,2105,2110,2115,2120,2125,2130,2135,2140,2145,2150,2155,2160,2165,2170,2175,2180,2185,2190,2195,2200,2205,2210,2215,2220,2225,2230,2235,2240,2245,2250,2255,2260,2265,2270,2275,2280,2285,2290,2295,2300,2305,2310,2315,2320,2325,2330,2335,2340,2345,2350,2355,2360,2365,2370,2375,2380,2385,2390,2395,2400,2405,2410,2415,2420,2425,2430,2435,2440,2445,2450,2455,2460,2465,2470,2475,2480,2485,2490,2495,2500,2505,2510,2515,2520,2525,2530,2535,2540,2545,2550,2555,2560,2565,2570,2575,2580,2585,2590,2595,2600,2605,2610,2615,2620,2625,2630,2635,2640,2645,2650,2655,2660,2665,2670,2675,2680,2685,2690,2695,2700,2705,2710,2715,2720,2725,2730,2735,2740,2745,2750,2755,2760,2765,2770,2775,2780,2785,2790,2795,2800,2805,2810,2815,2820,2825,2830,2835,2840,2845,2850,2855,2860,2865,2870,2875,2880,2885,2890,2895,2900,2905,2910,2915,2920,2925,2930,2935,2940,2945,2950,2955,2960,2965,2970,2975,2980,2985,2990,2995,3000,3005,3010,3015,3020,3025,3030,3035,3040,3045,3050,3055,3060,3065,3070,3075,3080,3085,3090,3095,3100,3105,3110,3115,3120,3125,3130,3135,3140,3145,3150,3155,3160,3165,3170,3175,3180,3185,3190,3195,3200,3205,3210,3215,3220,3225,3230,3235,3240,3245,3250,3255,3260,3265,3270,3275,3280,3285,3290,3295,3300,3305,3310,3315,3320,3325,3330,3335,3340,3345,3350,3355,3360,3365,3370,3375,3380,3385,3390,3395,3400,3405,3410,3415,3420,3425,3430,3435,3440,3445,3450,3455,3460,3465,3470,3475,3480,3485,3490,3495,3500,3505,3510,3515,3520,3525,3530,3535,3540,3545,3550,3555,3560,3565,3570,3575,3580,3585,3590,3595,3600,3605,3610,3615,3620,3625,3630,3635,3640,3645,3650,3655,3660,3665,3670,3675,3680,3685,3690,3695,3700,3705,3710,3715,3720,3725,3730,3735,3740,3745,3750,3755,3760,3765,3770,3775,3780,3785,3790,3795,3800,3805,3810,3815,3820,3825,3830,3835,3840,3845,3850,3855,3860,3865,3870,3875,3880,3885,3890,3895,3900,3905,3910,3915,3920,3925,3930,3935,3940,3945,3950,3955,3960,3965,3970,3975,3980,3985,3990,3995,4000]
    spectrum = [4.7309e-23,1.2307e-21,5.6895e-21,1.5662e-19,1.1946e-18,4.5436e-18,1.8452e-17,3.536e-17,7.267e-16,2.4856e-15,8.0142e-15,4.2613e-14,1.3684e-13,8.3823e-13,2.7367e-12,1.0903e-11,6.2337e-11,1.7162e-10,5.6265e-10,2.0749e-09,6.0168e-09,1.3783e-08,3.5052e-08,1.0913e-07,2.683e-07,4.2685e-07,8.6466e-07,2.2707e-06,4.1744e-06,6.5911e-06,1.229e-05,2.7826e-05,4.7904e-05,7.1345e-05,9.679999999999999e-05,0.00018608,0.00028988,0.00035789,0.00049211,0.00086068,0.0010205,0.001245,0.00193,0.0026914,0.0029209,0.004284,0.0070945,0.0089795,0.0094701,0.011953,0.016463,0.018719,0.018577,0.021108,0.027849,0.035635,0.037837,0.04143,0.040534,0.043306,0.050939,0.06554,0.082922,0.08408,0.093376,0.098984,0.10733,0.10757,0.11969,0.1306,0.13625,0.11838,0.12348,0.15036,0.17158,0.18245,0.17594,0.18591,0.2047,0.19589,0.20527,0.24525,0.25024,0.23843,0.22203,0.21709,0.21226,0.24861,0.27537,0.28321,0.27894,0.32436,0.3812,0.40722,0.39806,0.38465,0.35116,0.37164,0.42235,0.46878,0.47139,0.428,0.40262,0.41806,0.43623,0.43919,0.42944,0.40724,0.41497,0.44509,0.46388,0.45313,0.41519,0.38214,0.3738,0.40051,0.43411,0.45527,0.46355,0.47446,0.5018,0.50071,0.47139,0.46935,0.48934,0.50767,0.51489,0.48609,0.41843,0.40307,0.45898,0.48932,0.47778,0.48657,0.49404,0.47674,0.47511,0.48336,0.46564,0.47805,0.52798,0.56741,0.55172,0.53022,0.51791,0.48962,0.5204,0.57228,0.60498,0.61156,0.6114000000000001,0.59028,0.55387,0.51942,0.45673,0.46215,0.43006,0.39926,0.46953,0.56549,0.59817,0.56531,0.52024,0.50956,0.5342,0.5851,0.6019099999999999,0.58541,0.60628,0.60058,0.62359,0.68628,0.73532,0.73658,0.72285,0.70914,0.66759,0.6631,0.69315,0.74469,0.75507,0.6826100000000001,0.69338,0.72051,0.67444,0.64253,0.61886,0.55786,0.5564,0.55227,0.5893,0.65162,0.6748,0.6639,0.71225,0.79455,0.85595,0.83418,0.7438900000000001,0.66683,0.70077,0.75075,0.76383,0.68837,0.58678,0.50762,0.45499,0.44049,0.50968,0.61359,0.67355,0.64363,0.621,0.6457000000000001,0.65147,0.6420400000000001,0.6358200000000001,0.63136,0.68543,0.7597,0.79699,0.80371,0.85138,0.86344,0.79493,0.66257,0.47975,0.38152,0.49567,0.68385,0.80772,0.86038,0.7565499999999999,0.55017,0.42619,0.62945,0.85249,1.0069,1.0693,1.1021,1.1141,1.1603,1.2061,1.1613,1.1801,1.1511,1.1227,1.1026,1.1514,1.2299,1.0485,1.1738,1.2478,1.1971,1.1842,1.2258,1.2624,1.2312,1.1777,1.2258,1.1232,1.2757,1.2583,1.2184,1.2117,1.2488,1.2135,1.1724,1.1839,1.0963,0.87462,0.79394,1.3207,1.2288,1.1352,1.2452,1.3659,1.3943,1.2238,1.1775,1.3499,1.3313,1.425,1.4453,1.4084,1.4619,1.3108,1.4903,1.5081,1.5045,1.5595,1.6173,1.5482,1.4297,1.5335,1.5224,1.5724,1.5854,1.5514,1.5391,1.5291,1.5827,1.5975,1.6031,1.5544,1.535,1.5673,1.4973,1.5619,1.5682,1.5077,1.5331,1.6126,1.5499,1.5671,1.6185,1.5631,1.5724,1.623,1.5916,1.6181,1.6177,1.6236,1.6038,1.5734,1.5683,1.2716,1.4241,1.5413,1.4519,1.6224,1.5595,1.4869,1.5903,1.5525,1.6485,1.5676,1.5944,1.5509,1.5507,1.5451,1.4978,1.4966,1.5653,1.4587,1.5635,1.6264,1.556,1.5165,1.5893,1.5481,1.5769,1.6186,1.5206,1.4885,1.5314,1.5455,1.2594,1.4403,1.3957,1.5236,1.5346,1.569,1.4789,1.5905,1.5781,1.5341,1.3417,1.5357,1.6071,1.5446,1.6292,1.5998,1.4286,1.5302,1.5535,1.6199,1.4989,1.5738,1.5352,1.4825,1.4251,1.5511,1.5256,1.5792,1.5435,1.5291,1.549,1.5049,1.552,1.5399,1.5382,1.5697,1.525,1.5549,1.5634,1.5366,1.4988,1.531,1.4483,1.474,1.5595,1.4847,1.5408,1.5106,1.5201,1.4374,1.532,1.518,1.4807,1.4816,1.4331,1.5134,1.5198,1.5119,1.4777,1.4654,1.5023,1.456,1.477,1.502,1.5089,1.532,1.5479,1.5448,1.5324,1.4953,1.5281,1.4934,1.2894,1.3709,1.4662,1.4354,1.4561,1.4491,1.4308,1.4745,1.4788,1.4607,1.4606,1.4753,1.4579,1.436,1.4664,1.4921,1.4895,1.4822,1.4911,1.4862,1.4749,1.4686,1.4611,1.4831,1.4621,1.4176,1.4697,1.431,1.4128,1.4664,1.4733,1.4739,1.4802,1.4269,1.4165,1.4118,1.4026,1.4012,1.4417,1.3631,1.4114,1.3924,1.4161,1.3638,1.4508,1.4284,1.4458,1.4128,1.461,1.4707,1.4646,1.434,1.4348,1.4376,1.4525,1.4462,1.4567,1.415,1.4086,1.3952,1.3519,1.3594,1.4447,1.3871,1.4311,1.4153,1.3499,1.1851,1.2393,1.3855,1.3905,1.3992,1.3933,1.3819,1.3844,1.3967,1.4214,1.4203,1.4102,1.415,1.4394,1.4196,1.4169,1.3972,1.4094,1.4074,1.3958,1.412,1.3991,1.4066,1.3947,1.3969,1.3915,1.3981,1.383,1.3739,1.3748,1.3438,0.96824,1.1206,1.1278,1.1821,1.2333,1.2689,1.2609,1.2464,1.2714,1.2684,1.3403,1.3192,1.2918,1.2823,1.2659,1.2674,1.2747,1.3078,1.3214,1.3144,1.309,1.3048,1.3095,1.3175,1.3155,1.3071,1.2918,1.3029,1.2587,1.2716,1.1071,1.0296,0.92318,0.9855,1.0861,1.2407,1.1444,1.0555,1.038,1.0813,1.085,1.04,1.0466,1.1285,1.0703,1.1534,1.1962,1.2357,1.2178,1.2059,1.2039,1.2269,1.1905,1.2195,1.2148,1.2153,1.2405,1.2503,1.2497,1.247,1.2477,1.2401,1.2357,1.2341,1.2286,1.233,1.2266,1.242,1.2383,1.2232,1.2221,1.2295,1.1945,0.26604,0.15396,0.68766,0.37952,0.53878,0.68601,0.8146099999999999,0.97417,1.1138,1.1278,1.1608,1.1686,1.1778,1.1771,1.1771,1.1771,1.1798,1.1727,1.1713,1.1765,1.1636,1.1607,1.1662,1.1614,1.1536,1.1586,1.1592,1.145,1.1305,1.1257,1.091,1.1058,1.0953,1.0875,1.0972,1.0932,1.0742,1.0913,1.1121,1.0905,1.0725,1.0843,1.0856,1.0657,1.0782,1.0545,1.0974,1.0859,1.0821,1.0548,1.0559,1.0533,1.0268,1.0086,0.90356,0.89523,0.83216,0.85183,0.82259,0.9051900000000001,0.86188,0.99764,0.95157,0.67271,0.93506,0.96935,0.93381,0.98465,0.84979,0.9293,0.91601,0.92392,0.8942600000000001,0.9565,0.93412,1.0032,0.97234,1.0092,0.99901,1.0013,1.0157,1.0101,0.99703,1.0053,0.98631,1.0165,1.0187,0.9917,0.99217,0.9859599999999999,0.89372,0.97493,0.96927,0.9648600000000001,0.85112,0.913,0.97317,0.99166,0.99196,0.99171,0.98816,0.9867899999999999,0.99449,1.0005,0.97916,0.96324,0.849,0.9154600000000001,0.9592000000000001,0.94956,0.96755,0.95387,0.9668600000000001,0.95721,0.94042,0.92687,0.95277,0.9561500000000001,0.95237,0.9365599999999999,0.93957,0.90861,0.93245,0.92927,0.93305,0.94423,0.90752,0.91062,0.92228,0.93455,0.92393,0.92584,0.90881,0.87327,0.8512999999999999,0.81357,0.76253,0.66566,0.7178,0.54871,0.7426,0.59933,0.66791,0.68889,0.84457,0.81709,0.77558,0.63854,0.65217,0.70431,0.6246699999999999,0.66808,0.68893,0.62834,0.62649,0.67836,0.57646,0.73017,0.59271,0.73877,0.74414,0.78049,0.70026,0.74504,0.7215,0.7111,0.70331,0.78742,0.58968,0.55127,0.4321,0.40921,0.30086,0.24841,0.1438,0.25084,0.16142,0.16338,0.20058,0.39887,0.47181,0.37195,0.40532,0.27834,0.28579,0.36821,0.19461,0.37112,0.27423,0.49396,0.14726,0.48378,0.26891,0.34362,0.42411,0.34117,0.32821,0.27067,0.46101,0.37385,0.42066,0.4612,0.44174,0.50503,0.4586,0.50374,0.50275,0.5024,0.6521,0.6862200000000001,0.63461,0.71397,0.68765,0.60648,0.57529,0.58987,0.57191,0.63864,0.61509,0.63815,0.60468,0.71338,0.69218,0.66865,0.73732,0.6881699999999999,0.75083,0.73928,0.7346200000000001,0.7490599999999999,0.73227,0.75358,0.75102,0.73728,0.7541,0.75176,0.74884,0.73971,0.73887,0.7385699999999999,0.73532,0.74442,0.72805,0.73442,0.72336,0.68174,0.71252,0.72753,0.72685,0.71972,0.71914,0.72278,0.71877,0.71761,0.72068,0.70817,0.71129,0.7033700000000001,0.71422,0.6887799999999999,0.69896,0.70175,0.6897,0.69508,0.69058,0.69753,0.69636,0.6930500000000001,0.69385,0.68628,0.69055,0.68736,0.68787,0.67613,0.68015,0.6823399999999999,0.68202,0.67497,0.67172,0.67636,0.6717,0.67176,0.672,0.66525,0.66833,0.66452,0.64714,0.65694,0.66274,0.65896,0.65463,0.65521,0.65118,0.64919,0.64646,0.64847,0.64641,0.6448199999999999,0.63818,0.61875,0.63585,0.62121,0.63266,0.62239,0.63196,0.62913,0.61713,0.62032,0.61944,0.58626,0.6046899999999999,0.61661,0.61536,0.60363,0.62158,0.59252,0.61471,0.60434,0.60321,0.6047400000000001,0.59722,0.58083,0.5894,0.59814,0.57852,0.5933,0.5541,0.56697,0.59317,0.57919,0.5557299999999999,0.58835,0.58124,0.51058,0.53965,0.52067,0.50323,0.57852,0.50291,0.5077199999999999,0.48577,0.49696,0.46883,0.46637,0.46765,0.50644,0.39792,0.48304,0.41565,0.41278,0.47899,0.33154,0.41357,0.2685,0.29985,0.24987,0.20136,0.07961799999999999,0.21753,0.11317,0.14189,0.18586,0.08168599999999999,0.12817,0.1087,0.14428,0.051589,0.15725,0.09922400000000001,0.10591,0.070574,0.2956,0.23411,0.15331,0.04174,0.015462,0.12876,0.28785,0.20329,0.2985,0.25599,0.19337,0.22479,0.31183,0.11326,0.14604,0.15764,0.059176,0.27113,0.21854,0.12164,0.2034,0.24762,0.23812,0.14248,0.31316,0.2809,0.31458,0.31171,0.33693,0.28648,0.34753,0.35002,0.46857,0.40188,0.3886,0.37494,0.40996,0.41954,0.4231,0.45873,0.44831,0.45483,0.45642,0.33692,0.4524,0.47679,0.47235,0.36,0.48371,0.44069,0.45514,0.32318,0.4387,0.41985,0.40741,0.47715,0.45575,0.33504,0.41569,0.46239,0.4466,0.47336,0.45434,0.4689,0.44696,0.43131,0.47715,0.43392,0.36489,0.44825,0.43708,0.43717,0.43409,0.36247,0.43692,0.48086,0.42986,0.43346,0.41428,0.45336,0.42232,0.42489,0.46956,0.43407,0.4278,0.4664,0.45528,0.45934,0.44663,0.45805,0.46531,0.45139,0.44406,0.44808,0.46236,0.46819,0.43304,0.46658,0.46721,0.46003,0.47203,0.46633,0.45397,0.47016,0.46504,0.46908,0.46339,0.46797,0.46272,0.46077,0.46197,0.46247,0.45754,0.45528,0.45655,0.45945,0.45746,0.4586,0.45966,0.45705,0.45258,0.45097,0.44773,0.44363,0.4507,0.44023,0.43532,0.44496,0.42725,0.4311,0.41146,0.39567,0.40019,0.37148,0.3957,0.38527,0.38822,0.37051,0.24652,0.38744,0.40825,0.40879,0.40625,0.40614,0.41233,0.41693,0.42001,0.42763,0.42456,0.42204,0.41335,0.37305,0.40733,0.42078,0.42399,0.42714,0.42213,0.41989,0.40936,0.41285,0.41786,0.39618,0.41257,0.40421,0.40514,0.38957,0.3713,0.39183,0.40852,0.35312,0.36228,0.39181,0.34621,0.30062,0.38382,0.38453,0.30594,0.34696,0.38413,0.30114,0.33366,0.33337,0.31352,0.28833,0.28581,0.32419,0.31217,0.33328,0.26855,0.25872,0.29866,0.30217,0.23279,0.26249,0.32224,0.28051,0.26625,0.2345,0.17759,0.22923,0.1448,0.14579,0.20304,0.16925,0.23117,0.18348,0.16454,0.17804,0.17681,0.16831,0.17039,0.17798,0.12711,0.075645,0.10904,0.058186,0.060119,0.0047451,0.016159,0.016025,0.0046298,0.0015164,9.6096e-05,0.00029009,3.6034e-06,4.807e-05,7.178599999999999e-05,4.1948e-06,7.343899999999999e-07,2.1404e-06,4.8133e-09,1.8076e-11,3.1563e-06,1.3589e-06,9.0764e-12,1.2791e-05,4.9764e-06,1.481e-13,5.1667e-07,2.92e-07,1.9731e-08,2.7498e-06,4.4401e-05,0.00017917,0.00032332,0.00025748,0.0001227,0.0011089,5.2164e-05,8.1587e-05,2.3716e-06,2.5672e-06,4.4017e-08,6.1689e-07,2.0899e-06,2.5215e-06,0.00019896,4.0262e-06,0.00058098,0.00049328,0.00034384,2.3782e-05,0.00011586,7.552599999999999e-05,6.7136e-07,6.3215e-09,4.9057e-05,0.0012704,0.00081226,3.2466e-09,1.0528e-08,0.0018353,0.00238,0.00073892,3.6444e-07,0.0020448,0.00017457,0.0016493,0.00061919,0.00046653,0.0021142,0.0026396,0.023353,0.00036378,0.00018366,0.035565,0.011759,0.013559,0.0021442,0.008271799999999999,0.0091637,0.046314,0.0092198,0.016975,0.02585,0.027792,0.049546,0.0045588,0.03802,0.061601,0.050156,0.0025194,0.035834,0.020962,0.021416,0.038351,0.02988,0.013263,0.051039,0.039601,0.0318,0.036317,0.045063,0.061791,0.049751,0.023095,0.036215,0.11569,0.10213,0.027412,0.011271,0.062361,0.081978,0.13759,0.06615,0.088509,0.117,0.13643,0.16307,0.085421,0.090276,0.1306,0.043225,0.15184,0.09338299999999999,0.065197,0.036054,0.076942,0.094845,0.049678,0.017848,0.046771,0.070198,0.09733899999999999,0.18463,0.06877800000000001,0.06973600000000001,0.06347999999999999,0.12001,0.060637,0.11529,0.05849,0.14859,0.13747,0.12503,0.1234,0.060629,0.09418,0.18973,0.17478,0.19778,0.16441,0.18157,0.20367,0.18253,0.16852,0.2285,0.18968,0.21759,0.25061,0.26552,0.23356,0.18493,0.16029,0.18402,0.25773,0.25514,0.24302,0.1869,0.27052,0.26474,0.26068,0.24239,0.22571,0.26573,0.25683,0.24929,0.25211,0.24437,0.2645,0.27505,0.26378,0.28004,0.27539,0.25884,0.26745,0.2622,0.27928,0.27244,0.25522,0.26973,0.27839,0.27714,0.26892,0.26686,0.27464,0.27336,0.27202,0.27295,0.26491,0.26904,0.26927,0.27208,0.2721,0.27705,0.27481,0.27309,0.26675,0.27342,0.2699,0.27058,0.27182,0.27132,0.26474,0.26759,0.2631,0.27062,0.26848,0.26808,0.26568,0.27002,0.26756,0.26667,0.26264,0.26728,0.26245,0.26308,0.25722,0.25452,0.24175,0.23507,0.23775,0.23407,0.24145,0.23974,0.24678,0.21602,0.23516,0.23672,0.24464,0.2487,0.24195,0.24755,0.24904,0.25874,0.25569,0.25303,0.25107,0.23233,0.24179,0.24197,0.25225,0.25833,0.25624,0.25823,0.24452,0.24692,0.25421,0.24202,0.2381,0.22323,0.22413,0.22397,0.22842,0.23683,0.2414,0.23296,0.2299,0.22727,0.2176,0.2268,0.23076,0.23719,0.23838,0.24104,0.2305,0.23465,0.24352,0.241,0.23449,0.2343,0.23754,0.24246,0.24269,0.23782,0.23971,0.24078,0.24126,0.24137,0.23651,0.23806,0.23821,0.23267,0.23282,0.23367,0.23539,0.227,0.22007,0.22026,0.21511,0.2196,0.22082,0.21535,0.22355,0.21822,0.21749,0.22768,0.21655,0.21867,0.22526,0.20855,0.22373,0.22277,0.21583,0.22231,0.22101,0.22223,0.22487,0.2212,0.22332,0.22384,0.21908,0.22235,0.22098,0.21178,0.17884,0.21068,0.21459,0.21516,0.22168,0.21879,0.21147,0.21629,0.21575,0.2136,0.21145,0.21229,0.20915,0.21303,0.20558,0.19447,0.20366,0.20906,0.19797,0.21321,0.21026,0.20484,0.21013,0.20718,0.20523,0.19303,0.20708,0.21134,0.20477,0.20968,0.20922,0.18107,0.20739,0.20551,0.19975,0.20396,0.19778,0.1879,0.18965,0.18698,0.17808,0.17407,0.16154,0.16818,0.15481,0.16566,0.15301,0.15998,0.13284,0.14172,0.11484,0.1005,0.07698099999999999,0.088904,0.046931,0.031828,0.014815,0.009691099999999999,0.0032816,0.00098755,0.0012744,5.2041e-06,6.419e-06,6.2703e-08,6.2658e-06,2.9993e-06,2.8396e-07,1.1151e-05,1.6982e-05,2.6662e-10,4.513e-10,7.7505e-05,4.389e-05,0.00022333,0.00012947,8.6221e-07,5.6667e-07,2.3045e-05,1.9947e-05,0.00045069,0.00093615,0.00055242,0.0035935,0.0032821,0.010863,0.016727,0.010036,0.021906,0.028563,0.048847,0.067857,0.075512,0.083063,0.08561299999999999,0.08119,0.038156,0.015001,0.039748,0.026648,0.044981,0.07401000000000001,0.084856,0.096386,0.089781,0.091074,0.067927,0.054906,0.069193,0.061875,0.065676,0.077443,0.086812,0.085102,0.0891,0.08974699999999999,0.086133,0.093153,0.089654,0.091673,0.087588,0.088632,0.08977400000000001,0.090044,0.090767,0.089486,0.08463900000000001,0.08484,0.08416999999999999,0.07631,0.081996,0.08044800000000001,0.08180800000000001,0.07455000000000001,0.079068,0.07899200000000001,0.071202,0.07401000000000001,0.079315,0.07627299999999999,0.07772999999999999,0.07545300000000001,0.07577299999999999,0.074299,0.073118,0.070838,0.071937,0.06769,0.066929,0.068137,0.06486699999999999,0.06402099999999999,0.066288,0.06308,0.06322,0.061265,0.058824,0.059171,0.06387,0.058141,0.052031,0.056215,0.056824,0.057967,0.045836,0.0514,0.041536,0.047473,0.050237,0.049409,0.030817,0.044147,0.042552,0.030826,0.037109,0.040594,0.04415,0.033599,0.033813,0.0273,0.02659,0.033078,0.045099,0.014878,0.043249,0.020798,0.013611,0.024853,0.033363,0.024148,0.016727,0.016455,0.0080395,0.0056102,0.0035113,0.0028772,0.0070642,0.0015191,0.0022163,0.0005188,0.00037054,4.1393e-05,6.3593e-07,1.7502e-07,3.7716e-07,5.3758e-11,2.8222e-13,1.0435e-09,3.102e-11,1.5955e-14,1.5258e-18,1.0786e-27,3.8214e-22,1.7194e-34,5.4793e-31,2.2838e-33,4.4912e-28,5.8053e-35,5.9447e-34,1.1196e-37,5.6505e-29,3.8687e-28,2.8026e-45,3.9027e-16,1.175e-16,8.998800000000001e-19,1.4295e-19,1.3133e-27,2.6068e-25,1.1123e-37,0,0,0,0,1.0226e-29,7.1284e-33,0,2.9315e-42,1.125e-35,3.8557e-26,5.6052e-45,7.2935e-22,6.0734e-19,5.4888e-21,2.3314e-27,1.3146e-23,1.6648e-28,6.7262e-44,0,2.6777e-27,8.3791e-24,3.999e-38,4.8067e-34,3.8866e-27,1.217e-16,3.6205e-16,1.6484e-12,6.7478e-14,4.0233e-10,2.8685e-10,2.0548e-11,1.7605e-07,3.9008e-06,2.1276e-10,1.9609e-07,4.0575e-05,1.1566e-06,4.4867e-07,2.5356e-05,0.00016763,6.3129e-06,0.0003917,0.00024724,0.00045332,0.00018623,0.0026643,0.00081152,0.00011096,0.002722,0.0012581,0.0028948,0.0010835,0.0058858,0.0064903,0.0016273,0.0014489,0.0052276,0.0023361,0.0045971,0.0074379,0.00035233,0.00085429,0.0013381,0.0069628,0.01028,0.0042755,0.0078472,0.0028906,0.0068479,0.0055551,0.00063369,0.0075031,0.0060753,0.0024986,0.0020242,0.004209,0.0010321,0.00028947,0.0063012,0.0029113,0.0017492,0.0060221,0.0036224,0.0017671,0.0023805,0.0006551,0.004401,0.00092155,0.00084569,0.0022677,0.009819700000000001,0.0030289,0.0057614,0.011446,0.0033241,0.0032517,0.0066744,0.0056366,0.009232000000000001,0.014017,0.012516,0.009230199999999999,0.010621,0.008082300000000001,0.0042388,0.0026927,0.00043843,0.00030973,0.00013634,0.00049752,0.0016089,0.00019875,0.0003408,0.007294,0.0037464,0.00073409,0.0026067,0.0099378,0.0012248,0.0024465,0.0012186,0.0059265,0.0028644,0.011128,0.0087571,0.0012234,0.0017794,0.0039416,0.0039235,1.6133e-05,5.9987e-05,0.0035187,0.0046616,0.0090694,0.0034602,0.0035408,0.0080277,0.0036308,0.0052402,0.0071907,0.0039389,0.008456,0.0051115,0.0074896,0.0098552,0.009546499999999999,0.012509,0.0044594,0.0070802,0.0072774,0.013165,0.010006,0.008689199999999999,0.011553,0.0080348,0.011318,0.011153,0.008308899999999999,0.01253,0.009817899999999999,0.012264,0.010943,0.011224,0.012094,0.010419,0.012265,0.011917,0.011809,0.011963,0.011494,0.012122,0.011428,0.011127,0.0094556,0.009031000000000001,0.0095432,0.010538,0.009058099999999999,0.010795,0.010851,0.008337600000000001,0.0086444,0.010187,0.009167099999999999,0.0094523,0.00967,0.010262,0.010359,0.0094787,0.009472599999999999,0.011614,0.010239,0.009955,0.010299,0.01148,0.010599,0.010123,0.010978,0.010914,0.010253,0.007900300000000001,0.0048286,0.0083312,0.009438,0.0096922,0.010132,0.010878,0.01077,0.009364000000000001,0.0092254,0.010376,0.010698,0.0092707,0.0085837,0.0088494,0.010331,0.0092903,0.008991799999999999,0.008863299999999999,0.008550200000000001,0.0091243,0.0090521,0.009574600000000001,0.0088123,0.0077564,0.008869200000000001,0.0098592,0.0093049,0.0082451,0.0077569,0.009655,0.009505599999999999,0.0095925,0.0076916,0.0089756,0.008780100000000001,0.008827399999999999,0.0085085,0.007993999999999999,0.008098899999999999,0.0073604,0.006762,0.006534,0.0067717,0.0068818,0.007476,0.007925400000000001,0.007926900000000001,0.0071353,0.0069868,0.0069466,0.006852,0.0070502,0.0073541,0.0074027,0.0075412,0.0076277,0.0077199,0.0077482,0.0078057,0.0076806,0.0075097,0.0073872,0.0074327,0.0073723,0.00721,0.0071043]
    return np.interp(wavelength,wavelength_list,spectrum)



def Photo(struct,incidence,polarization,wl_min,wl_max,active_layers,number_points):
    """ Computes the theoretical short circuit current when the quantum yield is
    assummed to be 1 (ie no recombination of charge carrier) using the
    :absorption: function for the solar spectrum (AM 1.5).

    Args:
        structure (Structure): the object describing the multilayer
        incidence (float): incidence angle in degrees
        .. warning: not meant/tested for non-normal incidence, actually.
        polarization (float): 0 for TE, 1 for TM
        .. warning: meaningless in normal incidence
        wl_min (float): minimum wavelength of the spectrum
        wl_max (float): maximum wavelength of the spectrum
        active_layers(list): list of integers corresponding to the active layers
        number_points (int): number of points in the spectrum

    Returns:
        conversion_efficiency (float): well... conversion efficiency
        total_current: short circuit current in mA/cm^2
        total_current_max: short circuit current with unity absorbance (mA/cm^2)
        wavelength_list (numpy array): list of considered wavelengths
        spectrum: AM 1.5 solar Spectrum
        current_density: current by wavelength unit (mA/cm^2/nm)
        """

    theta=incidence*np.pi/180
    wavelength_list=np.linspace(wl_min,wl_max,number_points)

    photon_density = np.zeros(number_points, dtype = float)
    total_absorbed = np.zeros(number_points, dtype = float)
    spectrum = np.zeros(number_points, dtype = float)

    for k in range(number_points):
        absorb,r,t,R,T = absorption(struct,wavelength_list[k],theta,polarization)
        photon_density[k] = solar(wavelength_list[k])
        total_absorbed[k] = np.sum(absorb[active_layers])
        spectrum[k] = am1_5(wavelength_list[k])

    current_density = np.multiply(photon_density,total_absorbed)
    total_current_max = np.trapz(photon_density,wavelength_list)*1e3
    total_current = np.trapz(current_density,wavelength_list)*1e3
    conversion_efficiency = total_current/total_current_max

    return conversion_efficiency,total_current,total_current_max,wavelength_list,photon_density,total_absorbed

def dispersion(alpha,struct,wavelength,polarization):
    """ It would probably be better to compute the dispersion relation of a
    multilayered structure, like the determinant of the inverse of the
    scattering matrix. However, strangely enough, for a single interface, it
    just does not work. Even though the coefficients of the scattering matrix
    diverge the determinant does not, so that it does not work to find the
    surface plasmon mode, force instance.

    The present function actually computes the inverse of the modulus of the
    reflection coefficient. Since a mode is a pole of the coefficient, here it
    should be a zero of the resulting function. The determination of the square
    root is modified, so that the modes are not hidden by any cut due to the
    square root.

    Args:
        alpha (complex) : wavevector
        struct (Structure) : the object describing the multilayer
        wavelength : the wavelength in vacuum in nanometer
        polarization : 0 for TE, 1 for TM.

    Returns:
        1/abs(r) : inverse of the modulus of the reflection coefficient.

    """

    Epsilon, Mu = struct.polarizability(wavelength)
    thickness = copy.deepcopy(struct.thickness)
    # In order to ensure that the phase reference is at the beginning
    # of the first layer. Totally necessary when you are looking for
    # modes of the structure, this makes the poles of the reflection
    # coefficient much more visible.
    thickness[0] = 0
    Type = struct.layer_type
    # The boundary conditions will change when the polarization changes.
    if polarization == 0:
        f = Mu
    else:
        f = Epsilon
    # Wavevector in vacuum.
    k0 = 2 * np.pi / wavelength
    # Number of layers
    g = len(struct.layer_type)
    # Computation of the vertical wavevectors k_z
    gamma = np.sqrt(
        Epsilon[Type] * Mu[Type] * k0 ** 2 - np.ones(g) * alpha ** 2)

    # Changing the determination of the square root to achieve perfect stability
    if g > 2:
        gamma[1:g - 2] = gamma[1:g - 2] * (
                    1 - 2 * (np.imag(gamma[1:g - 2]) < 0))
    # Changing the determination of the square root in the external medium
    # to better see the structure of the complex plane.
    gamma[0] = gamma[0] * (
                    1 - 2 * (np.angle(gamma[0])<-np.pi/5)  )
    gamma[g-1] = gamma[g-1] * (
                1 - 2 * (np.angle(gamma[g-1])<-np.pi/5)  )

    T = np.zeros(((2 * g, 2, 2)), dtype=complex)

    # first S matrix
    T[0] = [[0, 1], [1, 0]]
    for k in range(g - 1):
        # Layer scattering matrix
        t = np.exp((1j) * gamma[k] * thickness[k])
        T[2 * k + 1] = [[0, t], [t, 0]]
        # Interface scattering matrix
        b1 = gamma[k] / f[Type[k]]
        b2 = gamma[k + 1] / f[Type[k + 1]]
        T[2 * k + 2] = [[(b1 - b2) / (b1 + b2), 2 * b2 / (b1 + b2)],
                        [2 * b1 / (b1 + b2), (b2 - b1) / (b1 + b2)]]
    t = np.exp((1j) * gamma[g - 1] * thickness[g - 1])
    T[2 * g - 1] = [[0, t], [t, 0]]
    # Once the scattering matrixes have been prepared, now let us combine them
    A = np.zeros(((2 * g - 1, 2, 2)), dtype=complex)
    A[0] = T[0]

    for j in range(len(T) - 2):
        A[j + 1] = cascade(A[j], T[j + 1])
    # reflection coefficient of the whole structure
    r = A[len(A) - 1][0, 0]

    return 1/np.abs(r)
#    return 1/r

def Map(struct,wavelength,polarization,real_bounds,imag_bounds,n_real,n_imag):
    """ Maps the function `dispersion` supposed to vanish when the dispersion
    relation is satisfied.

    Args:
        struct (Structure): object Structure describing the multilayer
        wavelength: wavelength in vacuum (in nm)
        polarization: 0 for TE, 1 for TM
        real_bounds: a list giving the bounds of the effective index
                     real part [n_min,n_max], defining the zone to
                     explore.
        imag_bounds: a list giving the bounds of the effective index
                     imaginary part.
        n_real: number of points horizontally (real part)
        n_imag: number of points vertically (imaginary part)

    Returns:
        X (1D numpy array): values of the real part of the effective index
        Y (1D numpy array): values of the imaginary part of the effective index
        T (2D numpy array): values of the dispersion function

    In order to visualize the map, just use :
        import matplotlib.pyplot as plt
        plt.contourf(X,Y,np.sqrt(np.real(T)))
        plt.show()
    """

    k_0=2*np.pi/wavelength
    X=np.linspace(real_bounds[0],real_bounds[1],n_real)
    Y=np.linspace(imag_bounds[0],imag_bounds[1],n_imag)
    xa,xb=np.meshgrid(X*k_0,Y*k_0)
    M=xa+1j*xb

    T=np.zeros((n_real,n_imag),dtype=complex)
    for k in range(n_real):
        for l in range(n_imag):
            T[k,l]=1/dispersion(M[k,l],struct,wavelength,polarization)

    return X,Y,T

def Guided_modes(struct,wavelength,polarization,neff_min,neff_max,initial_points = 40):

    """ This function explores the complex plane, looking for zeros of the
    dispersion relation. It does so by launching a steepest descent for a number
    `initial_points` of points on the real axis between neff_min and neff_max.


    Args:
        struct (Structure): object describing the multilayer
        wavelength (float): wavelength in nm
        polarization: 0 for TE, 1 for TM
        neff_min: minimum value of the effective index expected
        neff_max: maximum value of the effective index expected

    Returns:
        modes (list, complex): complex effective index identified as
                            solutions of the dispersion relation.

    """

    tolerance = 1e-10
#    initial_points = 40
    k_0=2*np.pi/wavelength
    neff_start = np.linspace(neff_min,neff_max,initial_points,dtype=complex)
    modes=[]
    for neff in neff_start:
#        solution = optim.newton(dispersion,kx,args=(struct,wavelength,polarization),tol=tolerance,full_output = True)
#        solution = optim.minimize(dispersion,kx,args=(struct,wavelength,polarization))
        solution = steepest(neff,tolerance,1000,struct,wavelength,polarization)
#        print(solution)
        if (len(modes)==0):
            modes.append(solution)
        elif (min(abs(modes-solution))>1e-5*k_0):
            modes.append(solution)

    return modes

def muller(starting_points,tol,step_max,struct,wl,pol):

    k_0 = 2* np.pi / wl
    x=np.array(starting_points) * k_0
    f=np.array([dispersion(x[0],struct,wl,pol),dispersion(x[1],struct,wl,pol),dispersion(x[2],struct,wl,pol)])
    step=0
    print(x,"\n step :",step,"\n",f)

    while (f[2]>tol) and (step<step_max):
        #print(x,"\n step :",step,"\n valeur de f", f[2] )
        q=(x[2]-x[1])/(x[1]-x[0])
        A = q * f[2] - q*(1+ q) * f[1] + q * q * f[0]
        B = (2*q+1) * f[2] - (1+q)**2 * f[1] + q*q * f[0]
        C = (1+q) * f[2]
        temp = np.sqrt(B*B-4*A*C)
        D = max([abs(B+temp),abs(B-temp)])
        new_x = x[2]-(x[2]-x[1]) * 2 * C / D
        #new_x= x[2] - 2*C/D
        x[0]=x[1]
        x[1]=x[2]
        x[2]=new_x
        f[0]=f[1]
        f[1]=f[2]
        f[2]=dispersion(new_x,struct,wl,pol)
        print("New values:",step,new_x/k_0,f[2])
        step += 1

    return x[2]/k_0

def steepest(start,tol,step_max,struct,wl,pol):
    """ Steepest descent to find a zero of the `dispersion`
    function. The advantage of looking for a zero is that you
    know when the algorithm can stop (when the value of the function
    is smaller than `tol`).

    Args:
        start (complex): effective index where the descent starts
        tol (real): when dispersion is smaller than tol, the
                    descent stops.
        step_max (integer): maximum number of steps allowed
        struct (Structure): the object describing the multilayer
        wl (float): wavelength in vacuum
        pol: 0 for TE, 1 for TM

    Returns:

        (float) : last effective index reached at the end of the descent

    """


    k_0 = 2 * np.pi / wl
    z=start*k_0
    delta = abs(z) * 0.001
    dz= 0.01 * delta
    step = 0
    current = dispersion(z,struct,wl,pol)

    while (current > tol) and (step < step_max):

        grad = (
        dispersion(z+dz,struct,wl,pol)
        -current
#        -dispersion(z-dz,struct,wl,pol)
        +1j*(dispersion(z+1j*dz,struct,wl,pol)
#        -dispersion(z-1j*dz,struct,wl,pol))
        -current)
        )/(dz)

        if abs(grad)!=0 :
            z_new = z - delta * grad / abs(grad)
        else:
            print("Time to get out of here ! Gradient is null")
            step = step_max

        value_new = dispersion(z_new,struct,wl,pol)
        if (value_new > current):
            # The path not taken
            delta = delta / 2.
            dz = dz / 2.
        else:
            current = value_new
            z = z_new
    #        print("Step", step, z,current)
        step = step + 1

    #print("End of the loop")
    if step == step_max:
        print("Warning: maximum number of steps reached")

    return z/k_0

def Profile(struct,n_eff,wavelength,polarization,pixel_size = 3):


    # Wavevector in vacuum.
    k_0 = 2 * np.pi / wavelength
    # Wavevector of the mode considered here.
    alpha = n_eff * k_0
    # About the structure:
    Epsilon, Mu = struct.polarizability(wavelength)
    thickness = copy.deepcopy(struct.thickness)
    Type = struct.layer_type
    g = len(Type) - 1
    # The boundary conditions will change when the polarization changes.
    if polarization == 0:
        f = Mu
    else:
        f = Epsilon
    # Computation of the vertical wavevectors k_z
    gamma = np.sqrt(
        Epsilon[Type] * Mu[Type] * k_0 ** 2 - np.ones(g+1) * alpha ** 2)
    # Changing the determination of the square root to achieve perfect stability
    if g > 2:
        gamma[1:g - 2] = gamma[1:g - 2] * (
                1 - 2 * (np.imag(gamma[1:g - 2]) < 0))
    # Don't forget the square root has to change
    # when the wavevector is complex (same as with
    # dispersion and Map)
    gamma[0] = gamma[0] * (
                    1 - 2 * (np.angle(gamma[0])<-np.pi/5)  )
    gamma[g] = gamma[g] * (
                1 - 2 * (np.angle(gamma[g])<-np.pi/5)  )
    # We compute all the scattering matrixes starting with the second layer
    T = np.zeros((2 * g, 2, 2), dtype=complex)
    T[0] = [[0, 1], [1, 0]]
    for k in range(1,g):
        t = np.exp(1j * gamma[k] * thickness[k])
        T[2 * k -1 ] = np.array([[0, t], [t, 0]])
        b1 = gamma[k] / f[Type[k]]
        b2 = gamma[k + 1] / f[Type[k + 1]]
        T[2 * k ] = np.array([[b1 - b2, 2 * b2], [2 * b1, b2 - b1]]) / (
                    b1 + b2)
    t = np.exp(1j * gamma[g] * thickness[g])
    T[2 * g - 1] = np.array([[0, t], [t, 0]])

    H = np.zeros((len(T) - 1, 2, 2), dtype=complex)
    A = np.zeros((len(T) - 1, 2, 2), dtype=complex)
    H[0] = T[2 * g - 1]
    A[0] = T[0]

    for k in range(len(T) - 2):
        A[k + 1] = cascade(A[k], T[k + 1])
        H[k + 1] = cascade(T[len(T) - k - 2], H[k])

    I = np.zeros((len(T), 2, 2), dtype=complex)
    for k in range(len(T) - 1):
        I[k] = np.array(
            [[A[k][1, 0], A[k][1, 1] * H[len(T) - k - 2][0, 1]],
             [A[k][1, 0] * H[len(T) - k - 2][0, 0],
              H[len(T) - k - 2][0, 1]]] / (
                    1 - A[k][1, 1] * H[len(T) - k - 2][0, 0]))

    # Coefficients, in each layer
    Coeffs = np.zeros((g+1,2),dtype = complex)
    Coeffs[0] = np.array([0,1.])
    # Value of the first down propagating plane wave below
    # the first interface, entering the scattering matrix
    # for the rest of the structure. The amplitude of the
    # incident wave is thus not 1.
    b1 = gamma[0]/f[Type[0]]
    b2 = gamma[1]/f[Type[1]]
    tmp = (b2 - b1)/ (2 * b2)
    for k in range(g):
        Coeffs[k+1] =  tmp * np.array([I[2 * k][0, 0],I[2 * k + 1][1, 0]])

    n_pixels = np.floor(np.array(thickness) / pixel_size)
    n_pixels.astype(int)
    n_total = int(np.sum(n_pixels))
    E = np.zeros(n_total,dtype = complex)
    h=0.
    t=0

    for k in range(g+1):
        for m in range(int(n_pixels[k])):
            h = h + pixel_size
            E[t] = Coeffs[k,0] * np.exp(1j * gamma[k] * h) + \
                   Coeffs[k,1] * np.exp(
                   1j * gamma[k] * (thickness[k] - h))
            t+=1
        h=0

    x = np.linspace(0,sum(thickness),len(E))
    return x,E

def Green(struct,window,lam,source_interface):

    """Computes the electric (TE polarization) or magnetic (TM) field inside
    a multilayered structure illuminated by punctual source placed inside
    the structure.

    Args:
        struct (Structure): description (materials,thicknesses)of the multilayer
        window (Window): description of the simulation domain
        lam (float): wavelength in vacuum
        source_interface (int):
    Returns:
        En (np.array): a matrix with the complex amplitude of the field

    Afterwards the matrix may be used to represent either the modulus or the
    real part of the field.
    """


    # Computation of all the permittivities/permeabilities
    Epsilon, Mu = struct.polarizability(lam)
    thickness = np.array(struct.thickness)
    pol = 0
    d = window.width
    C = window.C
    ny = np.floor(thickness / window.py)
    nx = window.nx
    Type = struct.layer_type
    print("Pixels vertically:", int(sum(ny)))

    # Check it's ready for the Green function :
    # Type of the layer is supposed to be the same
    # on both sides of the Interface

    if Type[source_interface-1]!= Type[source_interface]:
        print("Error: there should be the same material on both sides " +
              "of the interface where the source is located.")
        return 0

    # Number of modes retained for the description of the field
    # so that the last mode has an amplitude < 1e-3 - you may want
    # to change it if the structure present reflexion coefficients
    # that are subject to very swift changes with the angle of incidence.

    nmod = int(np.floor(0.83660 * d / w))

    # ----------- Do not touch this part ---------------
    l = lam / d
    w = w / d
    thickness = thickness / d

    if pol == 0:
        f = Mu
    else:
        f = Epsilon
    # Wavevector in vacuum, no dimension
    k0 = 2 * pi / l
    # Initialization of the field component
    En = np.zeros((int(sum(ny)), int(nx)))
    # Total number of layers
    # g=Type.size-1
    g = len(struct.layer_type) - 1

    # Scattering matrix corresponding to no interface.
    T = np.zeros((2 * g + 2, 2, 2), dtype=complex)
    T[0] = [[0, 1], [1, 0]]
    for nm in np.arange(2 * nmod + 1):

        alpha = 2 * pi * (nm - nmod)
        gamma = np.sqrt(
            Epsilon[Type] * Mu[Type] * k0 ** 2 - np.ones(g + 1) * alpha ** 2)

        if np.real(Epsilon[Type[0]]) < 0 and np.real(Mu[Type[0]]) < 0:
            gamma[0] = -gamma[0]

        if g > 2:
            gamma[1:g - 1] = gamma[1:g - 1] * (
                    1 - 2 * (np.imag(gamma[1:g - 1]) < 0))
        if np.real(Epsilon[Type[g]]) < 0 and np.real(
                Mu[Type[g]]) < 0 and np.real(
            np.sqrt(Epsilon[Type[g]] * k0 ** 2 - alpha ** 2)) != 0:
            gamma[g] = -np.sqrt(
                Epsilon[Type[g]] * Mu[Type[g]] * k0 ** 2 - alpha ** 2)
        else:
            gamma[g] = np.sqrt(
                Epsilon[Type[g]] * Mu[Type[g]] * k0 ** 2 - alpha ** 2)

        for k in range(g):
            t = np.exp(1j * gamma[k] * thickness[k])
            T[2 * k + 1] = np.array([[0, t], [t, 0]])
            b1 = gamma[k] / f[Type[k]]
            b2 = gamma[k + 1] / f[Type[k + 1]]
            T[2 * k + 2] = np.array([[b1 - b2, 2 * b2], [2 * b1, b2 - b1]]) / (
                    b1 + b2)
        t = np.exp(1j * gamma[g] * thickness[g])
        T[2 * g + 1] = np.array([[0, t], [t, 0]])

        H_up = np.zeros((2*source_interface, 2, 2), dtype=complex)
        A_up = np.zeros((2*source_interface, 2, 2), dtype=complex)

        H_up[0] = T[0]
        A_up[0] = T[0]

        for k in range(2*source_interface-1):
            A_up[k + 1] = cascade(A[k], T[k + 1])
            H_up[k + 1] = cascade(T[2*source_interface-1-k], H[k])

        I_up = np.zeros((len(T), 2, 2), dtype=complex)
        for k in range(2*source_interface-1):
            I_up[k] = np.array(
                [[A[k][1, 0], A[k][1, 1] * H[len(T) - k - 2][0, 1]],
                 [A[k][1, 0] * H[len(T) - k - 2][0, 0],
                  H[len(T) - k - 2][0, 1]]] / (
                        1 - A[k][1, 1] * H[len(T) - k - 2][0, 0]))

        h = 0
        t = 0


        E = np.zeros((int(np.sum(ny)), 1), dtype=complex)

        for k in range(g + 1):
            for m in range(int(ny[k])):
                h = h + float(thickness[k]) / ny[k]
                #The expression for the field used here is based on the assumption
                # that the structure is illuminated from above only, with an Amplitude
                # of 1 for the incident wave. If you want only the reflected
                # field, take off the second term.
                E[t, 0] = I[2 * k][0, 0] * np.exp(1j * gamma[k] * h) + \
                          I[2 * k + 1][1, 0] * np.exp(
                    1j * gamma[k] * (thickness[k] - h))
                t += 1
            h = 0
        E = E * np.exp(1j * alpha * np.arange(0, nx) / nx)
        En = En + E

    return En
