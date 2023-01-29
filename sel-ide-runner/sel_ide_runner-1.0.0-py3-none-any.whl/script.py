import os
import logging
from selenium import webdriver
from sel_ide_runner.suite import SeleniumTestSuite
from sel_ide_runner.selenium_emu import SeleniumLibrary


def create_driver_session( executor_url, session_id = None, options = {} ):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute
    def new_command_execute(self, command, params=None):
        if command == "newSession" and isinstance( session_id, str ):
            # Mock the response
            return { 'success': 0, 'value': None, 'sessionId': session_id }

        elif command == "close" and isinstance( self.session_id, str ):
            return { 'success': 0, 'value': None, 'sessionId': self.session_id }

        else:
            return org_command_execute( self, command, params )

    # Patch the function before creating the driver object
    # if isinstance( session_id, str ):
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote( command_executor = executor_url, options = options )
    if isinstance( session_id, str ):
        new_driver.session_id = session_id

    # Replace the patched function with original function
    # RemoteWebDriver.execute = org_command_execute
    return new_driver


class RunSeleniumIdeScript():
    def __init__( self, engine_options, session_id = None, selenium_host = None, full_details = False ):
        self.__selenium_host    = selenium_host
        self.__session_id       = session_id
        self.__engine_options   = engine_options
        self.__driver           = self.get_driver()
        self.__url              = None
        self.__fullDetails      = full_details
        self.__selLibrary       = SeleniumLibrary()
        self.__selLibrary.register_driver( self.__driver, 'remote' )
        return

    def close( self ):
        # self.__driver.close()
        return

    def get_driver( self ) -> webdriver.Remote:
        if self.__selenium_host is not None:
            return create_driver_session( self.__selenium_host, self.__session_id, options = self.__engine_options )

        return self.__engine_options

    def run_suite( self, suite_filename, suite_name = None, testcase_name = None, **kwargs ):
        suite_filename = os.path.abspath( suite_filename )
        if os.path.isfile( suite_filename ):
            tests = SeleniumTestSuite( suite_filename, self.check_for_errors )
            try:
                if tests.hasSuite( suite_name ):
                    logging.debug( f'running testsuite {suite_name} from file {suite_filename}' )
                    tests.runsuite( suite_name, self.__selLibrary, **kwargs )

                elif tests.hasTestcase( testcase_name ):
                    logging.debug( f'running testcase {testcase_name} from file {suite_filename}' )
                    tests.runtestcase( testcase_name, self.__selLibrary, **kwargs )

                else:
                    logging.debug( f'running suite full form file {suite_filename}' )
                    tests.run( self.__selLibrary, **kwargs )

            except:
                # self.__driver.save_screenshot('%s-error_screen.png' % suite_name)
                raise

        else:
            raise Exception( f'suite {suite_filename} missing')

        self.__driver.quit()

    def check_for_errors( self, text ):
        if self.__fullDetails:
            logging.error( text )

        return
