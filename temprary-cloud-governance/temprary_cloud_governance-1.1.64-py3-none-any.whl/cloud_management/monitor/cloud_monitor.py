from cloud_governance.cloud_management.aws.long_run.ec2_long_run import EC2LongRun
from cloud_governance.common.logger.logger_time_stamp import logger_time_stamp
from cloud_governance.main.environment_variables import environment_variables


class CloudMonitor:

    def __init__(self):
        self.__environment_variables_dict = environment_variables.environment_variables_dict
        self.__cloud_name = self.__environment_variables_dict.get('CLOUD_NAME')
        self.__monitor = self.__environment_variables_dict.get('MONITOR')

    @logger_time_stamp
    def aws_cloud_monitor(self):
        """
        This method ture if the cloud name is
        """
        if self.__monitor == 'long_run':
            ec2_long_run = EC2LongRun()
            ec2_long_run.run()

    @logger_time_stamp
    def run_cloud_monitor(self):
        """
        This verrify the cloud and run the monitor
        """
        if self.__cloud_name.upper() == "AWS".upper():
            self.aws_cloud_monitor()

    def run(self):
        """
        This method monitoring the cloud resources
        """
        self.run_cloud_monitor()
