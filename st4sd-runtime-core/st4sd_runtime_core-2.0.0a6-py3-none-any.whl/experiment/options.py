import experiment.model.conf
import optparse
import six
import os
from typing import Tuple, List, Optional



def parser_generate_elaunch():
    # type: () -> optparse.OptionParser
    """Generate a optparse.OptionParser for elaunch.py commandline arguments"""
    usage = "usage: %prog [options] [package]"
    import pkg_resources

    parser = optparse.OptionParser(usage=usage,
                                   version=pkg_resources.get_distribution("st4sd-runtime-core").version,
                                   description=__doc__)

    # HACK: Daresbury system dependant
    projectDir = os.path.split(os.path.expanduser("~"))[0]
    haltfile = os.path.join(projectDir, 'shared/CHPCBackend/.halt_backend')
    killfile = os.path.join(projectDir, 'shared/CHPCBackend/.kill_backend')

    launchOptions = optparse.OptionGroup(parser, "Launch Options")
    parser.add_option_group(launchOptions)

    restartGroup = optparse.OptionGroup(parser, "Restart Options - Use instead of launch options")
    parser.add_option_group(restartGroup)

    cdbGroup = optparse.OptionGroup(parser, "Centralized Database (CDB) Options - (used by memoization)")
    parser.add_option_group(cdbGroup)

    s3Group = optparse.OptionGroup(parser, "Options to store workflow instance to S3 bucket")
    available_package_types = [key for key in list(experiment.model.conf.ExperimentConfigurationFactory.format_map.keys())
                               if isinstance(key, six.string_types)]

    # VV: Leave the default values as None so that we can detect if the user has specified a value
    #     there's probably a smarter way to do this but it's good enough
    parser.add_option('--cwlFile', dest='cwlFile',
                      help='Override cwl main file - default main.cwl',
                      default=None)
    parser.add_option('--cwlJobOrderFile', dest='cwlJobOrderFile',
                      help='Override cwl job-order file. Set the option to '' to disable loading a job-order file '
                           '- default job_order.yml',
                      default=None)

    parser.add_option("--formatPriority", dest="formatPriority",
                      help="Comma separated list of configuration format priorities that "
                           "guides the selection of the Configuration parser which "
                           "will be used to read the Experiment configuration (Available options: %s)."
                           " - default '%%default'" % available_package_types,
                      default=','.join(experiment.model.conf.ExperimentConfigurationFactory.default_priority)
                      )
    parser.add_option("-l", "--logLevel", dest="logLevel",
                      help="The level of logging. Default %default",
                      type="int",
                      default=20,
                      metavar="LOGGING")
    parser.add_option("", "--hybrid", dest="hybrid",
                      help="Indicates the experiment will run in an LSF managed hybrid environment. "
                           "If given the value of this argument must be the default queue for the remote side of "
                           "the environment. NB: Must be specified for launch AND restart.",
                      default=None,
                      metavar="HYBRID")
    parser.add_option("", "--haltFile", dest="haltFile",
                      help="Name of file periodically polled to see if process should halt - default %default.",
                      default=haltfile,
                      metavar="HALTFILE")
    parser.add_option("", "--killFile", dest="killFile",
                      help="Name of file periodically polled to see if process should be killed - default %default.",
                      default=killfile,
                      metavar="KILLFILE")
    parser.add_option("", "--fuzzyMemoization", dest="fuzzyMemoization",
                      help="Enables fallback fuzzy-memoization for cases where hard memoization fails to find "
                           "suitable past components. Fuzzy memoization replaces dependencies to files generated "
                           "by components to dependencies to the producer component + the name of the file. Default "
                           "is not to attempt fuzzy memoization at all.",
                      default=False, action="store_true")

    launchOptions.add_option("-i", "--inputs", dest="inputs",
                             help="A comma separated list of input files. Can be specified multiple times",
                             action='append',
                             default=[],
                             metavar="INPUTS")
    launchOptions.add_option("-d", "--data", dest="data",
                             help="A path to a file with the same name as a file in the experiments data/ directory. "
                                  "The named file will replace the file in the data directory",
                             action="append",
                             default=[],
                             metavar="DATA")
    launchOptions.add_option("-a", "--variables", dest="variables",
                             help="Path to a file that will be used to define instance specific variables",
                             default=None,
                             metavar="VARIABLES")
    launchOptions.add_option("-p", "--platform", dest="platform",
                             help="The platform the experiment is being deployed on. "
                                  "Use when an experiment support configurations for multiple platforms/systems",
                             default=None,
                             metavar="PLATFORM")
    launchOptions.add_option("", "--instanceName", dest="instance_name",
                             help="Override the base name of the instance dir, can be"
                                  "combined with --nostamp. (default is <package>.instance)",
                             default=None,
                             metavar="INSTANCE_NAME")
    launchOptions.add_option("", "--nostamp", dest="stamp",
                             help="Do not add timestamp to instance names.",
                             action="store_false",
                             default=True,
                             metavar="NOSTAMP")
    launchOptions.add_option("", "--metadata", dest="user_metadata_file",
                             help="Path to YAML file containing user metadata (dictionary with strings as keys)."
                                  "The `user_metadata` dictionary is stored in the generated `elaunch.yaml` file "
                                  "under the field `userMetadata`",
                             default=None, metavar="USER_METADATA_FILE")
    launchOptions.add_option("-m", "", dest="user_metadata_dict",
                             help="Update user_metadata dictionary with `key:value` entry",
                             default=[], metavar="USER_METADATA_ENTRY", action="append")
    launchOptions.add_option('--enableOptimizer', dest='enable_optimizer',
                             default='n', choices=['y', 'n'],
                             help='Enable/disable optimizer (y/n). Default %default')
    launchOptions.add_option('', '--discovererMonitorDir', dest='discoverer_monitor_dir',
                             help='Point elaunch.py to a directory which is monitored by some ExperimentDiscoverer '
                                  'daemon so that the resulting Experiment Instance is automatically register '
                                  'to the centralized experiment instance database.',
                             default=None,
                             metavar='DISCOVERER_MONITOR_DIR')
    launchOptions.add_option('', '--ignoreTestExecutablesError', dest='ignoreTestExecutablesError',
                             default=False, action='store_true',
                             help="Don't treat issues during executable checking and resolution as errors. "
                                  "This may be useful in scenarios where a backend is unavailable (e.g. kubernetes, "
                                  "LSF, etc) but there exist cached memoization candidates available which can be used "
                                  "instead of executing a task.")
    launchOptions.add_option('', '--ignoreInitializeBackendError', default=False, action='store_true',
                             dest='ignoreInitializeBackendError',
                             help="Don't treat issues during backend initialization as errors. "
                                  "This may be useful in scenarios where a backend is unavailable (e.g. kubernetes, "
                                  "LSF, etc) but there exist cached memoization candidates available which can be used "
                                  "instead of executing a task.")

    restartGroup.add_option("-r", "--restart", dest="restart",
                            help="Restart at given stage"
                                 "Note this option requires an existing instance is passed to the experiment NOT "
                                 "a package. If specified this option overrides any option in the LAUNCH group. ",
                            type="int",
                            default=None,
                            metavar="RESTART")
    restartGroup.add_option("", "--restageData", dest="stageData",
                            help='If specified components inputs (copy/links) will be staged on restart. '
                                 'The default is not to stage i.e. the existing staged versions of any files are used',
                            action='store_true',
                            default=False)
    restartGroup.add_option("", "--noRestartHooks", dest="useRestartHooks",
                            help='If specified non-repeating components are started as in a normal run. The default '
                                 'behaviour is to restart as if they processes exited due to ResourceExhausted. This '
                                 'will cause any restart hooks for the component to be executed.',
                            action='store_false',
                            default=True)

    cdbGroup.add_option('--mongoEndpoint', dest='mongoEndPoint',
                        help='MongoDB endpoint; can either be tcp://<ip>:<port> or http[s]://domain. `tcp://` '
                             'endpoints need also --mongo-user, and --mongo-password (possibly --mongo-database, '
                             '--mongo-collection, and --mongo-authsource)', default=None)
    cdbGroup.add_option('--mongoUser', dest='mongoUser',
                        help='Username to be used for MongoDB authentication (only necessary for tcp:// endpoints)',
                        default=None)
    cdbGroup.add_option('--mongoPassword', dest='mongoPassword',
                        help='Password to be used for MongoDB authentication (only necessary for tcp:// endpoints)',
                        default=None)
    cdbGroup.add_option('--mongoAuthsource', dest='mongoAuthSource',
                        help='Database name to authenticate (may only be specified for for tcp:// endpoints)',
                        default=None)
    cdbGroup.add_option('--mongoDatabase', dest='mongoDatabase',
                        help='Database that hosts MongoDB items (may only be specified for for tcp:// endpoints)',
                        default=None)
    cdbGroup.add_option('--mongoCollection', dest='mongoCollection',
                        help='Collection to be used with MongoDB database '
                             '(may only be specified for for tcp:// endpoints)',
                        default=None)
    cdbGroup.add_option('--cdbRegistry', dest='cdbRegistry', default=None,
                        help='Endpoint of CDB registry can either be tcp://<ip>:<port> or http[s]://domain')

    s3Group.add_option('--s3StoreToURI', dest='s3StoreToURI',
                       help="S3 URI (i.e. s3://<bucket-name>/path/to/folder) under which the entire workflow instance "
                            "directory will be updated (with the exception of folders/files that are symbolic links). "
                            "You must also specify a valid --s3AuthWithEnvVars OR --s3AuthBearer64 parameter.",
                       default=None)
    s3Group.add_option('--s3AuthWithEnvVars', dest='s3AuthWithEnvVars',
                       help='Authenticate to S3 end-point using the information from the environment variables: '
                            'S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY, S3_END_POINT', default=False, action='store_true')
    s3Group.add_option('--s3AuthBearer64', dest='s3AuthBearer64',
                       help='Authenticate to S3 end-point using the information provided in this option. This '
                            'value is expected to be a valid JSON dictionary with the keys S3_ACCESS_KEY_ID, '
                            'S3_SECRET_ACCESS_KEY, S3_END_POINT. The string representing the JSON dictionary '
                            'is expected to be base64 encoded.', default=None)

    return parser


def parser_elaunch_arguments(parser=None, args=None, values=None):
    # type: (...) -> Tuple[optparse.Values, List[str]]
    """Parse the elaunch.py commandline arguments

    Args:
        parser(Optional[optparse.OptionParser]): Parser to use, defaults to parser_generate_elaunch()
        args(Optional[List[str]]): List of arguments to elaunch.py (defaults to sys.argv[1:])
        values(Optional[optparse.Values]): Values is an optional optparse.Values instance to hold extracted arguments

    Returns

        A (optparse.Values, List[str]) tuple. The first value contains the extracted arguments, the second any
        leftover bits of `args` which were not used to extract arguments by the parser.
    """
    parser = parser or parser_generate_elaunch()
    options, args = parser.parse_args(args=args, values=values)
    options.formatPriority = options.formatPriority.split(',')
    options.enable_optimizer = {'n': False, 'y': True}[options.enable_optimizer]

    return options, args
