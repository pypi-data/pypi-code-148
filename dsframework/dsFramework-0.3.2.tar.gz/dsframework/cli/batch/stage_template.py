"""! @brief Skeleton for implementing a specific stage to be used in a DataProc Workflow template."""
import argparse
import sys
import logging
from json import loads as json_loads
from dsframework.base.batch.pipeline_stage_base import ZIDS_BatchPipelineStage

logger = logging.getLogger(__name__)


##
# @file
# @brief generatedStageName class, inherits ZIDS_BatchPipelineStage base class.
class generatedStageName(ZIDS_BatchPipelineStage):
    """! The stage class that will be later converted to an executable job in a specific workflow.
    See class ExampleStage for an example implementation of the load, run and finish methods.
    A method for initiating a SparkSession is available in the base class ZIDS_BatchPipelineStage
    For logging please use the module-level logger - 'logger'
    """

    def __init__(self, stage_config):
        """! The Stage class (generatedStageName) initializer.
        Base class will load basic configuration parameters, additional fields should be added here

            Args:
                stage_config : Configuration dictionary, loaded from configuration file.
        """
        self.wf_name = generatedWFName
        super().__init__(stage_config, logger)

    def load(self):
        """! The \'load\' phase is for loading input dataframes and running input data tests if needed
        """
        raise NotImplementedError

    def run(self):
        """! The \'run\' phase is for the transform logic
        """
        raise NotImplementedError

    def finish(self):
        """! The \'finish\' phase is for saving output dataframes and running output data tests if needed
        """
        raise NotImplementedError


if __name__ == "__main__":
    """! Executes the stage by instantiating it and calling the __call__ function of the base class.
        
        Args:
            System argument 1 - Configuration file
            System argument 2 - Start date, received from Airflow
            System argument 3 - End date, received from Airflow
            System argument 4 - Placeholder for future parameters
    """

    # Handle input arguments
    parser = argparse.ArgumentParser(description='Configure and run generatedStageName class')
    parser.add_argument('config', type=str,
                        help='Configuration file')
    parser.add_argument('start_date', type=str, default='',
                        help='Start date, received from Airflow')
    parser.add_argument('end_date', type=str, default='',
                        help='End date, received from Airflow')
    parser.add_argument('params', nargs=argparse.REMAINDER,
                        help='Placeholder for future parameters')
    args = parser.parse_args()

    # Configure stage class and run
    stage = generatedStageName(json_loads(args.config))
    try:
        stage.update_stage_params(args.start_date, args.end_date, args.params)
        stage()
    except Exception as e:
        raise Exception(f" Stage failed with error: {e}")



