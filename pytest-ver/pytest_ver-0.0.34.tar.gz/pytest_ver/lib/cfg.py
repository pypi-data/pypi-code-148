import argparse
import json
import os
import re

import jsmin

from . import services
from .build_info import BuildInfo
from .constants import Constants
from .report.common.page_info import PageInfo


# -------------------
## Holds configuration functions and globals
class Cfg:
    # -------------------
    ## constructor
    def __init__(self):
        # --- Public - default settings
        ## holds path to cfg file
        self.cfg_path = 'cfg.json'
        ## holds path to output directory
        self.outdir = 'out'

        ## holds storage type: one of dev, shared
        self.storage_type = 'dev'
        ## holds path to the shared directory to publish; used only if storage_type is shared
        self.storage_shared_dir = None
        ## report mode; use to suppress the creation of JSON files or not
        self.report_mode = False
        ## holds run type: one of formal, dryrun, dev
        self.test_run_type = 'dev'
        ## holds run id
        self.test_run_id = 'dev-001'
        ## holds format to use for DTS
        self.dts_format = "%Y-%m-%d %H:%M:%S %Z"
        ## flag indicates to use UTC or local time
        self.use_utc = False
        ## holds page info e.g. headers and footers
        self.page_info = PageInfo()
        ## holds current test name
        self.test_script = None
        ## holds path to the requirements json file
        self.reqmt_json_path = None

        ## test protocol file name - no results
        self.tp_protocol_fname = 'test_protocol'
        ## test report file name - with results
        self.tp_report_fname = 'test_report'

        ## report types to generate, valid: txt, pdf, docx
        self.report_types = ['txt', 'pdf', 'docx']

        ## internal IUV use only; indicates if in IUV mode
        self.iuvmode = False

    # TODO refactor to cli class
    # -------------------
    ## add option for conftest.py behavior
    #
    # @param parser the pytest parser object
    # @return None
    def cli_addoption(self, parser):
        parser.addoption('--iuvmode', action='store_true', dest='iuvmode', default=False)
        parser.addoption('--cfg_path', action='store', dest='cfg_path', default=None)

    # -------------------
    ## handle the incoming CLI flags for conftest.py behavior
    #
    # @param config the pytest config reference
    # @return None
    def cli_configure(self, config):
        self.cli_set('iuvmode', config.getoption('iuvmode'))
        if config.getoption('cfg_path') is not None:
            self.cli_set('cfg_path', str(config.getoption('cfg_path')))

        if self.iuvmode:
            services.harness.init_iuv()

    # -------------------
    ## add option for CLI behavior
    #
    # @return None
    def cli_parse(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--cfg_path', action='store', dest='cfg_path', default=None)
        parser.add_argument('--iuvmode', action='store_true', dest='iuvmode', default=False)
        args, _ = parser.parse_known_args()

        self.cli_set('iuvmode', args.iuvmode)
        if args.cfg_path is not None:
            self.cli_set('cfg_path', args.cfg_path)

    # -------------------
    ## used to set command line interface switches
    #
    # @param name   the name of the variable
    # @param value  the value of the variable to use
    # @return None
    def cli_set(self, name, value):
        if name in ['cfg_path', 'iuvmode']:
            setattr(self, name, value)

    # -------------------
    ## initialize - step1
    # read cfg json file
    #
    # @param report_mode used to suppress creation of out/*.json files (for reporting)
    # @return None
    def init(self, report_mode):
        self._read_ini()

        self.report_mode = report_mode

        if not os.path.isdir(self.outdir):  # pragma: no cover
            # coverage: in IUV and UT, outdir is created by scripts
            os.mkdir(self.outdir)

        self.page_info.check()

    # -------------------
    ## initialize - step2
    # get the current test name
    #
    # @return None
    def init2(self):
        self.test_script = None
        if 'PYTEST_CURRENT_TEST' in os.environ:  # pragma: no cover
            # coverage: in IUV and UT, variable is always set
            # eg.  ver/test_sample_ver1.py
            m = re.search(r'test_(\w+)\.py::(\w+)', os.getenv('PYTEST_CURRENT_TEST'))
            if m:
                self.test_script = m.group(1)

    # -------------------
    ## report configuration to the log
    #
    # @return None
    def report(self):
        services.logger.start('Cfg:')
        services.logger.line(f"  {'Cfg path': <20}: {self.cfg_path}")
        services.logger.line(f"  {'Output Dir': <20}: {self.outdir}")
        services.logger.line(f"  {'Storage Type': <20}: {self.storage_type}")
        services.logger.line(f"  {'Report mode': <20}: {self.report_mode}")
        services.logger.line(f"  {'Shared dir': <20}: {self.storage_shared_dir}")
        services.logger.line(f"  {'Test Run ID': <20}: {self.test_run_id}")
        services.logger.line(f"  {'Req. json path': <20}: {self.reqmt_json_path}")
        if self.iuvmode:  # pragma: no cover
            # coverage: iuvmode is always set during IUV and UT runs
            services.logger.line(f"  {'IUV mode': <20}: {self.iuvmode}")

        services.logger.line(f"  {'pytest version': <20}: {Constants.version}")
        services.logger.line(f"  {'git sha': <20}: {BuildInfo.git_sha}")
        services.logger.line(f"  {'git branch': <20}: {BuildInfo.git_branch}")
        services.logger.line(f"  {'git uncommitted': <20}: {BuildInfo.git_uncommitted}")
        services.logger.line(f"  {'git unpushed': <20}: {BuildInfo.git_unpushed}")

        services.logger.line('')

    # -------------------
    ## read the cfg json file
    # set attributes in this class based on content
    #
    # @return None
    def _read_ini(self):
        if not os.path.isfile(self.cfg_path):
            services.logger.warn(f'{self.cfg_path} not found')
            return

        # load json file
        with open(self.cfg_path, 'r', encoding='utf-8') as fp:
            cleanj = jsmin.jsmin(fp.read())
            j = json.loads(cleanj)

        # override and/or add to available attributes
        for key, value in j.items():
            if key == 'tp_report':
                self.page_info.init_tp_report(value)
            elif key == 'tp_protocol':
                self.page_info.init_tp_protocol(value)
            elif key == 'trace':
                self.page_info.init_trace(value)
            elif key == 'summary':
                self.page_info.init_summary(value)
            else:
                if not hasattr(self, key):
                    services.logger.warn(f'json key "{key}" not found in cfg class')
                setattr(self, key, value)
