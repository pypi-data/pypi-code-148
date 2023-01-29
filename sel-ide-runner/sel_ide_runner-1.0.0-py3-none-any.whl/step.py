import logging
import copy
import json
import re
import time
from sys import exc_info
from mako.template import Template
from mako import exceptions as mako_exc
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.expected_conditions import staleness_of, visibility_of
from selenium.webdriver.support.ui import WebDriverWait, Select
from sel_ide_runner.selenium_emu import SeleniumLibrary
from selenium.webdriver.common.keys import Keys


class FlowControlNotSupported( Exception ): pass


class JsonAttrEncoder( json.JSONEncoder ):
    def default(self, o: any) -> any:
        if isinstance( o, object ):
            return str( o )

        return o


def buildSendKeys():
    sendkeys = { f"KEY_{key}": getattr( Keys, key )  for key in dir( Keys ) if not key.startswith('_') }
    return sendkeys

class SeleniumTestStep( object ):
    __SENDKEYS = buildSendKeys()

    __COMMAND_TRANSLATE = {
        "continue": "_continue",
        "break": "_break",
        "while": "_while",
        "else": "_else",
        "elseif": "_elseif",
        "if": "_if",
    }

    def __init__( self, id, comment, command, target, targets, value ):
        self.__id       = id
        self.__comment  = comment.strip()
        if command in self.__COMMAND_TRANSLATE:
            # Some corrections on the commands, to avoid colliding with Python statements
            self.__command = self.__COMMAND_TRANSLATE[ command ]

        else:
            self.__command  = command

        self.__target   = target
        self.__targets  = targets
        self.__value    = value
        # Some corrections from Selenium IDE -> SeleniumLibrary
        if self.__target.startswith( 'linkText=' ):
            self.__target = self.__target.replace( 'linkText=', 'link:' )

        return

    @property
    def Id( self ):
        return self.__id

    @property
    def Command( self ):
        return self.__command

    @property
    def Target( self ):
        return self.__target

    @property
    def Targets( self ):
        return self.__targets

    @property
    def Value( self ):
        return self.__value

    @property
    def Comment( self ):
        return self.__comment

    @classmethod
    def dummy( cls ):
        return cls( '',  '',  '',  '',  [],  '' )

    def run( self, driver:SeleniumLibrary, suite, **kwargs ):
        self.__suite = suite
        self.__driver = driver
        self.__attributes = kwargs
        # This corrects the value for the automation
        if self.__comment.startswith( '${' ) and self.__comment.endswith( '}' ):
            self.__value = self.__comment

        if self.__value == '':
            logging.info( f"Executing {self.__command} with target '{self.__target}'")

        else:
            logging.info( f"Executing {self.__command} with target '{self.__target}' and value '{self.__value}'")

        getattr(self, self.__command )()
        # try:
        #     getattr(self, self.__command )()
        #
        # except TypeError:
        #     logging.exception( f"Command: {self.__command} with value '{self.__value}'" )
        #     logging.error( mako_exc.text_error_template().render() )
        #     raise
        #
        # except:
        #     logging.exception( f"Command: {self.__command} with value '{self.__value}'" )
        #     self.__driver.capture_page_screenshot()
        #     raise

        # if self.__suite.Callback:
        #     self.__suite.Callback( driver.page_source )
        return

    def waitForPageLoadEvent( self, timeout = 5, poll_frequency = 1, browser_breath_delay = 1 ):
        """Wait until HTML is ready by using stale check."""
        # pylint: disable=no-member
        if browser_breath_delay < 1:
            browser_breath_delay *= 10

        # let the browser take a deep breath...
        time.sleep( browser_breath_delay )
        try:
            # pylint: disable=no-member
            WebDriverWait( None, timeout, poll_frequency ).until_not( staleness_of( self.__driver.find_element( 'tag=html' ) ), '' )

        # pylint: disable=bare-except
        except:  # noqa: E722
            # instead of halting the process because document is not ready
            # in <TIMEOUT>, we try our luck...
            # pylint: disable=no-member
            self.__driver.debug( exc_info()[ 0 ] )

        return

    def open( self ):
        """New: Open supports relative and full URLs.
        The UI.Vision Selenium IDE does not recommend the use of the base URL concept, but we support it for backward compatibility.

        target:     URL
        :return:
        """
        if self.__target.startswith( 'http' ):
            path = self.__target

        else:
            path = f"{self.__suite.BaseUrl}{self.__target}"

        self.__driver.driver.get( path )
        return

    def click( self ):
        """Clicks on the element.

        target: A locator

        :return:
        """
        element = self.__driver.find_element( self.__target )
        self.__driver.click_element( element )
        return

    def clickAndWait( self ):
        """ClicksAndWait on the element then waits for a page load event.

        target: A locator

        :return:
        """
        self.click()
        self.waitForPageLoadEvent()
        return

    def clickAt( self ):
        """Clicks on specific location

        target:     A Selenium IDE locator
        value:      x,y position of the mouse event relative to the target element. For example: "10,10"
        :return:
        """
        X, Y = self.__value.split( ',' )
        self.__driver.click_element_at_coordinates( self.__target, int( X ), int( Y ) )
        return

    def type( self ):
        """This command erases box content, but sendkey does not

        target:     A Selenium IDE locator
        value:      The string to be set to an input field.

        :return:
        """
        element = self.__driver.find_element( self.__target )
        self.__driver.click_element( element )
        if self.__value.startswith( '${' ) and self.__value.endswith( '}' ):
            # Do some Mako stuff
#            try:
            template = Template( text = self.__value )
            data = template.render( **self.__attributes )

            # except:
            #     logging.error( f"Exception in 'type' value {self.__value} with attributes {json.dumps(self.__attributes, indent= 4, cls = JsonAttrEncoder )}\n{mako_exc.text_error_template().render()}" )
            #     raise

        else:
            data = self.__value

        logging.info( f"Selenium typing '{data}' for {self.__target}" )
        self.__driver.input_text( element, data )
        # element.send_keys( data )
        return

    def sendKeys( self ):
        """For example: "${KEY_DOWN}"

        target:     	A locator
        value:          A character.

        :return:
        """
        try:
            element = self.__driver.find_element( self.__target )

        except:
            located = self.__driver.find_element( self.__target )
            print( f'verifyValue: {self.__target} {located} {self.__value}' )
            raise

        if self.__value.startswith( '${' ) and self.__value.endswith( '}' ):
            # Do some Mako stuff
            attrs = copy.deepcopy( self.__attributes )
            try:
                attrs.update( self.__SENDKEYS )
                template = Template( text = self.__value )
                data = template.render( **attrs )

            except:
                logging.error( f"Exception in 'type' value {self.__value} with attributes {json.dumps(attrs, indent= 4, cls = JsonAttrEncoder )}\n{mako_exc.text_error_template().render()}" )
                raise

        else:
            data = self.__value

        logging.info( f"Selenium sending keys '{data}' for {self.__target}" )
        element.send_keys( data )
        return


    def select( self ):
        """

        target:     A locator of a drop-down menu
        value:      An option locator. For example: "label=Option1" (...andWait: plus waits for page load event)
        :return:
        """
        element = self.__driver.find_element( self.__target )
        item = Select( element )
        if '=' in self.__value:
            mode, value = self.__value.split( '=' )
            if mode == 'label':
                item.select_by_visible_text( value )

            else:
                item.select_by_value( value )

        elif self.__value.isdigit():
            item.select_by_index( self.__value )

        elif self.__value == '*':
            item.all_selected_options()

        else:
            msg = f"Don\'t know how to select {self.__value} on {self.__target}"
            raise Exception( msg )

        return

    def selectAndWait( self ):
        """

        target:     A locator of a drop-down menu
        value:      An option locator. For example: "label=Option1" (...andWait: plus waits for page load event)
        :return:
        """
        self.select()
        self.waitForPageLoadEvent()
        return

    def selectFrame( self ):
        """

        target:     "index=0" (Select the first frame of index 0)
                    "relative=parent" (Select the parent frame)
                    "relative=top" (Select the top frame)

        :return:
        """
        self.__driver.select_frame( self.__target )
        return

    def verifyTitle( self ):
        """The next command will still be run even if the text verification fails.

        target:     The expected string of the title (Exact matching).

        :return:
        """
        element = self.__driver.find_element('tag=title')
        if element.text != self.__target:
            self.__driver.info( f"Page title '{self.__target}' nor found, got '{element.text}'" )

        return

    def verifyTextPresent( self ):
        """The next command will still be run even if the text verification fails.

        target:     A Selenium IDE locator
        value:      The expected string of the target element (Exact matching).

        :return:
        """
        try:
            assert bool( self.__value in self.__driver.driver.page_source )

        except:
            print( 'verifyTextPresent: {self.__value} not present in {source}' )
            raise

        return

    def verifyTextNotPresent( self ):
        try:
            assert not bool( self.__value in self.__driver.driver.page_source )

        except:
            print( f'verifyNotTextPresent: {self.__value} present' )
            raise

        return

    def assertElementPresent( self ):
        """Checks if the element exists on the page.

        A Selenium IDE locator

        :return:
        """
        try:
            assert bool( self.__driver.find_element( self.__target ) )

        except:
            print( f'assertElementPresent: {self.__target} not present' )
            raise

        return

    def verifyElementPresent( self ):
        """Checks if the element exists on the page and logs error if not.

        target:     	A Selenium IDE locator

        :return:
        """
        try:
            assert bool( self.__driver.find_element( self.__target ) )

        except:
            print( f'verifyElementPresent: {self.__target} not present' )
            raise

        return

    def verifyElementNotPresent( self ):
        present = True
        try:
            self.__driver.find_element( self.__target )

        except NoSuchElementException:
            present = False

        try:
            assert not present

        except:
            print( f'verifyElementNotPresent: {self.__target } present')
            raise

        return

    def waitForTextPresent( self, **kwargs ):
        try:
            assert bool( self.__value in self.__driver.driver.page_source )

        except:
            print( f'waitForTextPresent: {self.__value} ]not present')
            raise

        return

    def waitForTextNotPresent( self, **kwargs ):
        try:
            assert not bool( self.__value in self.__driver.driver.page_source)

        except:
            print( f'waitForTextNotPresent: {self.__value} present')
            raise

    def assertText( self ):
        """Variable declared in the storeXXX commands can be used in the string. For example: "Hello ${varusr}"

        target: A Selenium IDE locator
        value:  The expected string of the target element (Exact matching).

        :return:
        """
        if not isinstance( self.__value, str ):
            self.__value = ''

        try:
            target_value = self.__driver.find_element( self.__target ).text
            logging.info('   assertText target value =' + repr(target_value))
            if self.__value.startswith('exact:'):
                assert target_value == self.__value[ len( 'exact:' ): ]

            else:
                assert target_value == self.__value

        except:
            located = self.__driver.find_element( self.__target ).get_attribute( 'value' )
            print( f'assertText: {self.__target} {located} {self.__value}' )
            raise

        return

    def assertNotText( self ):
        if not isinstance( self.__value, str ):
            self.__value = ''

        try:
            target_value = self.__driver.find_element( self.__target ).text
            logging.info('  assertNotText target value =' + repr(target_value))
            if self.__value.startswith('exact:'):
                assert target_value != self.__value[len('exact:'):]

            else:
                assert target_value != self.__value

        except:
            located = self.__driver.find_element( self.__target ).get_attribute( 'value' )
            print( f'assertNotText: {self.__target} {located} {self.__value}' )
            raise

        return

    def assertValue( self ):
        if not isinstance( self.__value, str ):
            self.__value = ''

        try:
            target_value = self.__driver.find_element( self.__target ).get_attribute('value')
            logging.info('  assertValue target value ='+repr(target_value))
            assert target_value == self.__value
        except:
            located = self.__driver.find_element( self.__target ).get_attribute( 'value' )
            print( f'assertValue: {self.__target} {located} {self.__value}' )
            raise

        return

    def assertNotValue( self ):
        if not isinstance( self.__value, str ):
            self.__value = ''

        try:
            target_value = self.__driver.find_element( self.__target ).get_attribute('value')
            logging.info('  assertNotValue target value ='+repr(target_value))
            assert target_value != self.__value

        except:
            located = self.__driver.find_element( self.__target ).get_attribute( 'value' )
            print( f'assertNotValue: {self.__target} {located} {self.__value}' )
            raise

    def verifyValue( self ):
        if not isinstance( self.__value, str ):
            self.__value = ''

        try:
            target_value = self.__driver.find_element( self.__target ).get_attribute('value')
            logging.info('  verifyValue target value ='+repr(target_value))
            assert target_value == self.__value

        except:
            located = self.__driver.find_element( self.__target ).get_attribute( 'value' )
            print( f'verifyValue: {self.__target} {located} {self.__value}' )
            raise

    def runScript( self ):
        self.__driver.driver.execute_script( self.__target )
        return

    def setWindowSize( self ):
        width, height = self.__target.split('x')
        self.__driver.driver.set_window_size( int( width ), int( height ) )
        return

    def selectWindow( self ):
        """Switch browser tabs. In addition to the tab name value, you can use numbers tab=0,1,2,3 to switch tabs. Tab=0 is current tab, 1 is one to right, etc.

        target:     	Auto-generated

        :return:
        """
        index = int( self.__target.split('=')[-1] )
        self.__driver.driver.switch_to.window( self.__driver.driver.window_handles[ index ] )
        return

    def AssertChecked( self ):
        """ Continues test only if a checkbox or radio button is checked

        target:         A Selenium IDE locator

        :return:
        """
        self.__driver.checkbox_should_be_selected( self.__target )
        return

    def assertAlert( self ):
        """The expected alert message

        :return:
        """
        self.__driver.alert_should_be_present()
        return

    def assertConfirmation( self ):
        """	The expected Confirm message

        :return:
        """
        self.__driver.alert_should_be_present()
        return

    def assertPrompt( self ):
        """The expected Prompt message

        :return:
        """
        self.__driver.alert_should_be_present()
        return

    def assertEditable( self ):
        """Checks if the input field can be edited.

        A Selenium IDE locator

        :return:
        """
        element = self.__driver.find_element( self.__target )
        if not element.is_enabled():
            raise RobotNotRunningError( f'element {element.tag_name}:{element.text} is not editable' )

        return

    def assertTitle( self ):
        """The expected string of the title (Exact matching).

        target: 	expected string

        :return:
        """
        if self.__driver.driver.title != self.__target:
            raise RobotNotRunningError( f'title in not {self.__target}, got {self.__driver.driver.title}' )

        return

    def bringBrowsertoForeground( self ):
        """Brings the active browser tab to the foreground. Some browser features such as giving the selected input element the focus work only when the browser is in front.

        :return:
        """
        raise NotImplemented()

    def captureScreenshot( self ):
        """Captures the contents of the OS view port (i.e. whatever is currently being displayed on the monitor). The screenshot is displayed in the "Screenshot tab". From there, you can export it.

        target:     	file name

        :return:
        """
        self.__driver.driver.save_screenshot( self.__target )
        return

    def captureEntirePageScreenshot( self ):
        """	Captures the contents of the entire website. The screenshot is displayed in the "Screenshot tab". From there, you can export it.

        target:     	file name

        :return:
        """
        with open( self.__target, 'w' ) as stream:
            stream.write( self.__driver.driver.page_source )

        return

    def Check( self ):
        """Check a checkbox.

        target: locator name

        :return:
        """
        element = self.__driver.find_element( self.__target )
        self.__driver.select_checkbox( element )
        return

    def Uncheck( self ):
        """UnCheck a checkbox.

        target: locator name

        :return:
        """
        element = self.__driver.find_element( self.__target )
        self.__driver.unselect_checkbox( element )
        return

    def chooseOkOnNextConfirmation( self ):
        """UI.Vision RPA closes dialogs automatically. In other words, chooseOkOnNextConfirmation is a built-in behavior, and no longer a separate command.

        :return:
        """
        raise NotImplemented()

    def csvRead( self ):
        """Reads one line of the CSV file and makes the values available in ${COL1}, ${COL2}, ...and so on. Important: To submit more than just the first line of the CSV file, you must start the macro with the LOOP button. Each loop reads one line of the CSV. The line read is based on the value of the ${!LOOP} counter variable.

        target:     	name of CSV file

        :return:
        """
        raise NotImplemented()

    def csvSave( self ):
        """Saves the line that was built store | value | !csvLine to a file inside the Chrome storage (not to your hard drive)

        target      name of CSV file

        :return:
        """
        raise NotImplemented()

    def deleteAllCookies( self ):
        """Deletes all cookies

        :return:
        """
        self.__driver.delete_all_cookies()
        return

    def dragAndDropToObject( self ):
        """Drag and drop an element

        target: The locator of the element to be dragged
        value:  The locator of the element on which the target element is dropped.

        :return:
        """
        locator = self.__driver.find_element( self.__target )
        target = self.__driver.find_element( self.__value )
        self.__driver.drag_and_drop( locator, target )
        return

    def echo( self ):
        """The string to be printed in the log console.

        target:     string

        :return:
        """
        logging.info( self.__target )
        return

    def executeScript( self ):
        """	Run a Javascript snippet and store the result in variable

        target:     Javascript
        value:      variable

        :return:
        """
        self.__driver.execute_javascript( self.__target, self.__value )
        return

    def executeAsyncScript( self ):
        """Run an async Javascript snippet and store the result in variable

        target:     Javascript
        value:      variable

        :return:
        """
        self.__driver.execute_async_javascript( self.__target, self.__value )
        return

    def editContent( self ):
        """

        target:     Selenium IDE locator
        value:      text in HTML format

        :return:
        """
        locator = self.__driver.find_element( self.__target )
        raise NotImplemented()

    def highlight( self ):
        """

        target:     Selenium IDE locator
        value:      No longer needed. The new IDE highlights all found elements by default. You can disable highlighting in the settings.

        :return:
        """
        locator = self.__driver.find_element( self.__target )
        return

    def mouseOver( self ):
        """

        target:         Selenium IDE locator
        :return:
        """
        self.__driver.mouse_over( self.__driver.find_element( self.__target ) )
        raise NotImplemented()

    def pause( self ):
        """The amount of time to sleep in millisecond. For example: "5000" means to wait for 5 seconds.

        target:         milliseconds

        :return:
        """
        time.sleep(int(self.__target)/1000)
        return

    def prompt( self ):
        """Ask the user for input and store the value in a variable.

        target:     your text here@default value
        value:      variable

        :return:
        """
        raise NotImplemented()

    def sourceExtract( self ):
        """Extract data and stores it in variable. Works with the page source, instead of looking at the web page object model (DOM).

        target:     search string or regex
        value:      variable

        :return:
        """
        result = re.search( self.__target, self.__driver.driver.page_source )
        if result:
            groups = "".join( [ str(item) for item in result.groups() ] )
            self.__driver.VariableStore( self.__value, groups )

        else:
            self.__driver.VariableStore( self.__value, self.__driver.driver.page_source )

        return

    def sourceSearch( self ):
        """Counts matches and stores the result in a variable. Works with the page source, instead of looking at the web page object model (DOM).

        target:     search string or regex
        value:      variable

        :return:
        """
        result = re.search( self.__target, self.__driver.driver.page_source )
        if result:
            self.__driver.VariableStore( self.__value, len( result.groups() ) )

        else:
            self.__driver.VariableStore( self.__value, 0 )

        raise NotImplemented()

    def Refresh( self ):
        """	Refreshes (reloads) the current page.

        :return:
        """
        self.__driver.driver.refresh()
        return

    def Run( self ):
        """Re-use one macro (test case) inside of another.

        :return:
        """
        raise NotImplemented()

    def store( self ):
        """Note: System variables start with ! like !TIMEOUT_WAIT. So you can not create a variable that starts with ! (=> error message)

        target:     A string
        value:      The name of the variable storing the string. For example: "var_usr"

        :return:
        """
        self.__driver.VariableStore( self.__target, self.__value )
        return

    def storeAttribute( self ):
        """

        target:     ….href …alt
        value:     Variable to store the attribute in it

        :return:
        """
        target, attribute = self.__target.split( '@' )
        locator = self.__driver.find_element( target )
        self.__driver.VariableStore( self.__value, locator.get_attribute( attribute ) )
        return

    def storeChecked( self ):
        """result is true if the radiobutton or box is checked, otherwise false

        target:     A Selenium IDE locator
        value:      variable to store the result in

        :return:
        """
        locator = self.__driver.find_element( self.__target )
        self.__driver.VariableStore( self.__value, locator.get_attribute('value') )
        return

    def storeEval( self ):
        """

        target:     Javascript to run...
        value:      Variable to store the result in (optional)

        :return:
        """
        raise NotImplemented()

    def storeText( self ):
        """

        target:     A Selenium IDE locator
        value:      The name of the variable storing the text of the target element. E. g. "abc"

        :return:
        """
        locator = self.__driver.find_element( self.__target )
        self.__driver.VariableStore( self.__value, locator.text )
        return

    def storeTitle( self ):
        """

        target:     (the title of the website)
        value:      The name of the variable storing the title e. g "mytitle"
        :return:
        """
        self.__driver.VariableStore( self.__value, self.__driver.driver.title )
        return

    def storeValue( self ):
        """

        target:     A Selenium IDE locator
        value:      The name of the variable storing the value of the target element. E. g. "phone"

        :return:
        """
        locator = self.__driver.find_element( self.__target )
        self.__driver.VariableStore( self.__value, locator.get_attribute('value') )
        return

    def storeXpathCount( self ):
        """Counts elements

        target:     A Selenium IDE locator
        value:      The name of the variable storing the value of the target element. E. g. "phone"

        :return:
        """
        locators = self.__driver.find_elements( self.__target )
        self.__driver.VariableStore( self.__value, len( locators ) )

    def storedVars( self ):
        """	(Deprecated)

        target:     used inside storeEval and other places

        :return:
        """
        raise NotImplemented()

    def ThrowError( self ):
        """This command triggers an error. It stops the macro execution and displays "your error message" in the log file. Together with if/endif it allows you to create your own error conditions.

        target:     Your error message
        :return:
        """
        raise RobotNotRunningError( self.__target )

    def Verify( self ):
        """	Assert that a variable is an expected value. The variable's value will be converted to a string for comparison.

        target:     variable name without brackets
        value:      value

        :return:
        """
        assert self.__driver.VariableStore.get( self.__target ) != self.__value
        return

    def VerifyChecked( self ):
        """Logs if a checkbox or radio button is checked

        target:     A Selenium IDE locator

        :return:
        """
        locator = self.__driver.find_element( self.__target )
        self.__driver.checkbox_should_be_selected( locator )
        return

    def waitForElementPresent( self ):
        """These commands are no longer needed, as the UI.Vision RPA IDE uses implicit waiting, just like webDriver
        :return:
        """
        locator = self.__driver.find_element( self.__target )
        return

    def waitForElementToLoad( self ):
        """These commands are no longer needed, as the UI.Vision RPA IDE uses implicit waiting, just like webDriver

        :return:
        """
        raise NotImplemented()

    def waitForPageToLoad( self ):
        """Wait for the page to be fully loaded. Normally not needed as all "...andWait" commands include it e. g. in ClickandWait

        :return:
        """
        raise NotImplemented()

    def waitForVisible( self ):
        """Waits for the element to be visible.

        :return:
        """
        locator = self.__driver.find_element( self.__target )
        assert locator.is_enabled() == True
        assert locator.is_displayed() == True
        return

    def Do( self ):
        """Similar to while, the the first "if" check is done at the end of the loop.

        :return:
        """
        raise FlowControlNotSupported()

    def Repeat_if( self ):
        """Similar to while, the the first "if" check is done at the end of the loop.

        target:     	Javascript to evaluate

        :return:
        """
        raise FlowControlNotSupported()

    def gotoIf( self ):
        """(Deprecated) If the expression evaluates to TRUE the execution jumps to LABEL, otherwise continues with the next command. Often used with !statusOK.

        target:     Javascript to evaluate
        value:      Label

        :return:
        """
        raise FlowControlNotSupported()

    def gotoLabel( self ):
        """(Deprecated) Jumps to LABEL.

        taget:      label

        :return:
        """
        raise FlowControlNotSupported()

    def forEach( self ):
        """Loop over the content of an Javascript array.

        target:     Javascript to evaluate

        :return:
        """
        raise FlowControlNotSupported()

    def end( self ):
        """Loop over the content of an Javascript array.

        :return:
        """
        raise FlowControlNotSupported()

    def _if( self ):
        """The classic if-then-else conditional. If the expression evaluates to TRUE the "then" section is executed, otherwise the "else" section is executed. Often used with !statusOK

        target:         	Javascript to evaluate
        :return:
        """
        raise FlowControlNotSupported()

    def _elseif( self ):
        """The classic if-then-else conditional. If the expression evaluates to TRUE the "then" section is executed, otherwise the "else" section is executed. Often used with !statusOK

        target:     	Javascript to evaluate
        :return:
        """
        raise FlowControlNotSupported()

    def _else( self ):
        """The classic if-then-else conditional. If the expression evaluates to TRUE the "then" section is executed, otherwise the "else" section is executed. Often used with !statusOK

        :return:
        """
        raise FlowControlNotSupported()

    def label( self ):
        """	(Deprecated) Defines the LABEL position for gotoIf and gotoLabel to jump to.

        target:         Label

        :return:
        """
        raise FlowControlNotSupported()

    def times( self ):
        """	Loop "Number" times.

        target:     number

        :return:
        """
        raise FlowControlNotSupported()

    def _while( self ):
        """	Executes the section between while...end as often/as long as the conditional statement evaluates to true.

        target:     Javascript to evaluate

        :return:
        """
        raise FlowControlNotSupported()

    def _break( self ):
        """The break statement breaks the loop and continues executing the code after the loop (if any). Usually it is used after a conditional "if" (or similar) statement.

        :return:
        """
        raise FlowControlNotSupported()

    def _continue( self ):
        """The continue statement breaks one iteration (in the loop) and continues with the next iteration in the loop. So the difference between break and continue is that break leaves a loop, and continue "only" jumps to the next iteration.

        :return:
        """
        raise FlowControlNotSupported()
