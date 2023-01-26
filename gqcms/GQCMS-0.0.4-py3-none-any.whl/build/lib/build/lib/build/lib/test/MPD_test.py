import gqcms
import numpy as np

def test_mpd():
    a = gqcms.Hubbard(3, t=1, U=2, circular=False)
    ham = a.Hamiltonian()
    df = gqcms.FCI(ham, states=0)
    wf = df["C"][0]
    mpd = gqcms.MPD(a, wf)
    domains = mpd.getDomainProbabilityDataFrame(nu=2, U_max=2, stepsize=1)
    mpd_frame = mpd.getMPDProbabilityDataFrame(domains)
    MPD_prob = mpd_frame[(0,1)][0]
    wf_prob = wf[0]**2 + wf[1]**2 + wf[3]**2 + wf[5]**2 + wf[8]**2
    assert np.isclose(MPD_prob, wf_prob), f"got {MPD_prob}, expected {wf_prob}"


if __name__ == "__main__":
    test_mpd()
    print("all clear")
