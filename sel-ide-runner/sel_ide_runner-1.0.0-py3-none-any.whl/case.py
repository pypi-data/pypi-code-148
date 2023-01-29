from typing import Union
import logging
from sel_ide_runner.step import SeleniumTestStep
from sel_ide_runner.selenium_emu import SeleniumLibrary


class SeleniumTestCase( object ):
    """A Single Selenium Test Case"""
    def __init__(self, suite: 'SeleniumTestSuite', id: str, name: str, commands: Union[list,None] = None ):
        self.__id = id
        self.__suite = suite
        self.__name = name
        self.__commands = commands if isinstance( commands, list ) else []
        # Walk through checking the commands
        step = SeleniumTestStep.dummy()
        for command in self.__commands:
            cmd = command.get( 'command' )
            if not hasattr( step, cmd ):
                raise Exception( f'Unknown Selenium IDE command {cmd}' )

        return

    @property
    def Name( self ):
        return self.__name

    @property
    def Id( self ):
        return self.__id

    def run( self, driver: SeleniumLibrary, **kwargs ):
        self.base_url = self.__suite.BaseUrl
        logging.info( f'running {self.__name}' )
        for command in self.__commands:
            step = SeleniumTestStep( **command )
            step.run( driver, self.__suite, **kwargs )

        return
