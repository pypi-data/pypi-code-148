# info@codebasedlearning.dev, a.voss@fh-aachen.de

import unittest
import importlib.metadata

import cbl_tools
from cbl_tools import versioning
from cbl_tools.versioning import semver_of, package_semver_of, __version__ as cbl_tools_versioning_version

cbl_tools_package_version = importlib.metadata.version('cbl_tools')


class VersioningTestCase(unittest.TestCase):
    def test_versioning_import(self):
        self.assertEqual(cbl_tools.versioning.semver_of, semver_of)
        self.assertEqual(cbl_tools.versioning.package_semver_of, package_semver_of)
        # note: versioning.semver_of is not semver_of, but their hashes should be equal
        self.assertEqual(versioning.semver_of.__code__.__hash__(), semver_of.__code__.__hash__())
        self.assertEqual(versioning.package_semver_of.__code__.__hash__(), package_semver_of.__code__.__hash__())

    def test_semver_of(self):
        self.assertEqual("1.2.3", cbl_tools.versioning.semver_of(1, 2, 3))
        self.assertEqual("4.5.6", versioning.semver_of(4, 5, 6))
        self.assertEqual("7.8.9", semver_of(7, 8, 9))
        self.assertEqual("1.2.3-a.1", semver_of(1, 2, 3, 'a.1'))

    def test_package_semver(self):
        self.assertEqual(f"{cbl_tools_package_version}", cbl_tools_versioning_version.__version__)

    def test_package_semver_of(self):
        self.assertEqual(f"{cbl_tools_package_version}", cbl_tools.versioning.package_semver_of())
        self.assertEqual(f"{cbl_tools_package_version}", versioning.package_semver_of())
        self.assertEqual(f"{cbl_tools_package_version}", package_semver_of())
        self.assertEqual(f"{cbl_tools_package_version}-rc.3", package_semver_of("rc.3"))


if __name__ == '__main__':
    unittest.main()
