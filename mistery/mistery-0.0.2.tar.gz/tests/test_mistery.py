import mistery
import numpy as np
import unittest

class TestMistery(unittest.TestCase):

    def test_interpolate(self):
        FeH = -0.1238923

        ts = np.round(np.random.uniform(low=0.5, high=2.5, size=3), 5)
        isos = mistery.get_isochrones(ts=ts, FeH=FeH, Av=0.1, photometry='UBVRIplus')

        Ms = np.round(np.random.uniform(low=0.6, high=1.4, size=3), 4)
        tracks = mistery.get_tracks(Ms=Ms, FeH=FeH, Av=0.1, photometry='UBVRIplus')
    
        # interpolate a track and an isochrone to the same point,
        # where both values of log_L should be close (~per cent)
        for M, track in zip(Ms, tracks):
            for t, iso in zip(ts, isos):
                logL_track = np.interp(t, track['star_age']/1e9, track['Bessell_V'])
                logL_iso = np.interp(M, iso['initial_mass'], iso['Bessell_V'])
                np.testing.assert_allclose(logL_track, logL_iso, rtol=1e-2, atol=1e-2)

if __name__ == '__main__':
    unittest.main()
