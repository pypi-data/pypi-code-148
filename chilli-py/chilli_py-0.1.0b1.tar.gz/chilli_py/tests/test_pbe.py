import numpy as np
import numpy 
from pprint import pprint 
from chilli_py.bench import Benchmark, Entry, small_bench
from chilli_py.exc import lda_slater_x, lda_pw_c, gga_pbe_x, gga_pbe_c
from chilli_py.utils import myprint 

from xcauto_pbe import pbex_n_gnn, pbec_n_gnn

def _rks_gga_wv0(rho, vxc, weight):
    """
        Needed by 
            - nr_rks
    """
    vrho, vgamma = vxc[:2]
    ngrid = vrho.size
    wv = numpy.empty((4,ngrid))
    wv[0]  = weight * vrho
    wv[1:] = (weight * vgamma * 2) * rho[1:4]
    wv[0] *= .5  # v+v.T should be applied in the caller
    return wv

def nr_rks(ni, mol, grids, xc_code, dms, relativity=0, hermi=0, max_memory=2000, verbose=None):
    """
        nr_rks

        Input 
            - ni, NumInt() instance 
            - mol, PySCF mol object 
            - grids, mf.grids instance or other grids instance 
            - dm, density matrix, e.g., dm = mf.make_rdm1() 
            - xc_code, str(), e.g., "LDA", "GGA" 

        Workflow 
            - 1) nuclei coords, basis -> mol 
            - 2) get the basis functions on the grid called atomic orbitals (ao) 
                
                    # For a GGA like PBE, derv=1 
                    ao = dft.numint.eval_ao(mol, mf.grids.coords, deriv=1)
            - 3) get the density and density derivatives on the grid 

                    # For a GGA like PBE, xctype="GGA"
                    #   + GGA, dim(rho) -> {density,density_dx, density_dy, density_dz}
                    rho = dft.numint.eval_rho(mol, ao, dm, xctype='GGA')
            - 4) get the exchange-correlation energy and potential 
                
                    #   GGA, dim(vxc) -> {number_of_electrons, exc_energy, potential'ish} 
                    vxc = mf._numint.nr_vxc(mol, mf.grids,xc, dm, spin=0)
                    # or using this routine for RKS 
                    vxc = nr_rks(mf._numint, mf.mol, mf.grids, "GGA", dm)
                    # The exchange-correlation energy simplified 
                    ret = chilli_pbe("Hans",rho)
                    exc_energy = np.dot((mf.grids.weights.T*rho[0]),ret[0])
                    # or 
                    mf = mf.define_xc_(chilli_pbe, 'GGA')
                    mf.kernel()

        Notes
            - for my test cases nset seems to be one 
            - for my test cases the for [--] ni.block_loop is only executed once 
                + one set of {weights,coords}
            - thus the overal complex double looping can be avoided for our cases 

        This is a (somehow) cleaned Python version of 
            - https://github.com/pyscf/pyscf/blob/master/pyscf/dft/numint.py#L775
            - started cleaning GGA part for PBE 
            - LDA and MGGA are uncleaned 
    """
    xctype = ni._xc_type(xc_code)
    make_rho, nset, nao = ni._gen_rho_evaluator(mol, dms, hermi)
    #print(f"nset: {nset}")
    shls_slice = (0, mol.nbas)
    ao_loc = mol.ao_loc_nr()

    nelec = numpy.zeros(nset)
    excsum = numpy.zeros(nset)
    if isinstance(dms, numpy.ndarray):
        vmat = numpy.zeros((nset,nao,nao), dtype=dms.dtype)
    else:
        vmat = numpy.zeros((nset,nao,nao), dtype=numpy.result_type(*dms))
    aow = None
    if xctype == 'LDA':
        ao_deriv = 0
        for ao, mask, weight, coords \
                in ni.block_loop(mol, grids, nao, ao_deriv, max_memory):
            aow = numpy.ndarray(ao.shape, order='F', buffer=aow)
            for idm in range(nset):
                rho = make_rho(idm, ao, mask, 'LDA')
                exc, vxc = ni.eval_xc(xc_code, rho, spin=0,
                                      relativity=relativity, deriv=1,
                                      verbose=verbose)[:2]
                vrho = vxc[0]
                den = rho * weight
                nelec[idm] += den.sum()
                excsum[idm] += numpy.dot(den, exc)
                # *.5 because vmat + vmat.T
                aow = numpy.einsum('pi,p->pi', ao, .5*weight*vrho, out=aow)
                #aow = _scale_ao(ao, .5*weight*vrho, out=aow)
                #vmat[idm] += _dot_ao_ao(mol, ao, aow, mask, shls_slice, ao_loc)
                vmat[idm] += numpy.dot(ao.T,aow)
                rho = exc = vxc = vrho = None
    elif xctype == 'GGA':
        #from pyscf.dft.numint import _rks_gga_wv0,_scale_ao,_dot_ao_ao
        ao_deriv = 1
        for ao, mask, weight, coords in ni.block_loop(mol, grids, nao, ao_deriv, max_memory):
            aow = numpy.ndarray(ao[0].shape, order='F', buffer=aow)
            for idm in range(nset):
                rho = make_rho(idm, ao, mask, 'GGA')
                exc, vxc = ni.eval_xc(xc_code, rho, spin=0,
                                      relativity=relativity, deriv=1,
                                      verbose=verbose)[:2]
                den = rho[0] * weight
                nelec[idm] += den.sum()
                excsum[idm] += numpy.dot(den, exc)
                # ref eval_mat function
                wv = _rks_gga_wv0(rho, vxc, weight)
                aow = numpy.einsum('npi,np->pi', ao, wv, out=aow)
                #aow = _scale_ao(ao, wv, out=aow)
                #vmat[idm] += _dot_ao_ao(mol, ao[0], aow, mask, shls_slice, ao_loc)
                vmat[idm] += numpy.dot(ao[0].T,aow)
                rho = exc = vxc = wv = None
    elif xctype == 'NLC':
        nlc_pars = ni.nlc_coeff(xc_code)
        ao_deriv = 1
        vvrho=numpy.empty([nset,4,0])
        vvweight=numpy.empty([nset,0])
        vvcoords=numpy.empty([nset,0,3])
        for ao, mask, weight, coords \
                in ni.block_loop(mol, grids, nao, ao_deriv, max_memory):
            rhotmp = numpy.empty([0,4,weight.size])
            weighttmp = numpy.empty([0,weight.size])
            coordstmp = numpy.empty([0,weight.size,3])
            for idm in range(nset):
                rho = make_rho(idm, ao, mask, 'GGA')
                rho = numpy.expand_dims(rho,axis=0)
                rhotmp = numpy.concatenate((rhotmp,rho),axis=0)
                weighttmp = numpy.concatenate((weighttmp,numpy.expand_dims(weight,axis=0)),axis=0)
                coordstmp = numpy.concatenate((coordstmp,numpy.expand_dims(coords,axis=0)),axis=0)
                rho = None
            vvrho=numpy.concatenate((vvrho,rhotmp),axis=2)
            vvweight=numpy.concatenate((vvweight,weighttmp),axis=1)
            vvcoords=numpy.concatenate((vvcoords,coordstmp),axis=1)
            rhotmp = weighttmp = coordstmp = None
        for ao, mask, weight, coords \
                in ni.block_loop(mol, grids, nao, ao_deriv, max_memory):
            aow = numpy.ndarray(ao[0].shape, order='F', buffer=aow)
            for idm in range(nset):
                rho = make_rho(idm, ao, mask, 'GGA')
                exc, vxc = _vv10nlc(rho, coords,
                                    vvrho[idm], vvweight[idm], vvcoords[idm], nlc_pars)
                den = rho[0] * weight
                nelec[idm] += den.sum()
                excsum[idm] += numpy.dot(den, exc)
# ref eval_mat function
                wv = _rks_gga_wv0(rho, vxc, weight)
                aow = numpy.einsum('npi,np->pi', ao, wv, out=aow)
                #aow = _scale_ao(ao, wv, out=aow)
                #vmat[idm] += _dot_ao_ao(mol, ao[0], aow, mask, shls_slice, ao_loc)
                vmat[idm] += numpy.dot(ao[0].T, aow)
                rho = exc = vxc = wv = None
        vvrho = vvweight = vvcoords = None
    elif xctype == 'MGGA':
        if (any(x in xc_code.upper() for x in ('CC06', 'CS', 'BR89', 'MK00'))):
            raise NotImplementedError('laplacian in meta-GGA method')
        ao_deriv = 2
        for ao, mask, weight, coords \
                in ni.block_loop(mol, grids, nao, ao_deriv, max_memory):
            aow = numpy.ndarray(ao[0].shape, order='F', buffer=aow)
            for idm in range(nset):
                rho = make_rho(idm, ao, mask, 'MGGA')
                exc, vxc = ni.eval_xc(xc_code, rho, spin=0,
                                      relativity=relativity, deriv=1,
                                      verbose=verbose)[:2]
                vrho, vsigma, vlapl, vtau = vxc[:4]
                den = rho[0] * weight
                nelec[idm] += den.sum()
                excsum[idm] += numpy.dot(den, exc)

                wv = _rks_gga_wv0(rho, vxc, weight)
                aow = numpy.einsum('npi,np->pi', ao[:4], wv, out=aow)
                #aow = _scale_ao(ao[:4], wv, out=aow)
                vmat[idm] += _dot_ao_ao(mol, ao[0], aow, mask, shls_slice, ao_loc)

# FIXME: .5 * .5   First 0.5 for v+v.T symmetrization.
# Second 0.5 is due to the Libxc convention tau = 1/2 \nabla\phi\dot\nabla\phi
                wv = (.5 * .5 * weight * vtau).reshape(-1,1)
                vmat[idm] += _dot_ao_ao(mol, ao[1], wv*ao[1], mask, shls_slice, ao_loc)
                vmat[idm] += _dot_ao_ao(mol, ao[2], wv*ao[2], mask, shls_slice, ao_loc)
                vmat[idm] += _dot_ao_ao(mol, ao[3], wv*ao[3], mask, shls_slice, ao_loc)

                rho = exc = vxc = vrho = wv = None
    elif xctype == 'HF':
        pass
    else:
        raise NotImplementedError(f'numint.nr_uks for functional {xc_code}')

    for i in range(nset):
        vmat[i] = vmat[i] + vmat[i].conj().T
    if nset == 1:
        nelec = nelec[0]
        excsum = excsum[0]
        vmat = vmat[0]
    return nelec, excsum, vmat

def get_exc(weights,rho,exc):
    """
        weights: mf.grids.weights
        rho    : rho = (rho,dx,dy,dz) 
        exc    : exc = (exc,(vrho,vlap), fxc, kxc)
    """
    #print(f"pyscf exc: {exc[0]} \n weights: {weights}")
    return np.dot((weights*rho[0]),exc[0])


def chilli_lda_pw(xc_code, rho, spin=1, relativity=0, deriv=1, verbose=None):
    """
        chilli_lda_pw
        This function provides an interface to use the Chilli LDA,PW 
        functional in PySCF. 

            rho = dft.numint.eval_rho(mol, ao, dm, xctype='LDA')
            ret = chilli_lda_pw("LDA,PW",rho)
            # or 
            mf = mf.define_xc_(chilli_lda_pw, 'LDA')
            mf.kernel()
    """
    # The PySCF internal variant would be somthing like this:

    # from pyscf import gto, scf, dft
    # # LDA
    # ret = dft.libxc.eval_xc('lda,pw', rho, spin, relativity, deriv, verbose)
    # return ret

    # SS: try to mask values close to zero. 
    rho = np.ma.masked_where(rho == 0,rho)
    fx, vx = lda_slater_x(rho)
    fc, vc = lda_pw_c(rho)
    # PySCF likes to have ex,ec NOT fx,fx!
    exc = (fx + fc)/rho
    vxc = vx + vc
    # SS: the structure of the output is important. 
    return exc, (vxc,None), None, None

def chilli_pbe(xc_code, rho, spin=1, relativity=0, deriv=1, verbose=None):
    """
        chilli_pbe
        This function provides an interface to use the Chilli PBE,PBE 
        functional in PySCF.

            rho = dft.numint.eval_rho(mol, ao, dm, xctype='GGA')
            ret = chilli_pbe("PBE,PBE",rho)
            # or
            mf = mf.define_xc_(chilli_pbe, 'GGA')
            mf.kernel()
    """
    # The PySCF internal variant would be somthing like this:

    # # PBE 
    # ret = dft.libxc.eval_xc('pbe,pbe', rho, spin, relativity, deriv, verbose)
    # return ret  

    # Get: rho, dx, dy, dz one grid 
    rho0, dx, dy, dz = rho[:4]
    #print(f"rho0: {rho0} \n dx : {dx} \n dy: {dy} \n dz: {dz}")
    vgamma = (dx**2 + dy**2 + dz**2)
    rho0 = np.ma.masked_where(rho0 == 0,rho0)
    vgamma = np.ma.masked_where(vgamma == 0,vgamma)

    # LDA part 
    fx, vx = lda_slater_x(rho0)
    fc, vc = lda_pw_c(rho0)
    # GGA part 
    fx1, vx1, vx2 = gga_pbe_x(rho=rho0,grho=vgamma)
    fc1, vc1, vc2 = gga_pbe_c(rho=rho0,grho=vgamma)
   
    Fx = fx/rho0 + fx1/rho0
    Fc = fc/rho0 + fc1/rho0
    Vx = vx + vx1 
    Vc = vc + vc1 
    exc = Fx + Fc
    vxc = Vx + Vc 
    vxc2 = (vx2 + vc2)/2.
    vrho = (vxc,vxc2)
    ret = (exc,vrho,None,None)

    # SS: if we want to use xcauto this would look like 

    # IMPORTANT: xcauto return fx = rho*ex, fc = rho*ec 
    #   fx2 = pbex_n_gnn(rho0,vgamma) 
    #   fc2 = pbec_n_gnn(rho0,vgamma)
    #   exc_xcauto = fx2/rho0 + fc2/rho0

    return ret 

def run_pyscf(f_xyz,xc):
    """
        run_pyscf 
        Run normal PySCF calculation and 
        a debugging calculation. 
    """
    # Indirect imports, b/c CI 
    from pyscf import gto, scf, dft
    print("RKS, PySCF")
    mol = gto.M(
                atom = f_xyz,
                basis = "sto3g",
                symmetry = False,
                 )

    mf = scf.RKS(mol)
    mf.xc = xc
    mf.verbose = 8
    # PySCF hides one SCF step in the initialization 
    mf.max_cycle = 299 #99 # maxiter -1 
    mf.conv_tol = 1e-12
    # With or without DIIS 
    #mf.diis = None
    # Use Hcore as inital guess for Fockian. 
    mf.init_guess = '1e'
    # We do not like pruning. 
    mf.grids.prune = None
    mf.grids.radi_method = dft.radi.gauss_chebyshev #dft.radi.becke
    mf.grids.radii_adjust = None
    mf.grids.atom_grid = (100,110)  #(2,6) #(2,6)  #(100,110) #(100,110) #(2,6)
    mf.grids.build()
    mf.kernel()
    etot1 = mf.e_tot 

    dm = mf.make_rdm1() 
    res = mf._numint.nr_vxc(mol, mf.grids, xc, dm, spin=0)
    

    # Eval with Chilli exc
    # Notes:
    #   - various variables in PBE can have different values 
    #   - I currently assume the final difference of 1e-6 comes from different variables 
    
    # Density and respective derivatives on the grid 
    # Rho, Dx, Dy, Dz = dft.numint.eval_ao(mol, mf.grids.coords, deriv=1)
    # LDA wrapper 
    if xc == "LDA,PW": 
        mf.xc = "LDA,PW"    
        mf = mf.define_xc_(chilli_lda_pw, 'LDA')
    # PBE wrapper 
    if xc == "PBE,PBE": 
        mf.xc = "PBE,PBE"   
        mf = mf.define_xc_(chilli_pbe, 'GGA')
    mf.kernel()
    dm = mf.make_rdm1()
    ao = dft.numint.eval_ao(mol, mf.grids.coords, deriv=1)
    RHO = dft.numint.eval_rho(mol, ao, dm, xctype='GGA')
    ret = chilli_pbe("Hans",RHO)
    res = mf._numint.nr_vxc(mol, mf.grids,xc, dm, spin=0)
    mf._numint.Hans_is_calling = "Okay"
    res2 = nr_rks(mf._numint, mf.mol, mf.grids, "GGA", dm)    
    print(res2)
    print(np.dot((mf.grids.weights.T*RHO[0]),ret[0]))
    print(get_exc(mf.grids.weights,RHO,ret))
    etot2 = mf.e_tot 
    print(f"DeltaE: {etot1-etot2}") 
    return etot1, etot2 

def run_chilli(f_xyz):
    """
        run_chilli 
        Run basic chilli_pyc calculation. 
    """
    from chilli_py.BasisSet import BasisSet
    from chilli_py.RKS_debug_grad import RKS
    from chilli_py.atoms import Atoms, atoms_from_xyz
    atoms = atoms_from_xyz(f_xyz)
    basis = BasisSet.initialize(atoms,basis_name="sto-3g")
    mf = RKS(atoms,"sto-3g",xc_name="PBE,PBE",grids=(100,110),maxiter=300) #(2,6))
    mf.verbose = False
    mf.kernel()
    return mf.Etot 

def test_rks(use_ref=True,xc="LDA,VWN"):
    """
        test_rks 
        Test RKS (with PBE support) routine. 
    """
    F = small_bench
    #F = {"He" : small_bench["He"]}
    #F = {"H2" : small_bench["H2"]}
    #F = {"Ne" : small_bench["Ne"]}
    #F = {"CH4" : small_bench["CH4"]}
    bench = Benchmark(f"xc: xc: {xc}")
    for key, f_xyz in F.items():
        print(f"system: {key} path: {f_xyz}")
        etot = run_chilli_py(f_xyz)
        etot_pyscf, etot_pyscf2 = run_pyscf(f_xyz,xc)
        #etot = run_chilli_py(f_xyz)
        e = Entry(f'{key}',etot,etot_pyscf)
        bench.add(e)
    bench.show()
    ME, MAE, RMSD = bench.analyze()
    if not use_ref:
        pprint(bench.get_dict())
    assert MAE < 5e-6
    print("tests@xc: sucessfully done!")


if __name__ == '__main__':
    #test_rks(use_ref=False,xc="LDA,PW")
    test_rks(use_ref=False,xc="PBE,PBE")

