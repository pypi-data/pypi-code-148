import logging
import json
from sel_ide_runner.case import SeleniumTestCase
from sel_ide_runner.selenium_emu import SeleniumLibrary


class SuiteNotAvailable( Exception ): pass
class TestCaseNotAvailable( Exception ): pass



class SeleniumSuite( object ):
    def __init__( self, parent, id, name, persistSession, parallel, timeout, tests ):
        self.__parent = parent
        self.__id = id
        self.__name = name
        self.__persistSession = persistSession
        self.__parallel = parallel
        self.__timeout = timeout
        self.__tests = tests
        return

    @property
    def Name( self ):
        return self.__name

    def run( self, testcases, driver, **kwargs ):
        for testcase_id in self.__tests:
            for testcase in testcases:
                if testcase.Id == testcase_id:
                    testcase.run( driver, **kwargs )

        return


class SeleniumTestSuite(object):
    """A Selenium Test Suite"""

    def __init__( self, filename, callback = None ):
        self.__callback = callback
        self.__suite_name   = ''
        self.__testcases    = []
        self.__suites       = []
        with open( filename, 'r' ) as stream:
            dom = json.load( stream )

        self.__id = dom.get( "id" )
        if dom.get("version") != "2.0":
            raise Exception( "Invlaid version" )

        self.__suite_name = dom.get( "name" )
        self.__url = dom.get( "url" )
        for testcase in dom.get( 'tests', [] ):
            self.__testcases.append( SeleniumTestCase( self, **testcase ) )

        for suite in dom.get( 'suites', [] ):
            self.__suites.append( SeleniumSuite( self, **suite ) )

        self.__urls = dom.get( 'urls', [] )
        self.__plugins = dom.get( 'plugins', [] )
        return

    @property
    def Callback( self ):
        return self.__callback

    @property
    def Name( self ):
        return self.__suite_name

    @property
    def BaseUrl( self ):
        return self.__url

    @property
    def Id( self ):
        return self.__id

    def hasSuite( self, suite_name ):
        for suite in self.__suites:
            if suite.Name == suite_name:
                return True

        if isinstance( suite_name, str ):
            raise SuiteNotAvailable( f'Suite not found {suite_name}')

        return False

    def hasTestcase( self, testcase_name ):
        for testcase in self.__testcases:
            if testcase.Name == testcase_name:
                return True

        if isinstance( testcase_name, str ):
            raise TestCaseNotAvailable( f'Testcase not found {testcase_name}')

        return False

    def runsuite( self, suite_name, driver: SeleniumLibrary, **kwargs ):
        for suite in self.__suites:
            if suite.Name == suite_name:
                suite.run( self.__testcases, driver, **kwargs )

        return

    def runtestcase( self, testcase_name, driver: SeleniumLibrary, **kwargs ):
        for testcase in self.__testcases:
            if testcase.Name == testcase_name:
                testcase.run( driver, **kwargs )

        return

    def run( self, driver: SeleniumLibrary, **kwargs ):
        for testcase in self.__testcases:
            # try:
            testcase.run( driver, **kwargs )

            # except:
            #     logging.exception( f'Error in {self.__suite_name} {self.__testcases}' )
            #     raise
            #
