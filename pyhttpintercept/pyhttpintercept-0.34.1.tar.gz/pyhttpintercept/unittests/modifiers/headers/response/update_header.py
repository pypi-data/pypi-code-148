# encoding: utf-8

import logging_helper
from pyhttpintercept.helpers import run_ad_hoc_header_modifier
from pyhttpintercept.intercept.modifiers.headers.response import update_header as module_to_test
from timingsutil import Stopwatch


logging = logging_helper.setup_logging()

TEST_URL = u'http://echo.jsontest.com/key/value/one/two'

headers_for_update = run_ad_hoc_header_modifier(module=module_to_test,
                                      request=TEST_URL,
                                      filter=u'*',  # Test Wildcard (invalid regex)
                                      params='unit-test:Tom')

assert headers_for_update['unit-test'] == "Tom"


headers_for_update = run_ad_hoc_header_modifier(module=module_to_test,
                                      request=TEST_URL,
                                      filter=u'.*',  # Test Wildcard (valid regex)
                                      params='unit-test:Dick')

assert headers_for_update['unit-test'] == "Dick"

headers_for_update = run_ad_hoc_header_modifier(module=module_to_test,
                                      request=TEST_URL,
                                      filter=u'jsontest',  # Test string match
                                      params='unit-test:Harry')

assert headers_for_update['unit-test'] == "Harry"

headers_for_update = run_ad_hoc_header_modifier(module=module_to_test,
                                      request=TEST_URL,
                                      filter=u'lighter',  # Not a match
                                      params='unit-test:Jane')

assert len(headers_for_update) == 0
