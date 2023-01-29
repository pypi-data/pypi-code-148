import sys
import json
import yaml
import getopt
import logging
import os
import posixpath
import pyotp
from urllib.parse import urlparse
from selenium import webdriver
from sel_ide_runner.script import RunSeleniumIdeScript
from pykeystore import KeyStoreEx, load_password


class PathNotExists( Exception ): pass
class InvalidBrowser( Exception ): pass
class WrongFileType( Exception ): pass


class Builtin():
    def __init__( self, keystore = None, open = False ):
        self.__keystore = None
        if keystore is None and open:
            # Try the default
            passphrase      = load_password( os.path.join( os.path.expanduser( '~' ), '.keystore.password' ) )
            self.__keystore = KeyStoreEx.load( os.path.join( os.path.dirname( __file__ ), 'keystore.pyks' ),
                                               passphrase )
        else:
            self.__keystore = keystore

        return

    def OTP( self, account ):
        secret = self.__keystore.get2fa( account )
        if secret is None:
            raise Exception( f"Secret for account '{secret}' was not found in keystore for OTP")

        return pyotp.TOTP( secret ).now()

    def getPassword( self, account ):
        password = self.__keystore.getPassword( account )
        if password is None:
            raise Exception( f"Password for account '{account}' was not found in keystore")

        return password



def usage():
    print("""sel-ide-runner [ <options> ] <ide.filename> [ { test <test-case-name> | suite <suite-name> } ]

Options:
-v/--verbose                        Be very verbose in the output
-h/--help                           Help page
-s/--server <url>                   The URL to the Selenium server, when omitted http://localhost:1234 is used
-l/--logfile <file>                 The the filename for the logger
-b/--browser <name>                 Select the browser you want to use (default chrome) posible firefox, chrome and edge. 
-S/--screenshot <dir>               Screen shot storage folder
-D/--data <dir>                     Data storage folder
-K/--keystore <file>                The pykeystore to be used
-P/--passphrase <file|passphrase>   The passphrase file or the actual passphrase  
-V/--variable <variable|file>       The variable like 'MyVar="Testing Selenium"' or a .YAML/.JSON file with the variables.
    """)

class SelRunnerProperties( object ):
    def __init__(self):
        self.__verbose      = False
        self.__scheme       = 'http'
        self.__host         = '127.0.0.1'
        self.__port         = 1234
        self.__uri          = 'wd/hub'
        self.__logfile      = 'trace.log'
        self.__screenDir    = os.path.abspath( os.getcwd() )
        self.__dataDir      = os.path.abspath( os.getcwd() )
        self.__keystore     = ''
        self.__passphrase   = ''
        self.__browser      = 'chrome'
        return

    @property
    def Verbose( self ) -> bool:
        return self.__verbose

    @Verbose.setter
    def Verbose( self, value: bool ) -> None:
        self.__verbose = value
        return

    def getLoglevel( self ):
        if self.__verbose:
            return logging.DEBUG

        return logging.INFO

    @property
    def Server( self ) -> str:
        return posixpath.join( f'{self.__scheme}://{self.__host}:{self.__port}', self.__uri )

    @Server.setter
    def Server( self, value: str ) -> None:
        if '://' in value:                      # actual url
            r = urlparse( value )
            self.__scheme  = r.scheme
            self.__host    = r.hostname
            self.__port    = r.port

        elif ':' in value and '/' not in value:     # host:port
            self.__host, self.__port = value.split(':')

        else:                                   # host
            self.__host = value

        return

    @property
    def LogFile( self ) -> str:
        return os.path.abspath( self.__logfile )

    @LogFile.setter
    def LogFile( self, value: str ) -> None:
        self.__logfile = value
        return

    @property
    def ScreenShotFolder( self ) -> str:
        return self.__screenDir

    @ScreenShotFolder.setter
    def ScreenShotFolder( self, value ):
        if not os.path.exists( value ):
            raise PathNotExists( f"Screenshot filepath ({value}) doesn't exists" )

        self.__screenDir = value
        return

    @property
    def DataFolder( self ) -> str:
        return self.__dataDir

    @DataFolder.setter
    def DataFolder( self, value ):
        if not os.path.exists( value ):
            raise PathNotExists( f"Data filepath ({value}) doesn't exists" )

        self.__dataDir = value
        return

    @property
    def KeyStore( self ) -> str:
        return self.__keystore

    @KeyStore.setter
    def KeyStore( self, value ):
        if not os.path.exists( value ):
            raise FileNotFoundError( f"Keystore ({value}) doesn't exists" )

        self.__keystore = value
        return

    @property
    def Passphrase( self ) -> str:
        return self.__passphrase

    @Passphrase.setter
    def Passphrase( self, value ):
        if os.path.exists( value ):
            self.__passphrase = load_password( value )

        else:
            self.__passphrase = value

        return

    def getKeystore( self ):
        if self.__keystore != '':
            if self.__passphrase == '':
                self.__passphrase = load_password( os.path.join( os.path.expanduser( '~' ), '.keystore.password' ) )

            keystore = KeyStoreEx.load( self.__keystore, self.__passphrase )
            return keystore

        return None

    @property
    def Browser( self ) -> str:
        return self.__browser

    @Browser.setter
    def Browser( self, value ):
        if value not in ( 'chrome', 'firefox', 'edge' ):
            raise InvalidBrowser( f"Invalid browser {value}, allowed are 'chrome', 'firefox', 'edge'" )

        self.__browser = value
        return

    def getBrowserOptions( self ):
        if self.__browser == 'chrome':
            return webdriver.ChromeOptions()

        elif self.__browser == 'firefox':
            return webdriver.FirefoxOptions()

        elif self.__browser == 'edge':
            return webdriver.EdgeOptions()

        return


def main():
    try:
        properties = SelRunnerProperties()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hvs:l:S:D:K:P:b:", ["help", "verbose", "server=", "logfile=", "screenshot=", "data=", "keystore=", "passphrase=", "browser=" ])

        except getopt.GetoptError as err:
            # print help information and exit:
            print(err)  # will print something like "option -a not recognized"
            usage()
            sys.exit(2)

        attributes = {}
        for o, a in opts:
            if o == "-v":
                properties.Verbose = True

            elif o in ("-h", "--help"):
                usage()
                sys.exit()

            elif o in ("-s", "--server"):
                properties.Server = a

            elif o in ("-l", "--logfile"):
                properties.LogFile = a

            elif o in ("-S", "--screenshot"):
                properties.ScreenShotFolder = a

            elif o in ("-D", "--data"):
                properties.DataFolder = a

            elif o in ("-K", "--keystore"):
                properties.KeyStore = a

            elif o in ("-P", "--passphrase"):
                properties.Passphrase = a

            elif o in ("-b", "--browser"):
                properties.Browser = a

            elif o in ( '-V', '--variable' ):
                if '=' in a:
                    attr, value = a.split('=')
                    attributes[ attr.strip() ] = value

                elif os.path.exists( a ):
                    with open( a, 'r' ) as stream:
                        if a.endswith('.json'):
                            attrs = json.load( stream )

                        elif a.endswith('.yaml'):
                            attrs = yaml.load( stream, Loader = yaml.Loader )

                        else:
                            raise WrongFileType( f"{a} is unknown file type, .yaml or .json is allowed" )

                        attributes.update( attrs )

                else:
                    raise SyntaxError( f'Could not understand variable {a}' )

            else:
                assert False, "unhandled option"

        # Start of the logging to file and console
        logging.basicConfig( filename = properties.LogFile, level=properties.getLoglevel() )
        console = logging.StreamHandler( stream = sys.stdout )
        console.setLevel( properties.getLoglevel() )
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

        # Try to get the pykeystore
        attributes[ 'builtin' ] = Builtin( properties.getKeystore() )
        logging.info( f"Connecting to Selenium Server {properties.Server} with browser {properties.Browser}" )
        seleniumRunner = RunSeleniumIdeScript( properties.getBrowserOptions(), selenium_host = properties.Server )
        script_Filename = args.pop( 0 )
        if not os.path.exists( script_Filename ):
            raise FileNotFoundError( f"{script_Filename} is not found" )

        logging.info( f"Using Selenium IDE script {script_Filename}" )
        suite_name  = None
        case_name   = None
        if len( args ) > 0:
            command = args.pop( 0 )
            if command == 'test':
                case_name = args.pop( 0 )
                logging.info( f"Starting test case {case_name}" )

            elif command == 'suite':
                suite_name = args.pop( 0 )
                logging.info( f"Starting test suite {suite_name}" )

            else:
                raise SyntaxError( f"{command} is not understand, use 'test' or 'suite'" )

        logging.info( "Selenium IDE executing" )
        seleniumRunner.run_suite( script_Filename, suite_name = suite_name, testcase_name = case_name, **attributes )
        seleniumRunner.close()

    except Exception as exc:
        logging.exception( "Exception occured" )
        print( str( exc ), file = sys.stderr )

    return


if __name__ == '__main__':
    main()