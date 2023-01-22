import emcnet.device.vmppt_store as victron_mppt

import unittest


class TestVictronMPPT(unittest.TestCase):

    @unittest.skip("only run this test when we have an MQTT broker launched")
    def test_victron_mppt_1(self):
        pass
        victron_mppt.VMPPTMonitor(emulate=True).run(3)


if __name__ == '__main__':
    unittest.main()
