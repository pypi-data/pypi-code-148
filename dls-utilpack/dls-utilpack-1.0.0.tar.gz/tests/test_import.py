import logging

from dls_utilpack.describe import describe
from dls_utilpack.import_class import import_module_classname

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestImportModuleClassname(BaseTester):
    def test(self, constants, logging_setup, output_directory):
        """ """

        self.main(constants, output_directory)

    # ----------------------------------------------------------------------------------------
    async def _main_coroutine(
        self,
        constants,
        output_directory,
    ):
        """ """

        class_object = import_module_classname("tests.task_classes.task_z::TaskZ")

        task_object = class_object()

        logger.debug(describe("task_object", task_object))
