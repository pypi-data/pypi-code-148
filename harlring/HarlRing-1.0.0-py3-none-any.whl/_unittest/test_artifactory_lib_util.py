import unittest
from harlring.artifactory.artifactory_lib_util import ArtifactoryLibUtil


class TestPubArtifactoryLib(unittest.TestCase):
    def test_artifactorylibutil_001(self):
        """
        使用util
        """
        user = "aqc001"
        password = "l1nx1L1n@n6"
        artifactory_lib_util = ArtifactoryLibUtil(user, password)
        path_string = "http://artifactory.test.com:8081/artifactory/Daily/BPC"
        print(artifactory_lib_util.artifactory_path_exist(path_string))



