import numpy as np
from scipy.linalg import eigh
from chilli_py.constants import ANG2BOHR, BOHR2ANG
from chilli_py.atoms import Atoms
from chilli_py.RKS import RKS, eval_RKS 
from chilli_py.utils import myprint 
from chilli_py.integrals import get_E, get_J, dmat
from chilli_py.exc import lda_slater_spin_x, lda_vwn_spin_c, func_pol
from chilli_py.alias import ortho
from chilli_py.bench import Ne, CH4, H2O 

class RFLO: 
    """
        RFLO class. 
        Construction of Fermi-orbitals (FOs) 
        and Fermi-Lowedin orbitals (FLOs). 

        Input 
            - atoms: Atoms()
            - fods: Atoms() 
            - mf_init: None or e.g. RKS() 

        References
            - PyFLOSIC2, RFLO.py 
    """
    def __init__(self,atoms,fods,mf_init=None):
        """
            __init__
            Initialize an instance of the class. 
        """
        self.atoms = atoms 
        self.fods = fods 
        # Initialization of mf 
        self._init_mf(mf_init)
        # For RKS 
        self.Nelec= self.mf.atoms.Nelec
        self.Nclosed,self.Nopen = divmod(int(self.Nelec),2)
        # Restricted calculation 
        self.nspin = 1 
        self.nks = (np.array(self.mf.D).shape)[1]
        self.occup = self.mo_occ 
        self.nksocc = self._get_nksocc()
        self.ham_sic = "HOOOV" 

    def _init_mf(self,mf_init): 
        """
            _init_mf
            Initialization of the iternal mf object. 
            In the common sense mf is a RKS object. 
        """
        if mf_init is None: 
            mf = RKS(self.atoms)
            mf.kernel() 
            self.mf = mf 
        if mf_init is not None: 
            self.mf = mf_init 

    @property
    def mo_occ(self):
        """
            mo_occ
            Evaluate occupation. 
        """
        Nclosed,Nopen = divmod( int(self.atoms.Nelec), 2 )
        mo_occ = np.zeros(len(self.mf.basis))
        mo_occ[:Nclosed] += 2
        return mo_occ

    def _get_nksocc(self): 
        """
            _get_nksocc
            Get number of occupied Kohn-Sham states. 
        """
        nksocc = np.zeros([1],dtype=int)
        for i in range(0, self.nks):
            if int(self.occup[i]) != int(0):
                nksocc[0] += 1
        return nksocc

    def _basis_at_coords(self,coords):
        """
            _basis_at_coords
            Evaluate basis on grid. 
        """
        bfs = self.mf.basis.basis
        npts = len(coords)
        nbf = len(bfs)
        basis_ongrid = np.zeros((npts,nbf))
        for j,bf in enumerate(bfs):
            for i,(coord) in enumerate(coords):
                basis_ongrid[i,j] = bf.eval(coord)
        return basis_ongrid
    
    def _basisgrad_at_coords(self,coords):
        """
            _basisgrad_at_coords
            Evaluate gradient of basis functions on grid. 

            Needed by 
                - _get_FOD_FORCES
        """
        bfs = self.mf.basis.basis
        npts = len(coords)
        nbf = len(bfs)
        basisgrad_ongrid = np.zeros((3,npts,nbf))
        for j,bf in enumerate(bfs):
            for i,(coord) in enumerate(coords):
                basisgrad_ongrid[:,i,j] = bf.grad(coord)
        return basisgrad_ongrid


    def _get_PSI(self,fods,U):
        """
            _get_PSI 
            Calculate the values of the 
            basis functions in real space 
            at the coordinates of the FODs (ai),
            e.g., PSI(ai). 
        """
        ao1 = self._basis_at_coords(fods.pos)
        psi_ai_1 = np.dot(ao1,U)
        psi_ai_work = np.zeros((fods.Nelec, self.nksocc[0]))
        l = 0
        # Iterate over the occupied Kohn-Sham wf.
        for i in range(0, self.nks):
            if int(self.occup[i]) != int(0):
                # Iterate over the FODs.
                for k in range(0,fods.Nelec):
                    psi_ai_work[k, i] = psi_ai_1[k, i]
                l = l + 1
        return psi_ai_work 

    def _get_R(self,fods):
        """
            _get_R
            Calculate the rotation matrix R. 
        """
        # Init the rotation matrix.
        R = np.zeros((self.nks, self.nks))
        for i in range(0,self.nks):
            R[i, i] = 1.0
        # Get SUMPsi_ai (density at every point = fod)
        SUMPsi_ai = np.zeros((fods.Nelec))
        for m in range(0,fods.Nelec):
            SUMPsi_ai[m] = np.sqrt(np.sum((self.PSI[m, :])**2))
        # Build the rotation matrices.
        for m in range(0,fods.Nelec):
            for i in range(0,fods.Nelec):
                R[m, i] = self.PSI[m, i] / SUMPsi_ai[m]
        return R 

    def _get_FO(self,fods,U): 
        """
            _get_FO
            Transform Kohn-Sham orbitals to Fermi-orbitals (FOs). 
        """
        fo = np.zeros((self.nks, self.nks))
        # Apply the rotation to the occupied orbitals.
        for i in range(0,fods.Nelec):
            for j in range(0,fods.Nelec):
                fo[:, i] = fo[:, i] + self.R[i, j] * U[:, j]
        # Copy the unoccupied orbitals.
        for i in range(fods.Nelec,self.nks):
            fo[:, i] = U[:, i].copy()
        return fo 

    def _get_FLO(self,fods):
        """
            _get_FLO
            Transform Fermi-orbitals (FOs) 
            into Fermi-Lowedin orbitals (FLOs).
        """
        flo = np.zeros((self.nks, self.nks))
        # sfo is needed in order to determine the overlap matrix.
        sfo = np.zeros((self.nks, self.nks))
        # Initialize everything for the Loewdin orthonormalization.
        T_lo = np.zeros((fods.Nelec,fods.Nelec))
        Q_lo = np.zeros((fods.Nelec))
        if self.fods.Nelec > 0: 
            # Initialize the overlap of the FOs.
            ovrlp_fo = np.zeros((fods.Nelec,fods.Nelec))
            # Get the overlap.
            # The atomic overlap is directly included in sfo.
            sroot = np.linalg.cholesky(self.mf.S)
            sfo[:, :] = np.dot(np.transpose(sroot), self.FO[:, :])
            ovrlp_fo[0:fods.Nelec, 0:fods.Nelec] = np.dot(np.transpose(sfo[:, 0:fods.Nelec]), sfo[:, 0:fods.Nelec])
            # This is a Loewdin symmetric orthonormalization.
            q_fo, v_fo = np.linalg.eigh(ovrlp_fo)
            T_lo[0:fods.Nelec, 0:fods.Nelec] = v_fo
            Q_lo[0:fods.Nelec] = q_fo
            one_div_d = (1.0 / np.sqrt(q_fo)) * np.eye(fods.Nelec)
            vinv_fo = (np.transpose(v_fo))
            tra1 = np.dot(v_fo, one_div_d)
            trafo = np.dot(tra1, vinv_fo)
            for j in range(0,fods.Nelec):
                for i in range(0,fods.Nelec):
                    flo[:, j] = trafo[i, j] * self.FO[:, i] + flo[:, j]
            # For the unoccupied orbitals copy the FOs (and therefore the KSO).
            for i in range(fods.Nelec, self.nks):
                flo[:, i] = self.FO[:, i].copy()
        return flo 

    def _get_D(self,U,nocc):
        """
            _get_D 
            Get the density matrix. 
        """
        D = np.dot(U * nocc, U.T.conj())
        return D 

    def _get_Exc(self,D):
        """
            get_Exc
            Get exchange-correlation (xc) energy Exc and potential matrix Vxc.
        """
        rhoa = self.mf.grids.get_rho(D)
        #rhoa = np.ma.masked_where(rhoa == 0,rhoa) 
        #rhoa[~np.isfinite(rhoa)] = 0
        fx, vxa, vxb, fc, vca, vcb = func_pol[self.mf.xc_name].kernel(rho=rhoa,zeta=np.ones_like(rhoa)) 
        Exc = np.dot(self.mf.grids.weights,1*fx+fc)
        Vxc = np.einsum('g,g,gI,gJ->IJ',self.mf.grids.weights,vxa+vca,self.mf.grids.basis_ongrid,self.mf.grids.basis_ongrid)
        return Exc, Vxc

    def _get_veff(self,D):
        """
            _get_veff 
            Get the effective potential Veff. 
        """
        J =get_J(D,self.mf.ERI)
        Ecoul = 1/2.*get_E(J,D/2.)
        
        Exc,Vxc = self._get_Exc(D/4.)  
        # SS: changed 2J to 1/2J while comparing with PyPZSIC 
        Veff = Vxc + 1/2.*J 
        return Veff, 2*Exc, Ecoul

    def _get_EKS(self,U): 
        """
            _get_EKS
            Calculate Kohn-Sham (KS) energy and Fockian 
            for given total density matrix D
            constructed from given U.
        """
        D = dmat(U,self.Nclosed)
        EKS,HKS = eval_RKS(self.mf.ERI,
                           self.mf.Hcore,
                           self.mf.xc,
                           self.mf.Enuc,
                           D,verbose=False) 
        return EKS,HKS 

    def _get_ESIC(self,fods,U):
        """
            _get_ESIC 
            Get the SIC energy ESIC. 

            Notes: 
              - Assumes that _get_EKS was called before. 
        """
        Exc = 0.0
        Ecoul = 0.0
        nelec = 0.0 
        # The variables vsics and onedm save the contributions of the orbitals themselves.
        vsics = np.zeros((fods.Nelec, self.nks, self.nks))
        onedm = np.zeros((fods.Nelec, self.nks, self.nks))
        # Get the SIC for every orbital.
        for j in range(0, fods.Nelec):
            # Build the occupancy array in order to get one electron densities.
            occup_work = np.zeros_like(self.occup)
            for i in range(0,self.nks):
                if i == j:
                    occup_work[i] = 2.
            # Build the one electron densities.
            dm_work = self._get_D(U, occup_work)
            onedm[j] = dm_work
            veff_work, exc_work, ecoul_work = self._get_veff(dm_work)
            vsics[j] = veff_work 
            Exc += exc_work 
            Ecoul += ecoul_work 
        SIE = Ecoul + Exc
        Etot = self.EKS - SIE
        return Etot, SIE, Exc, Ecoul, vsics, onedm 

    def _get_HSIC(self,fods,U):
        """
            _get_HSIC
            Get the SIC Hamiltonian and eigenvalues.
   
            Input
                - U, typically, FLO 
    
            Output
                - HSIC : SIC Hamiltonian
                - Eigs : Eigenvalues FLOs
                - lambda_ij: input for the FOD forces
        """
        # First, initialize all variables.
        h_sic = np.zeros((self.nks, self.nks))
        h_sic_virtual = np.zeros((self.nks, self.nks))
        v_virtual = np.zeros((self.nks, self.nks))
        sumpfs = np.zeros((self.nks, self.nks))
        lambda_ij = np.zeros((fods.Nelec,fods.Nelec))
        # Bra and Ket are useful for doing scalar products using matrix multiplication.
        ket = np.zeros((self.nks, 1))
        bra = np.zeros((1, self.nks))
        # v_virtual is the projector of the virtual subspace
        # that might be needed depending 
        # on which unified hamiltonian approximation is used.
        if fods.Nelec>0:
            for i in range(fods.Nelec, self.nks):
                bra[0, :] = np.transpose(U[:, i])
                ket[:, 0] = (U[:, i])
                v_virtual = v_virtual + np.dot(ket, bra)
        # Get epsilon^k_kl, here named lambda to avoid confusion. 
        # This is needed for the forces.
        for j in range(fods.Nelec):
            for i in range(fods.Nelec):
                bra[0, :] = np.transpose(U[:, i])
                ket[:, 0] = (U[:, j])
                right = np.dot(self.vsics[j], ket)
                lambda_ij[i, j] = -np.dot(bra, right)
        # Do the energy eigenvalue correction and the SIC Hamiltonian.
        sumpfs[:, :] = 0.0
        if fods.Nelec>0:
            for i in range(0,fods.Nelec):
                # HOO
                ps = np.dot(self.onedm[i] / 2.0, self.mf.S)
                pf = np.dot(self.onedm[i] / 2.0, self.vsics[i]) 
                fps = np.dot(self.vsics[i], ps)
                spf = np.dot(self.mf.S, pf)
                h_sic = h_sic + fps + spf
                # HOOOV
                pfp = np.dot(pf, self.onedm[i] / 2.0) 
                fp = np.dot(self.vsics[i], self.onedm[i] / 2.0)  
                vfp = np.dot(v_virtual, fp)
                pfv = np.dot(pf, v_virtual)
                sumpf = pfp + vfp + pfv
                sumpfs = np.dot(sumpf, self.mf.S) + sumpfs
                # Get the SIC Hamiltonian.
                h_sic = -0.5 * h_sic
                h_sic_virtual = -np.dot(self.mf.S,sumpfs)
        # Get the SIC eigenvalues.
        if self.ham_sic == 'HOO':
            HSIC = h_sic
        if self.ham_sic == 'HOOOV':
            HSIC = h_sic_virtual
        HPZ = self.HKS + HSIC
        Eigs, _ = eigh(HPZ, self.mf.S)
        return HPZ, Eigs, lambda_ij

    def _get_FOD_FORCES(self,fods,U):
        """
            _get_FOD_FORCES
            Calculate the FOD forces.
            
            Note
                - This is the orginal LF implementation (PyFLOSIC@GitHub)

            Needs
                - the posibility to evalute gradients of basis functions 
                  on the grid, see _basisgrad_at_coords

            Output
                - fforce : FOD forces
        """
        # Initialize the forces.
        fforce = np.zeros((fods.Nelec, 3))
        fforce_output = np.zeros((fods.Nelec, 3))
        # gradpsi_ai holds the nabla KS value at the FOD position. Dimensions:
        # (FOD index (i) x KS index (alpha) x 3.
        gradpsi_ai = np.zeros((fods.Nelec, self.nksocc[0],3))
        # den_ai holds the density at the FOD positions, grad_ai holds nabla rho at the FOD positions.
        den_ai = np.zeros((fods.Nelec))
        grad_ai = np.zeros((fods.Nelec, 3))
        # gradfo holds the gradients of the fermi orbitals. The dimensions are:
        # (coefficients x FOD Index x components (x,y,z)
        gradfo = np.zeros((self.nks,fods.Nelec, 3))
        # The sum over the gradients of KSO at the positions a_i. The dimensions are:
        # (coefficients x FOD Index (i) x components (x,y,z))
        # sumgradpsi = numpy.zeros((p.nks, numpy.max(p.nfod), 3), dtype=p.datatype)
        # gradovrlp holds the derivative of the overlap matrix. The dimension are:
        # (nfod (i) x nfod (j) x components (x,y,z)).
        # However, only for i=j it is unequal to zero. it might be reasonable to cut this
        # structure down later, in order to save computational space.
        gradovrlp = np.zeros((fods.Nelec,fods.Nelec, 3))
        # Delta1 and Delta3 as defined in the papers concering FOD forces.
        # They have the dimension:
        # (nfod (l) x nfod (k) x nfod(m) x components (x,y,z)).
        # Delta1 = numpy.zeros((numpy.max(p.nfod), numpy.max(p.nfod), numpy.max(p.nfod), 3), dtype=p.datatype)
        # Delta3 = numpy.zeros((numpy.max(p.nfod), numpy.max(p.nfod), numpy.max(p.nfod), 3), dtype=p.datatype)
        # eps holds the matrix elements lambda_ij. It has the dimensions:
        # (nfod (l) x nfod(k))
        eps = np.zeros((fods.Nelec,fods.Nelec))
        # Fermi orbital overlap matrix.
        s_i_j = np.zeros((fods.Nelec,fods.Nelec))
        # Cholesky decomposition of the atomic overlap matrix.
        sroot = np.zeros((fods.Nelec,fods.Nelec))
        # Cholesky decomposition for the atomic overlap matrix.
        sroot = np.linalg.cholesky(self.mf.S)
        # Assign epsilon.
        eps[0:fods.Nelec, 0:fods.Nelec] = self.lambda_ij[0:fods.Nelec, 0:fods.Nelec]
        # Get the value of the gradients of the KSO at the FOD positions.
        ao1 = self._basisgrad_at_coords(fods.pos)
        #print(f"basisgrad at fods: {ao1}")
        gradpsi_ai_1 = [x.dot(U) for x in ao1]
        # Rearrange the data to make it more usable.
        x_1 = gradpsi_ai_1[0]
        y_1 = gradpsi_ai_1[1]
        z_1 = gradpsi_ai_1[2]
        # No iteration over spin
        l = 0
        # Iterate over the Kohn sham wf.
        for i in range(0, self.nks):
            if self.occup[i] != 0.0:
                # Iterate over the fods.
                for k in range(0,fods.Nelec):
                    gradpsi_ai[k, l, 0] = x_1[k][i]
                    gradpsi_ai[k, l, 1] = y_1[k][i]
                    gradpsi_ai[k, l, 2] = z_1[k][i]
                l = l + 1
            if l > self.nksocc:
                print('WARNING: Attempting to use not occupied KS wf for FLOSIC.')
        # Calculate the density and the gradient of the density from the KS wavefunctions.
        for m in range(0,fods.Nelec):
            den_ai[m] = np.sum((self.PSI[m, :])**2) 
        for r in range(0,3):
            for m in range(0,fods.Nelec):
                for a in range(0,fods.Nelec):
                    grad_ai[m, r] = grad_ai[m, r] + 2. * self.PSI[m, a] * gradpsi_ai[m, a, r]
        # sfo and sks hold the FO and KSO after the decomposed atomic overlap has been
        # included.
        sks = np.zeros((self.nks, self.nks))
        sfo = np.zeros((self.nks, self.nks))
        # Get the gradients of the Fermi orbitals. 
        # NOTE: NOT THE FERMI LOEWDIN ORBITALS!
        # This is dF in the usual notation.
        # Fill sks and sfo.
        sks[:, :] = np.dot(np.transpose(sroot), U[:, :])
        sfo[:, :] = np.dot(np.transpose(sroot), self.FO[:, :])
        # Get dF.
        for r in range(0, 3):
            for i in range(0,fods.Nelec):
                sum1 = np.zeros((self.nks))
                for a in range(0,fods.Nelec):
                    sum1 = gradpsi_ai[i, a, r] * sks[:, a] + sum1
                gradfo[:, i, r] = sum1[:] / np.sqrt(den_ai[i]) - (sfo[:, i] * grad_ai[i, r]) / (2. * den_ai[i])
        # Calculate the forces.
        # Now the actual calculation.
        # It is done as a loop over the spin.
        if fods.Nelec > 0:
            # Get the overlap matrix. 
            s_i_j = np.zeros((fods.Nelec,fods.Nelec))
            s_i_j[0:fods.Nelec, 0:fods.Nelec] = np.dot(np.transpose(sfo[:, 0:fods.Nelec]), sfo[:, 0:fods.Nelec])
            # Get the eigenvectors
            Q_alpha_tmp, T_alpha_tmp = eigh((s_i_j[0:fods.Nelec, 0:fods.Nelec]))
            T_alpha = np.zeros((fods.Nelec,fods.Nelec))
            Q_alpha = np.zeros((fods.Nelec))
            # Resort the matrices
            for i in range(0,fods.Nelec):
                for j in range(0,fods.Nelec):
                    T_alpha[j,fods.Nelec - 1 - i] = T_alpha_tmp[j, i]
                    Q_alpha[fods.Nelec - 1 - i] = Q_alpha_tmp[i]
            T_alpha = np.transpose(T_alpha)
            # Temporary variables.
            TdST = np.zeros((fods.Nelec,fods.Nelec,fods.Nelec,3))
            V_tmp = np.zeros((fods.Nelec))
            M_tmp = np.zeros((fods.Nelec,fods.Nelec))
            D1_km = np.zeros((fods.Nelec,fods.Nelec,fods.Nelec,3))
            D1_kmd = np.zeros((fods.Nelec,fods.Nelec,fods.Nelec,3))
            D3_km = np.zeros((fods.Nelec,fods.Nelec,fods.Nelec,3))
            D3_kmd = np.zeros((fods.Nelec,fods.Nelec,fods.Nelec,3))
            # Get dS.
            for r in range(0, 3):
                for n in range(fods.Nelec):
                    for m in range(fods.Nelec):
                        gradovrlp[n, m, r] = np.dot(np.transpose(sfo[:, n]), gradfo[:, m, r])
                # Get Matrix elements <T_j|dSdAm|T_k>.
                for m in range(fods.Nelec):
                    for a in range(fods.Nelec):
                        for b in range(fods.Nelec):
                            for i in range(fods.Nelec):
                                TdST[b, a, m, r] = TdST[b, a, m, r] + gradovrlp[i, m, r] * \
                                    (T_alpha[b, i] * T_alpha[a, m] + T_alpha[b, m] * T_alpha[a, i])
                # Get <phi|D1,km>
                V_tmp[0:fods.Nelec] = 1. / np.sqrt(Q_alpha[0:fods.Nelec])
                M_tmp = np.zeros((fods.Nelec,fods.Nelec))
                M_tmp2 = np.zeros((fods.Nelec,fods.Nelec))
                for m in range(fods.Nelec):
                    for k in range(fods.Nelec):
                        M_tmp[m, k] = np.sum(T_alpha[0:fods.Nelec, k] * T_alpha[0:fods.Nelec, m] * V_tmp[0:fods.Nelec])
                M_tmp2 = np.dot(M_tmp[0:fods.Nelec, 0:fods.Nelec], gradovrlp[0:fods.Nelec, 0:fods.Nelec, r])
                for m in range(0,fods.Nelec):
                    for k in range(0,fods.Nelec):
                        for l in range(0,fods.Nelec):
                            D1_km[l, k, m, r] = D1_km[l, k, m, r] + M_tmp[m, k] * M_tmp2[l, m]
                # Get D1_kmd (the lower case d meaning delta).
                for m in range(fods.Nelec):
                    D1_kmd[0:fods.Nelec,0:fods.Nelec, m, r] = D1_km[0:fods.Nelec,0:fods.Nelec, m, r] - \
                        np.transpose(D1_km[0:fods.Nelec,0:fods.Nelec, m, r])
                # Get the first part of the forces.
                for m in range(fods.Nelec):
                    for k in range(fods.Nelec):
                        for l in range(fods.Nelec):
                            fforce[m, r] = fforce[m, r] + D1_kmd[l, k, m, r] * eps[l, k]
                # Get D3_km.
                for m in range(fods.Nelec):
                    for k in range(fods.Nelec):
                        for l in range(fods.Nelec):
                            for a in range(fods.Nelec):
                                for b in range(fods.Nelec):
                                    tmp1 = T_alpha[b, k] * T_alpha[a, l] * np.sqrt(Q_alpha[a])
                                    tmp2 = T_alpha[a, k] * T_alpha[b, l] * np.sqrt(Q_alpha[b])
                                    tmp3 = (np.sqrt(Q_alpha[a]) + np.sqrt(Q_alpha[b])
                                            ) * np.sqrt(Q_alpha[a] * Q_alpha[b])
                                    D3_km[l, k, m, r] = D3_km[l, k, m, r] - 0.5 * \
                                        TdST[b, a, m, r] * ((tmp1 + tmp2) / tmp3)
                # Get D3_kmd (the lower case d meaning delta).
                for m in range(fods.Nelec):
                    D3_kmd[0:fods.Nelec,0:fods.Nelec, m, r] = D3_km[0:fods.Nelec, 0:fods.Nelec, m, r] - \
                        np.transpose(D3_km[0:fods.Nelec, 0:fods.Nelec, m, r])
                # Get the second part of the forces.
                for m in range(fods.Nelec):
                    for k in range(fods.Nelec):
                        for l in range(fods.Nelec):
                            fforce[m, r] = fforce[m, r] + D3_kmd[l, k, m, r] * eps[l, k]
        # Output the forces.
        fforce_output[0:fods.Nelec, :] = fforce[0:fods.Nelec, :]
        # Note: sign 
        fforce = -1 * fforce_output
        return fforce

    def kernel(self,verbose=False,fods=None,U=None): 
        """
            kernel 
            Run a full FLO-SIC construction 
            for a given set of orbitals U 
            (U -> density matrix D) and 
            a given set of Fermi-orbital 
            descriptors (FODs). 

            Run 
                - Transformation: KS -> FO
                - Transformation: FO -> FLO
                - Calculation: 
                    + ESIC
                    + HSIC, Eigs 
                    + fforces 
        """
        if fods is None:
            fods = self.fods 
        if U is None:
            U = self.mf.U
        print(f"FODs(FLO): {fods}")
        self.PSI = self._get_PSI(fods=fods,U=U)
        self.R = self._get_R(fods=fods)
        print(f"R : {self.R}") 
        self.FO = self._get_FO(fods=fods,U=U)
        self.FLO = self._get_FLO(fods=fods)
        print(f"FLO : {self.FLO}")
        self.EKS, self.HKS = self._get_EKS(U=U)
        self.Etot, self.SIE, self.Exc, self.Ecoul, self.vsics, self.onedm = self._get_ESIC(fods=fods,U=self.FLO) 
        self.HSIC, self.Eigs, self.lambda_ij = self._get_HSIC(fods=fods,U=self.FLO) 
        self.fforce = self._get_FOD_FORCES(fods=fods,U=U)
        if verbose > 3: 
            print(f"EKS: {self.EKS}") 
            print(f"SIC: Ecoul = {self.Ecoul} Exc = {self.Exc}")
            print(f"Etot(PZ-SIC): {self.Etot} SIE: {self.SIE}")
            print(f"Eigs: {self.Eigs}")
            print(f"HSIC: {self.HSIC}")
            print(f"fforce: {self.fforce}")
        return self.Etot, self.HSIC, self.fforce  
    
    def _get_energy(self,verbose=False,fods=None,U=None):
        """
            _get_energy
            Calculate EPZ energy.

            Run 
                - Transformation: KS -> FO
                - Transformation: FO -> FLO
                - Calculation: 
                    + ESIC
        """
        if fods is None:
            fods = self.fods
        if U is None:
            U = self.mf.U
        print(f"FODs(FLO,get_energy): {fods} \nU :{U}")
        self.PSI = self._get_PSI(fods=fods,U=U)
        self.R = self._get_R(fods=fods)
        self.FO = self._get_FO(fods=fods,U=U)
        self.FLO = self._get_FLO(fods=fods)
        self.EKS, self.HKS = self._get_EKS(U=U)
        self.Etot, self.SIE, self.Exc, self.Ecoul, self.vsics, self.onedm = self._get_ESIC(fods=fods,U=self.FLO)
        print(f"EKS: {self.EKS}")
        print(f"SIE: {self.SIE}")
        print(f"Etot: {self.Etot}")
        return self.Etot
    
    def _get_force(self,verbose=False,fods=None,U=None):
        """
            _get_force
            Calculate FOD forces, i.e, fforces. 

            Run
                - Calculation:
                    + HSIC, Eigs
                    + fforces
        """
        if fods is None:
            fods = self.fods
        if U is None:
            U = self.mf.U
        self.HSIC, self.Eigs, self.lambda_ij = self._get_HSIC(fods=fods,U=self.FLO)
        self.fforce = self._get_FOD_FORCES(fods=fods,U=U)
        return self.fforce 
    
def main():
    """
        main 
        Main function to test the functionality of the this routine. 
    """
    from chilli_py.bench import H2O, CH4, Ne, He, COH2,H2 
    atoms, fods = CH4() 
    mf = RKS(atoms,xc_name="LDA,VWN",basis_name="sto-3g")
    mf.kernel() 
    flo = RFLO(atoms,fods,mf_init=mf)
    flo.kernel(verbose=0)

if __name__ == "__main__": 
    main() 
