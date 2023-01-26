from itertools import combinations, product
import numpy as np


class Determinant:
    """
    This class can be used to generate ONVs from a list of occupied orbitals
    and generate all n-tuply exited determinants

    :param alpha_occ: list of occupied alpha orbitals
    :param beta_occ: list of occupied beta orbitals
    :param alpha_onv: bit string representation of occupied alpha orbitals
    :param beta_onv: bit string respresentation of occupied beta orbitals
    """

    def __init__(self, alpha_occ=[], beta_occ=[], nalpha=None, nbeta=None, sites=None):
        """
        :param nalpha: number of alpha electrons (default is None)
        :param nbeta: number of beta electrons (default is None)
        :param alpha_occ: list of occupied alpha orbitals indices
            e.g. [0, 1] means orbitals 0 and 1 are occupied
        :param beta_occ: list of occupied beta orbitals indices
        :param sites: the system size, if None, then half filling is assumed
        """

        if nalpha is not None and nbeta is not None:
            self._alpha_occ = list(range(nalpha))
            self._beta_occ = list(range(nbeta))
        else:
            self._alpha_occ = list(alpha_occ)
            self._beta_occ = list(beta_occ)

        self._nalpha = len(self._alpha_occ)
        self._nbeta = len(self._beta_occ)

        self._sites = self._nalpha + self._nbeta if sites is None else sites

        # Convert occupancy list to bit string
        self._alpha_onv = Determinant.orbitals_to_onv(self._alpha_occ)
        self._beta_onv = Determinant.orbitals_to_onv(self._beta_occ)

        self.excitations_list = []

    def __eq__(self, other):
        return self._alpha_onv == other.alpha_onv and self._beta_onv == other.beta_onv

    def __hash__(self) -> int:
        return hash((self._alpha_onv, self._beta_onv))

    def __str__(self):
        """
        Print a representation of the Determinant
        """
        output = ""

        # Loop through all sites
        for site in range(self._sites):
            if site in self._alpha_occ:
                # If site is occupied by an alpha electron, add an up arrow
                output += "\u25B2"
            else:
                # If no alpha electron is on this site, add _
                output += "_"

            if site in self._beta_occ:
                # If site is occupied by a beta electron, add a down arrow
                output += "\u25BC"
            else:
                # If no beta electron is on this site, add _
                output += "_"

            # Add spacing between sites
            output += "\t"

        return output

        # return "|" + str(self._alpha_occ) + str(self._beta_occ) + ">"

    @property
    def alpha_onv(self):
        return self._alpha_onv

    @property
    def beta_onv(self):
        return self._beta_onv

    @property
    def alpha_occ(self):
        return np.asarray(self._alpha_occ)

    @property
    def beta_occ(self):
        return np.asarray(self._beta_occ)

    @property
    def nalpha(self):
        return self._nalpha

    @property
    def nbeta(self):
        return self._nbeta

    @property
    def nelectrons(self):
        return self._nalpha + self._nbeta

    @property
    def sites(self):
        return self._sites

    @staticmethod
    def orbitals_to_onv(occ_list: list) -> list:
        """
        Convert a list of occupied orbitals to bit string
        e.g. [0, 1] -> 11

        :param occ_list: list of occupied orbitals
        """

        # Return 0 if occ_list is empty
        if not occ_list:
            return 0

        # Sort list and reverse it, because the highest occupied orbital
        # is the left most bit
        occ_list = sorted(occ_list, reverse=True)

        bitstring = 0
        prev_occ_orbital = occ_list[0]
        for occ_orbital in occ_list:
            # Leftshift the bit string so that the last bit corresponds to
            # the current occupied orbital
            bitstring <<= prev_occ_orbital - occ_orbital
            # Set last bit on 1
            bitstring |= 1
            # Store current orbital
            prev_occ_orbital = occ_orbital
        # Leftshift so that the last orbital corresponds to orbital 1
        bitstring <<= prev_occ_orbital

        return bitstring

    @staticmethod
    def onv_to_orbitals(bitstring) -> list:
        """
        Return a list with the occupied orbitals indices

        :param bitstring: bitstring representation of determinant
        """
        occ_list = []

        index = 0
        # Loop until all bits have been seen
        while bitstring != 0:
            # If the right most bit is 1, this orbital is occupied
            if bitstring & 1 == 1:
                occ_list.append(index)
            # Remove the right most bit
            bitstring >>= 1
            index += 1

        return occ_list

    @staticmethod
    def to_spin_orbitals(alpha_occ, beta_occ):
        """
        Returns a list of spin orbitals where even orbitals are alpha and
        odd orbitals are beta

        :param alpha_occ: list of occupied alpha orbitals
        :param beta_occ: list of occupied beta orbitals
        """

        return [i * 2 for i in alpha_occ] + [i * 2 + 1 for i in beta_occ]

    @staticmethod
    def get_unoccupied_orbitals(bitstring, nmo: int) -> list:
        """
        Return a list with the unoccupied orbitals indices

        :param bitstring: bit string representation of a determinant
        :param nmo: number of molecular orbitals
        """

        # Negate the bit string, now 1 corresponds to unoccupied orbital
        bitstring = ~bitstring

        unocc_list = []

        # Loop through all orbital indices
        for i in range(nmo):
            # If the last bit is 1, this orbital is unoccupied add it to
            # the list
            if bitstring & 1 == 1:
                unocc_list.append(i)
            # Remove the right most bit
            bitstring >>= 1

        return unocc_list

    @staticmethod
    def _num_different_orbitals(onv1, onv2) -> int:
        """
        Counts how many orbitals are different occupied between onv1 and
        onv2
        """

        different_bits = onv1 ^ onv2

        count = 0

        while different_bits != 0:
            if different_bits & 1 == 1:
                count += 1
            different_bits >>= 1

        # If one electron is in another orbital, two bits will be different
        return count / 2

    @staticmethod
    def get_position(ref_list, occ_list):
        """
        Returns the indices from the values in occ_list in ref_list
        Used to find the position of an orbital in the determinant
        """

        positions = []

        for index, i in enumerate(sorted(ref_list)):
            if i in occ_list:
                positions.append(index)

        return positions

    @staticmethod
    def _different_bits_to_orbitals(onv1, onv2):
        """
        Returns a list of orbitals that are different between onv1 and onv2

        :param onv1: bit string representation of a determinant
        :param onv2: bit string representation of a determinant
        """
        common_bits = onv1 & onv2

        # Find the different bits and convert to orbital indices
        different_orb_1 = Determinant.onv_to_orbitals(onv1 ^ common_bits)
        different_orb_2 = Determinant.onv_to_orbitals(onv2 ^ common_bits)

        return different_orb_1, different_orb_2

    def get_spin_orbitals(self):
        """
        Returns a list of spin orbitals where even orbitals are alpha and
        odd orbitals are beta
        """
        return [i * 2 for i in self._alpha_occ] + [i * 2 + 1 for i in self._beta_occ]

    def copy(self):
        """
        Creates a copy of itself
        """
        return Determinant(self._alpha_occ, self._beta_occ, sites=self._sites)

    def remove_alpha_orbital(self, orbital_index: int):
        """
        Removes the alpha orbital at orbital_index. This is equivalent to
        setting the bit at index 'orbital_index' to 0

        :param orbital_index: orbital to remove
        """
        # If we want to destroy an electron that is not occupied the
        # resulting wave function is 0
        if orbital_index not in self._alpha_occ:
            self._alpha_onv = 0
            self._beta_onv = 0
        else:
            # Create a bit string with at index 'orbital_index' a 1
            # Use XOR to set the bit at index 'orbital_index' in alpha_onv
            # to 0 and don't change any other bit
            self._alpha_onv ^= 1 << orbital_index

        # Update occupied list
        self._alpha_occ = Determinant.onv_to_orbitals(self._alpha_onv)
        self._beta_occ = Determinant.onv_to_orbitals(self._beta_onv)

    def remove_beta_orbital(self, orbital_index: int):
        """
        Removes the beta orbital at orbital_index. This is equivalent to
        setting the bit at index 'orbital_index' to 0

        :param orbital_index: orbital to remove
        """

        # If we want to destroy an electron that is not occupied the
        # resulting wave function is 0
        if orbital_index not in self._beta_occ:
            self._beta_onv = 0
            self._alpha_onv = 0
        else:
            # Create a bit string where the bit at index 'orbital_index' is 1
            # Use bitwise XOR to set the bit at index 'orbital_index' in
            # beta_onv to 0 and don't change any other bit
            self._beta_onv ^= 1 << orbital_index

        # Update occupied list
        self._alpha_occ = Determinant.onv_to_orbitals(self._alpha_onv)
        self._beta_occ = Determinant.onv_to_orbitals(self._beta_onv)

    def add_alpha_orbital(self, orbital_index: int):
        """
        Add an alpha orbital at orbital_index. This is equivalent to setting
        the bit at index 'orbital_index' to 1

        :param orbital_index: orbital to create
        """
        # If orbital is already occupied kill the wave function
        if orbital_index in self._alpha_occ:
            self._alpha_onv = 0
            self._beta_onv = 0
        else:
            # Create a bit string where the bit at index 'orbital_index' is 1
            # Use OR to set the bit at index 'orbital_index' in alpha_onv to 1
            # and don't change any other bit
            self._alpha_onv |= 1 << orbital_index

        # Update occupied list
        self._alpha_occ = Determinant.onv_to_orbitals(self._alpha_onv)
        self._beta_occ = Determinant.onv_to_orbitals(self._beta_onv)

    def add_beta_orbital(self, orbital_index: int):
        """
        Add an alpha orbital at orbital_index. This is equivalent to setting
        the bit at index 'orbital_index' to 1

        :param orbital_index: orbital to create
        """
        # If orbital is already occupied kill the wave function
        if orbital_index in self._beta_occ:
            self._alpha_onv = 0
            self._beta_onv = 0
        else:
            # Create a bit string where the bit at index 'orbital_index' is 1
            # Use OR to set the bit at index 'orbital_index' in beta_onv to 1
            # and don't change any other bit
            self._beta_onv |= 1 << orbital_index

        # Update occupied list
        self._alpha_occ = Determinant.onv_to_orbitals(self._alpha_onv)
        self._beta_occ = Determinant.onv_to_orbitals(self._beta_onv)

    def n_tuply_excitations(self, n: int, nmo: int, triplets=False) -> list:
        """
        Returns a list of all n-tuply excited determinants

        :param n: number of excitations
        :param nmo: number of sites
        """

        # Return determinant if no excitations are asked
        if n == 0:
            return [self]
        
        alpha_unocc = Determinant.get_unoccupied_orbitals(self._alpha_onv, nmo)
        beta_unocc = Determinant.get_unoccupied_orbitals(self._beta_onv, nmo)

        determinants = []

        # Create all possible combinations with n elements from the
        # alpha_occ orbitals to eleminate the use of a prefactor
        for bs in combinations(self._alpha_occ, n):
            for rs in combinations(alpha_unocc, n):
                det = self.copy()
                # Remove orbitals
                for b in bs:
                    det.remove_alpha_orbital(b)
                # Add orbitals
                for r in rs:
                    det.add_alpha_orbital(r)
                determinants.append(det)

        for bs in combinations(self._beta_occ, n):
            for rs in combinations(beta_unocc, n):
                det = self.copy()
                # Remove orbitals
                for b in bs:
                    det.remove_beta_orbital(b)
                # Add orbitals
                for r in rs:
                    det.add_beta_orbital(r)
                determinants.append(det)

        # Triplet excitations
        if triplets:
            # Excite alpha to beta
            for bs in combinations(self._alpha_occ, n):
                for rs in combinations(beta_unocc, n):
                    det = self.copy()
                    # Remove orbitals
                    for b in bs:
                        det.remove_alpha_orbital(b)
                    # Add orbitals
                    for r in rs:
                        det.add_beta_orbital(r)
                    determinants.append(det)

            # Excite beta to alpha
            for bs in combinations(self._beta_occ, n):
                for rs in combinations(alpha_unocc, n):
                    det = self.copy()
                    # Remove orbitals
                    for b in bs:
                        det.remove_beta_orbital(b)
                    # Add orbitals
                    for r in rs:
                        det.add_alpha_orbital(r)
                    determinants.append(det)

        # Excite alpha and beta
#         for i in range(n):
            
#             for alpha_a in combinations(self._alpha_occ, i):
#                 for alpha_r in combinations(alpha_unocc, i):
                    
#                     for j in range(n):
#                         self.excitations_list.append((i, j))
                        
#                         for beta_b in combinations(self._beta_occ, j):
#                             for beta_s in combinations(beta_unocc, j):
                                
#                                 det = self.copy()
                                
#                                 # Remove alpha orbitals
#                                 for a in alpha_a:
#                                     det.remove_alpha_orbital(a)
#                                 # Remove beta orbitals
#                                 for b in beta_b:
#                                     det.remove_beta_orbital(b)
                                
#                                 # Create alpha orbitals
#                                 for r in alpha_r:
#                                     det.add_alpha_orbital(r)
#                                 # Create beta orbitals
#                                 for s in beta_s:
#                                     det.add_beta_orbital(s)
                                
#                                 determinants.append(det)

        for n_beta in range(1, n):
            alpha_excitations_origin = list(combinations(self._alpha_occ, n-n_beta))
            beta_excitations_origin = list(combinations(self._beta_occ, n_beta))
            alpha_excitations_end = list(combinations(alpha_unocc, n-n_beta))
            beta_excitations_end = list(combinations(beta_unocc, n_beta))

            for i in product(alpha_excitations_origin, beta_excitations_origin):
                alpha_i, beta_i = i

                for a in product(alpha_excitations_end, beta_excitations_end):
                    alpha_a, beta_a = a

                    det = self.copy()
                                
                    # Remove alpha orbitals
                    for i in alpha_i:
                        det.remove_alpha_orbital(i)
                    # Remove beta orbitals
                    for i in beta_i:
                        det.remove_beta_orbital(i)
                    
                    # Create alpha orbitals
                    for a in alpha_a:
                        det.add_alpha_orbital(a)
                    # Create beta orbitals
                    for a in beta_a:
                        det.add_beta_orbital(a)
                    
                    determinants.append(det)

        return determinants

    def single_excitations(self, nmo: int) -> list:
        """
        Returns a list of all singly excited determinants

        :param nmo: number of molecular orbitals
        """
        return self.n_tuply_excitations(1, nmo)

    def single_and_double_excitations(self, nmo) -> list:
        """
        Returns a list of all singly and doubly excited Determinant

        :param nmo: number of molecular orbitals
        """
        return self.n_tuply_excitations(1, nmo) + self.n_tuply_excitations(2, nmo)

    def single_double_and_triple_excitations(self, nmo) -> list:
        """
        Returns a list of all singly, doubly and triple excited Determinant

        :param nmo: number of molecular orbitals
        """
        return (
            self.n_tuply_excitations(1, nmo)
            + self.n_tuply_excitations(2, nmo)
            + self.n_tuply_excitations(3, nmo)
        )

    def all_excitations(self, nmo: int) -> list:
        """
        Returns a list of all possible excited Determinant
        :param nmo: number of molecular orbitals
        """

        # pool = multiprocessing.Pool(multiprocessing.cpu_count())
        determinants = [self]
        
        # The maximum number of excitation is limited by the number of
        # electrons. The length of the occupied indices list gives the
        # number of electrons (N).
        for n in range(1, len(self._alpha_occ) + len(self._beta_occ) + 1):
            det = self.n_tuply_excitations(n, nmo, triplets=False)
            determinants.extend(det)
        # return determinants
        return list(set(determinants))

    def num_different_orbitals(self, other) -> int:
        """
        Returns a number of how many orbitals are different between
        the two slater Determinant

        :param other: other Determinant to compare
        """
        return Determinant._num_different_orbitals(
            self._alpha_onv, other.alpha_onv
        ) + Determinant._num_different_orbitals(self._beta_onv, other.beta_onv)

    def get_common_orbitals(self, other) -> list:
        """
        Returns a list of common occupied orbitals

        :param other: a Determinant to compare to
        """

        # Create a new bit string with a 1 on places where both old ONVs
        # are occupied
        common_onv_alpha = self._alpha_onv & other._alpha_onv
        common_onv_beta = self._beta_onv & other._beta_onv

        # Convert bistring to list
        common_list_alpha = Determinant.onv_to_orbitals(common_onv_alpha)
        common_list_beta = Determinant.onv_to_orbitals(common_onv_beta)

        # returns the mixed list
        return Determinant.to_spin_orbitals(common_list_alpha, common_list_beta)

    def get_doubly_occupied_orbitals(self) -> list:
        """
        Returns a list of doubly occupied orbitals
        """
        return Determinant.onv_to_orbitals(self._alpha_onv & self._beta_onv)

    def get_sign(self, alpha_orbitals=[], beta_orbitals=[]):
        """
        Returns the sign resulting from orbital rotation

        :param alpha_orbitals: alpha orbitals rotated to the front
        :param beta_orbitals: beta orbitals rotated to the front
        """

        # Find where the orbitals are in the determinant
        alpha_pos = Determinant.get_position(self._alpha_occ, alpha_orbitals)
        beta_pos = Determinant.get_position(self._beta_occ, beta_orbitals)

        sign = 1

        # Compute how many rotations needs to be done
        for i in range(len(alpha_pos)):
            # The number of rotations are reduced by the index because
            # there are already i orbitals move to the front.
            # If the number of rotations is odd, multiply the sign by -1
            if (alpha_pos[i] - i) % 2 == 1:
                sign *= -1

        # Same is done for beta
        for i in range(len(beta_pos)):
            if (beta_pos[i] - i) % 2 == 1:
                sign *= -1

        return sign

    def get_sign_spin_orbital(self, orbital):

        pos = Determinant.get_position(self.get_spin_orbitals(), [orbital])

        return 1 if pos[0] % 2 == 0 else -1

    def get_different_orbitals(self, other):
        """
        Returns a list of orbitals that are different between onv1 and onv2
        """

        # Get list of orbitals that are different between the determinants
        diff_alpha_1, diff_alpha_2 = Determinant._different_bits_to_orbitals(
            self._alpha_onv, other.alpha_onv
        )

        diff_beta_1, diff_beta_2 = Determinant._different_bits_to_orbitals(
            self._beta_onv, other.beta_onv
        )

        # Compute sign for orbital rotation
        sign_1 = self.get_sign(diff_alpha_1, diff_beta_1)
        sign_2 = other.get_sign(diff_alpha_2, diff_beta_2)

        # Convert orbital indices to spin orbitals list
        spin_orb_1 = Determinant.to_spin_orbitals(diff_alpha_1, diff_beta_1)
        spin_orb_2 = Determinant.to_spin_orbitals(diff_alpha_2, diff_beta_2)

        return spin_orb_1, spin_orb_2, sign_1 * sign_2
