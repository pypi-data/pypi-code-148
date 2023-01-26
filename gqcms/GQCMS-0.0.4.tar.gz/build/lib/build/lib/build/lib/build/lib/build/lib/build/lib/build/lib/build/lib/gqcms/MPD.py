import numpy as np
from itertools import combinations
import pandas as pd
import scipy.linalg as sp
import heapq
from . import Hubbard
from gqcms.matrices import Determinant


class MPD:
    """
    Will calculate the Maximum probability domains in a given basis set in the Hubbard model.
    """

    def __init__(self, Hubbard_mol: Hubbard, coefs: np.ndarray):
        """
        Constructor for the MPD class
        Hubbard_mol, Hubbard object: the molecule you want to calculate the MPDs from
        coefs, nparray of floats: the coeffcients of the wavefunction in ONV basis
        sites, int: amount of sites in the Hubbard model.
        circular, bool: are you looking at a cyclic molecule, default True
        """
        self.basis = Hubbard_mol.basis
        self.coefs = coefs
        self.sites = Hubbard_mol.sites
        self.circular = Hubbard_mol.circular
        self.molecule = Hubbard_mol

        def domainCalculator(sites):
            """
            Will calculate all possible domains for the given molecule
            Returns array of arrays, with all domains
            """
            dom_list = []
            sites_list = range(sites)
            # creates all possible combinations of sites.
            for count in sites_list:
                dom_list += combinations(sites_list, count + 1)
            return dom_list

        self.domains = domainCalculator(self.sites)

    def getCoefsPerONV(self):
        """returns dict of ONVs as keys with their respective coefficient"""
        ziplist = zip(self.coefs, self.basis)
        coefs_per_ONV = {str(ONV): coef for coef, ONV in ziplist}
        return coefs_per_ONV

    def probabilityCalculator(self, nu=1):
        """
        Will calculate the probability of every possible domain
        returns dict (domain: its probability)
        nu, int: the amount of electrons in a domain
        """
        # initiate probability list
        prob_dict = []

        # generate all possible domains, with or without symmetry

        dom_list = self.domains
        dom_dict = {}
        # look at all the domains
        for domain in dom_list:
            probability = 0
            # turn domain into bitstring
            # can be compared via bitwise
            domain_bits = Determinant.orbitals_to_onv(domain)

            # we only want to save the 5 biggest ONVs for every domain
            # We will use a priorityqueue for this
            domain_parts = []
            heapq.heapify(domain_parts)

            # We will exclude any ONVs which are simply a swap of the
            # alpha and beta parts
            alpha_set, beta_set = set(), set()

            for index, ONV in enumerate(self.basis):
                # count the overlap of alpha and domain and beta and domain
                alpha_count = len(
                    Determinant.onv_to_orbitals(ONV._alpha_onv & domain_bits)
                )
                beta_count = len(
                    Determinant.onv_to_orbitals(ONV._beta_onv & domain_bits)
                )

                # amount of electrons has to be equal to nu
                if alpha_count + beta_count == nu:
                    # probability is linked to coef**2
                    probability += self.coefs[index] ** 2

                    # get the tuple with probability first for comparison
                    # then check if we save more then five
                    # if so, remove smallest element
                    candidate_pair = (self.coefs[index], str(ONV))
                    if not (ONV._alpha_onv in beta_set and ONV._beta_onv in alpha_set):
                        heapq.heappush(domain_parts, candidate_pair)
                        alpha_set.add(ONV._alpha_onv)
                        beta_set.add(ONV._beta_onv)
                    if len(domain_parts) > 5:
                        heapq.heappop(domain_parts)

            # we need all lists to have the same value
            while len(domain_parts) != 5:
                domain_parts.append((np.nan, np.nan))
            # we only the strings, the coef of each is stored elsewhere.
            dom_dict[str(domain)] = [ONV for prob, ONV in domain_parts]

            prob_dict.append(round(probability, 8))

        # zip together to link domain to probability
        prob_dict = zip(dom_list, prob_dict)
        prob_dict = {dom: prob for dom, prob in prob_dict}

        # prob_dict = probability per domain
        # dom_dict = 5 most important ONVs per domain
        return prob_dict, dom_dict

    @staticmethod
    def domainInverter(domain, sites):
        """Will return a list of values that are not in the domain"""
        inverted_domain = []
        domain_set = set(domain)
        for i in range(sites):
            if i not in domain_set:
                inverted_domain.append(i)
        return inverted_domain

    def getProbabilityDataFrame(self, prob_dict):
        """
        Will generate a DataFrame containing several interesting values for every domain
        prob_dict, dict: dict of domains and their probabilities

        dataframe structure
        collumns: 'domain' | 'probability' | 'bits' | 'unocc_list' |
        domain: list of sites in the domain
        probability: the probability value of the domain
        bits: the bitstring representation
        unocc_list: list of unoccupied sites
        """
        # The DataFrame allows for easy storage, manipulation and comparison of multiple values
        prob_df = pd.DataFrame.from_dict(
            prob_dict, orient="index", columns=["probability"]
        )
        prob_df.reset_index(inplace=True)
        prob_df.rename(columns={"index": "domain"}, inplace=True)

        # all domains can be represented as bitstrings.
        prob_df["bits"] = prob_df["domain"].apply(Determinant.orbitals_to_onv)

        # single site flips can be gotten from:
        # unnocupieds, add 2**(site n°) for all sites that are not part of the domain
        prob_df["unocc_list"] = prob_df["domain"].apply(
            MPD.domainInverter, args=[self.sites]
        )

        # occupieds, subtract 2**(site n°) for all occupied sites => already stored in domain

        return prob_df

    def getSingleSiteFlips(self, domain, prob_dict=False, prob_df=False):
        """
        Will generate all single site flips for a domain, and their corresponding probabilities.
        domain, list of ints, the list representation of the domain.
        prob_dict, dict: list of domains with their probability
        prob_df, pd.DataFrame: it is possible to pass the prob_df directly, in order to spare time.

        """
        if type(prob_df) == bool:
            prob_df = self.getProbabilityDataFrame(prob_dict)
        domain_row = prob_df[prob_df["domain"] == domain]
        single_flip_list = []
        # domain_row is now a pandas series that can be searched like a DataFrame
        # first we will look at the sites that are not in the domain
        for value in domain_row["unocc_list"].array[0]:
            single_flip = prob_df[
                prob_df["bits"] == domain_row["bits"].array[0] + 2**value
            ]
            single_flip_list.append(single_flip)
        for value in domain_row["domain"].array[0]:
            single_flip = prob_df[
                prob_df["bits"] == domain_row["bits"].array[0] - 2**value
            ]
            single_flip_list.append(single_flip)

        single_flip_frame = pd.concat(
            single_flip_list, ignore_index=True, axis=0, join="outer"
        )
        return single_flip_frame

    def MPDFinder(self, prob_dict):
        """
        Will find MPD's of a molecule at U/t from Hubbard object, the probabilities of all domains are stored elsewhere.
        prob_dict, dict: list of domains and their probabilities
        """
        # list will store tuples of MPD with its probability
        MPD_list = []
        prob_df = self.getProbabilityDataFrame(prob_dict)
        for index, domain in prob_df.iterrows():
            if domain["probability"] > 1e-5:
                single_flips = self.getSingleSiteFlips(
                    domain["domain"], prob_dict, prob_df=prob_df
                )
                if not np.any(single_flips["probability"] > domain["probability"]):
                    if np.any(single_flips["probability"] == domain["probability"]):
                        equals = single_flips[
                            single_flips["probability"] == domain["probability"]
                        ]
                        with pd.option_context("mode.chained_assignment", None):
                            equals["size"] = equals["unocc_list"].apply(
                                len
                            )  # reports SettingWithCopyWarning, but is a false positive (https://www.dataquest.io/blog/settingwithcopywarning/)
                        # We want to keep the MPDs as small as possible, meaning that the unocc_list is as large as possible
                        if not np.any(equals["size"] > len(domain["unocc_list"])):
                            MPD_list.append(domain["domain"])
                    else:
                        MPD_list.append(domain["domain"])

        return MPD_list

    def setGroundState(self, new_ground_state):
        """sets a new ground state"""
        self.coefs = new_ground_state

    def getDomainProbabilityDataFrame(
        self, nu=1, U_max=20, stepsize=1, potdict=False, get_ONV_coefs=False
    ):
        """
        Generates a dataframe with the domains as the columns and the U/t values as the rows
        nu, int: the amount of electrons in the domain, default 1
        U_max, float: the maximmum value of U, default = 20
        stepsize, float: the stepsize, default 1
        potdict, dict: {site:potential}, default False
        get_ONV_coefs, bool: do you want to get the coefficients of the individual ONVs as well, default False
        """
        # initialize dataframe
        dom_prob, ONVs_per_domain = self.probabilityCalculator(nu=nu)
        dom_prob_df = pd.DataFrame.from_dict([dom_prob])

        # piggyback ONV_coefs
        ONVcoefs = self.getCoefsPerONV()
        ONV_coef_df = pd.DataFrame.from_dict([ONVcoefs])

        # change U/t and add the coefficients to the dataframe
        # we will start from the minimal value of U in the Hubbard object
        ut_list = (
            np.arange(self.molecule.U, U_max + stepsize, stepsize)
        )
        for U in ut_list[1:]:
            self.molecule.U = U
            self.molecule.onSiteRepulsionMatrix = self.molecule.OnSiteRepulsion()
            ham = self.molecule.Hamiltonian()

            E, C = sp.eigh(ham)
            self.setGroundState(C[:, 0])
            dom_prob, ONVs_per_domain = self.probabilityCalculator(nu=nu)
            dom_prob = pd.DataFrame.from_dict([dom_prob])
            dom_prob_df = pd.concat((dom_prob_df, dom_prob), axis=0, ignore_index=True)

            ONVcoefs = self.getCoefsPerONV()
            ONVcoefs = pd.DataFrame.from_dict([ONVcoefs])
            ONV_coef_df = pd.concat((ONV_coef_df, ONVcoefs), axis=0, ignore_index=True)
        dom_prob_df["U/t"] = ut_list
        ONV_coef_df["U/t"] = ut_list
        if get_ONV_coefs:
            return dom_prob_df, ONV_coef_df
        return dom_prob_df

    def getMPDProbabilityDataFrame(self, dom_prob_df):
        """
        Will generate a dataframe with the MPDs as the columns, and U/t as the rows
        dom_prob_df pd.DataFrame: dataframe as generated by the getDomainProbabilityDataFrame method
        """
        # intitialising indices to correct values
        MPD_dict = {}
        for row in dom_prob_df.iterrows():
            prob_dict = row[1].to_dict()
            prob_dict.pop("U/t")
            MPD_list = self.MPDFinder(prob_dict)
            # set for membership checks
            MPD_set = set(MPD_list)
            for domain in MPD_list:
                if domain not in MPD_dict.keys():
                    # dict entry will hold beginning and end points of MPDs
                    MPD_dict[domain] = [row[1].name, "ongoing"]
            for domain in MPD_dict.keys():
                if domain not in MPD_set and MPD_dict[domain][1] == "ongoing":
                    MPD_dict[domain][1] = row[1].name

        MPD_df = dom_prob_df.loc[:, MPD_dict.keys()]
        MPD_df["U/t"] = dom_prob_df.loc[:, "U/t"]
        for key in MPD_dict.keys():
            if MPD_dict[key][0] != 0:
                MPD_df[key][: MPD_dict[key][0]] = np.nan
            if MPD_dict[key][-1] != "ongoing":
                MPD_df[key][MPD_dict[key][-1] :] = np.nan

        return MPD_df


# def MPDPlotter(sites, electrons, nu, U_max, domains, t=1.0, pot_dict={}, circular=True, step_size=1.0):
#     """
#     Support function to allow for the plotting of MPDs over a U/t range
#     sites, int: the amount of sites in the molecule
#     electrons, tuple of ints: the amount of alpha and beta electrons (alpha, beta)
#     nu, int, amount of electrons in the domain
#     U_max, int: the maximum U that needs to be plotted
#     domains, list of tuples: the domains you want to study
#     t, float: the hopping parameter, default 1.0
#     pot_dict, dict{int:float}: dict that holds potentials that need top be applied in ionic Hubbard, default empty dict
#     circular, bool: True if molecule is cyclic, default True
#     check_con, bool: check whether the MPD is continuous or not, default=True
#     step_size, float: the size of U/t steps required, default = 1
#     """
#     # dictionary will hold the probabilities for every domain as a list
#     dom_dict = {}
#     for domain in domains:
#         dom_dict[domain] = []
#     U_t_list = np.arange(0, U_max, step_size)

#     # setting up some values for time saving
#     benzene = Hubbard(sites, electrons, t, 0)
#     hamiltonian = benzene.constructHubbardHamiltonian(benzene.constructAdjacencyMatrix(circular=circular))
#     E, C = sp.eigh(hamiltonian)
#     Hubbard_ground_state = C[:,0]
#     benzene_MPD = MPD(benzene.detList, Hubbard_ground_state, benzene.sites)

#     for U in U_t_list:
#         benzene.setU(U)
#         # we will apply a potential of 5 to site 0
#         hamiltonian = benzene.constructHubbardHamiltonian(benzene.constructAdjacencyMatrix(circular=circular))
#         if pot_dict:
#             hamiltonian += benzene.applyPotential(pot_dict)
#         E, C = sp.eigh(hamiltonian)
#         Hubbard_ground_state = C[:,0]

#         # calculate MPDs
#         benzene_MPD.setGroundState(Hubbard_ground_state)
#         # the implemented symmetry considerations do not work with ionic Hubbard models
#         # as adding a potential breaks the molecular symmetry
#         probabilities, coef_dict, ONV_per_domain = benzene_MPD.probabilityCalculator(nu=nu)

#         MPDs = benzene_MPD.MPDFinder(probabilities)

#         MPD_dict = {domain:probability for domain, probability in MPDs}

#         # filling the dom_dict => will help us plot later
#         for key in dom_dict.keys():
#             if key in MPD_dict.keys():
#                 dom_dict[key].append(MPD_dict[key])
#             else:
#                 dom_dict[key].append(np.nan)


#     return dom_dict
