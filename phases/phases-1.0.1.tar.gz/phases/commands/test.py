from phases.commands.run import Run
from pyPhases.test import TestCase, TestCaseIntegration
from unittest.loader import TestLoader
from unittest.suite import TestSuite
from unittest import TextTestRunner
import os
import sys

from pathlib import Path


class Test(Run):
    """test a Phase-Project by wrapping TestCases from pyPhase with the project and a configfile specified in project.test.yaml"""

    def __init__(self, options, *args, **kwargs):
        super().__init__(options, *args, **kwargs)
        self.testDir = "tests"
        self.failFast = False
        self.testPattern = "test*.py"

    def parseRunOptions(self):
        super().parseRunOptions()
        if self.options["<testdir>"]:
            self.testDir = Path(self.outputDir).joinpath(self.options["<testdir>"]).as_posix()
            sys.path.insert(0, self.testDir)
            self.logDebug("Set Testdir: %s" % (self.testDir))
        if self.options["<testpattern>"]:
            self.testPattern = self.options["<testpattern>"]
        if self.options["-f"]:
            self.failFast = True

    def wrapTestsInSuite(self, testOrSuite, wrapMethod):
        tests = []
        if isinstance(testOrSuite, TestSuite):
            for subTestOrSuite in testOrSuite._tests:
                tests += self.wrapTestsInSuite(subTestOrSuite, wrapMethod)
        else:
            check = wrapMethod(testOrSuite)
            if check:
                tests = [testOrSuite]
        return tests

    def run(self):
        self.beforeRun()
        self.prepareConfig()

        project = self.createProjectFromConfig(self.config)
        TestCase.project = project

        loader = TestLoader()
        self.logDebug("Discover Tests in %s for pattern %s (Basedir: %s)" % (self.testDir, self.testPattern, self.outputDir))
        os.chdir(self.outputDir)

        if os.path.isdir(self.testDir):
            suite = loader.discover(self.testDir, self.testPattern)
        else:
            suite = loader.loadTestsFromName(self.testDir)

        self.logDebug("Found Tests: %s" % (suite._tests))

        def wrapTestsInSuite(test):
            if isinstance(test, TestCaseIntegration):
                return False
            return True

        noIntegrationTests = self.wrapTestsInSuite(suite, wrapTestsInSuite)

        suite = TestSuite()
        suite.addTests(noIntegrationTests)
        runner = TextTestRunner()
        runner.failfast = self.failFast
        result = runner.run(suite)

        print(result)
        if len(result.errors) > 0 or len(result.failures):
            sys.exit("Test failed")
