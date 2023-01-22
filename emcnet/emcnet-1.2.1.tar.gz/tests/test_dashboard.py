import unittest
import emcnet.dashboard


class TestDashboard(unittest.TestCase):
    # database_name = ':memory:'      # special sqlite name for storing database in memory
    database_name = 'resources/test_dashboard'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_1(self):
        emcnet.dashboard.run(site_id='bigbird', emcnetdir='resources/test_dashboard',
                             loglevel="DEBUG", debug=True)

    def test_server_1(self):
        emcnet.dashboard.run(site_id='mmbp2', emcnetdir='resources/test_dashboard_server',
                             loglevel="DEBUG", debug=True)

    def test_server_2(self):
        emcnet.dashboard.run(site_id='mbp2', emcnetdir='resources/test_dashboard_server_2',
                             loglevel="DEBUG", debug=True)


if __name__ == '__main__':
    unittest.main()
