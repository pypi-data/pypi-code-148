from collections import namedtuple
from datetime import timedelta
from inspect import isclass
from typing import Optional, List

from robot.api import logger
from robot.errors import DataError
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import is_string
from robot.utils.importer import Importer
from SeleniumLibrary.keywords.screenshot import EMBED
from SeleniumLibrary.locators import ElementFinder
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from SeleniumLibrary.utils import LibraryListener, is_truthy, _convert_timeout
from SeleniumLibrary.errors import NoOpenBrowser
from SeleniumLibrary.keywords import (
    AlertKeywords,
    BrowserManagementKeywords,
    CookieKeywords,
    ElementKeywords,
    FormElementKeywords,
    FrameKeywords,
    JavaScriptKeywords,
    RunOnFailureKeywords,
    ScreenshotKeywords,
    SelectElementKeywords,
    TableElementKeywords,
    WaitingKeywords,
    WindowKeywords,
    WebDriverCache,

)
from SeleniumLibrary.base.context import ContextAware

class VariableManager( object ):
    def __init__(self):
        self.__store = {}
        return

    def clear( self ):
        self.__store = {}
        return

    def __call__(self, *args, **kwargs):
        variable = args[ 0 ]
        self.__store[ variable ] = args[ 1 ]
        return

    def get( self, variable ):
        return self.__store[ variable ]


class SeleniumLibrary( AlertKeywords,
                                    CookieKeywords,
                                    ElementKeywords,
                                    FormElementKeywords,
                                    FrameKeywords,
                                    JavaScriptKeywords,
                                    RunOnFailureKeywords,
                                    ScreenshotKeywords,
                                    SelectElementKeywords,
                                    TableElementKeywords,
                                    WaitingKeywords ):
    def __init__( self,
                  timeout=timedelta(seconds=5),
                  implicit_wait=timedelta(seconds=0),
                  screenshot_root_directory: Optional[str] = None,
                  event_firing_webdriver: Optional[str] = None ):
        """SeleniumLibrary can be imported with several optional arguments.

        - ``timeout``:
          Default value for `timeouts` used with ``Wait ...`` keywords.
        - ``implicit_wait``:
          Default value for `implicit wait` used when locating elements.
        - ``run_on_failure``:
          Default action for the `run-on-failure functionality`.
        - ``screenshot_root_directory``:
          Path to folder where possible screenshots are created or EMBED.
          See `Set Screenshot Directory` keyword for further details about EMBED.
          If not given, the directory where the log file is written is used.
        - ``plugins``:
          Allows extending the SeleniumLibrary with external Python classes.
        - ``event_firing_webdriver``:
          Class for wrapping Selenium with
          [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.event_firing_webdriver.html#module-selenium.webdriver.support.event_firing_webdriver|EventFiringWebDriver]
        """
        ContextAware.__init__( self, self )
        self.__variableManager = VariableManager()
        self.timeout = _convert_timeout(timeout)
        self.implicit_wait = _convert_timeout(implicit_wait)
        self.speed = 0.0
        self.run_on_failure_keyword = self.capture_page_screenshot
        self.screenshot_root_directory = screenshot_root_directory
        self._resolve_screenshot_root_directory()
        self._element_finder = ElementFinder(self)
        # self.ROBOT_LIBRARY_LISTENER = LibraryListener()
        self._running_keyword = None
        self._event_firing_webdriver = None
        if is_truthy(event_firing_webdriver):
            self._event_firing_webdriver = self._parse_listener(event_firing_webdriver)

        self._drivers = WebDriverCache()

        AlertKeywords.__init__( self, self )
        CookieKeywords.__init__( self, self )
        ElementKeywords.__init__( self, self )
        FormElementKeywords.__init__( self, self )
        FrameKeywords.__init__( self, self )
        JavaScriptKeywords.__init__( self, self )
        RunOnFailureKeywords.__init__( self, self )
        ScreenshotKeywords.__init__( self, self )
        SelectElementKeywords.__init__( self, self )
        TableElementKeywords.__init__( self, self )
        WaitingKeywords.__init__( self, self )
        return

    def register_driver(self, driver: WebDriver, alias: str):
        """Add's a `driver` to the library WebDriverCache.

        :param driver: Instance of the Selenium `WebDriver`.
        :type driver: selenium.webdriver.remote.webdriver.WebDriver
        :param alias: Alias given for this `WebDriver` instance.
        :type alias: str
        :return: The index of the `WebDriver` instance.
        :rtype: int
        """
        return self._drivers.register(driver, alias)

    @property
    def VariableStore( self ) -> VariableManager:
        return self.__variableManager

    def capture_page_screenshot( self ):
        return

    def failure_occurred(self):
        """Method that is executed when a SeleniumLibrary keyword fails.

        By default, executes the registered run-on-failure keyword.
        Libraries extending SeleniumLibrary can overwrite this hook
        method if they want to provide custom functionality instead.
        """
        try:
            self.capture_page_screenshot()

        except Exception as err:
            logger.warn( f"Keyword 'capture_page_screenshot' could not be run on failure: {err}" )

        return

    @property
    def driver(self) -> WebDriver:
        """Current active driver.

        :rtype: selenium.webdriver.remote.webdriver.WebDriver
        :raises SeleniumLibrary.errors.NoOpenBrowser: If browser is not open.
        """
        if not self._drivers.current:
            raise NoOpenBrowser("No browser is open.")

        return self._drivers.current

    # def find_element( self, locator: str, parent: Optional[WebElement] = None ) -> WebElement:
    #     """Find element matching `locator`.
    #
    #     :param locator: Locator to use when searching the element.
    #         See library documentation for the supported locator syntax.
    #     :type locator: str or selenium.webdriver.remote.webelement.WebElement
    #     :param parent: Optional parent `WebElememt` to search child elements
    #         from. By default, search starts from the root using `WebDriver`.
    #     :type parent: selenium.webdriver.remote.webelement.WebElement
    #     :return: Found `WebElement`.
    #     :rtype: selenium.webdriver.remote.webelement.WebElement
    #     :raises SeleniumLibrary.errors.ElementNotFound: If element not found.
    #     """
    #     return self._element_finder.find(locator, parent=parent)
    #
    # def find_elements( self, locator: str, parent: WebElement = None ) -> List[WebElement]:
    #     """Find all elements matching `locator`.
    #
    #     :param locator: Locator to use when searching the element.
    #         See library documentation for the supported locator syntax.
    #     :type locator: str or selenium.webdriver.remote.webelement.WebElement
    #     :param parent: Optional parent `WebElememt` to search child elements
    #         from. By default, search starts from the root using `WebDriver`.
    #     :type parent: selenium.webdriver.remote.webelement.WebElement
    #     :return: list of found `WebElement` or e,mpty if elements are not found.
    #     :rtype: list[selenium.webdriver.remote.webelement.WebElement]
    #     """
    #     return self._element_finder.find( locator, first_only=False, required=False, parent=parent )

    def _parse_listener(self, event_firing_webdriver):
        listener_module = self._string_to_modules(event_firing_webdriver)
        listener_count = len(listener_module)
        if listener_count > 1:
            message = f"Is is possible import only one listener but there was {listener_count} listeners."
            raise ValueError(message)

        listener_module = listener_module[0]
        importer = Importer("test library")
        listener = importer.import_class_or_module(listener_module.module)
        if not isclass(listener):
            message = f"Importing test Selenium lister class '{listener_module.module}' failed."
            raise DataError(message)

        return listener

    def _string_to_modules(self, modules):
        Module = namedtuple("Module", "module, args, kw_args")
        parsed_modules = []
        for module in modules.split(","):
            module = module.strip()
            module_and_args = module.split(";")
            module_name = module_and_args.pop(0)
            kw_args = {}
            args = []
            for argument in module_and_args:
                if "=" in argument:
                    key, value = argument.split("=")
                    kw_args[key] = value

                else:
                    args.append(argument)

            module = Module(module=module_name, args=args, kw_args=kw_args)
            parsed_modules.append(module)

        return parsed_modules

    def _resolve_screenshot_root_directory(self):
        screenshot_root_directory = self.screenshot_root_directory
        if is_string(screenshot_root_directory):
            if screenshot_root_directory.upper() == EMBED:
                self.screenshot_root_directory = EMBED

        return
