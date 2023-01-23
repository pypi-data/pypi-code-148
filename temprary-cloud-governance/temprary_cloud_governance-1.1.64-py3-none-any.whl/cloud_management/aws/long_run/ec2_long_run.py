

import datetime

import boto3

from cloud_governance.cloud_management.aws.long_run.monitor_long_run import MonitorLongRun
from cloud_governance.cloud_management.aws.long_run.tag_long_run import TagLongRun
from cloud_governance.common.elasticsearch.elastic_upload import ElasticUpload
from cloud_governance.common.logger.init_logger import logger
from cloud_governance.common.logger.logger_time_stamp import logger_time_stamp

from cloud_governance.common.clouds.aws.ec2.ec2_operations import EC2Operations
from cloud_governance.common.jira.jira_operations import JiraOperations
from cloud_governance.main.environment_variables import environment_variables


class EC2LongRun:
    """
    This class monitor the LongRun EC2 instances.
    User Steps:
    1. Create a Jira Issue in Clouds portal, store the IssueId
    2. Create the EC2 instance, tag IssueId
    CI Steps:
    1. CI Look the instances which are tagged with IssueId
    2. Checks the Issue had manager approval in the comments
    3. If manger approval, append some LongRun tags ( Project, LongRunDays, Manager )
    4. else, send mail to the user, manager regarding approval
    """

    def __init__(self, region_name: str = ''):
        self.__environment_variables_dict = environment_variables.environment_variables_dict
        self.__region_name = region_name if region_name else self.__environment_variables_dict.get('AWS_DEFAULT_REGION')
        self.__tag_long_run = TagLongRun(region_name=region_name)
        self.__monitor_long_run = MonitorLongRun(region_name=region_name)
        self.__ec2_operations = EC2Operations()
        self.__es_upload = ElasticUpload()
        self.__es_index = self.__environment_variables_dict.get('es_index')
        self.__cloud_name = 'AWS'.upper()

    def prepare_to_upload_es(self, upload_data: dict):
        """
        This method beautify and upload data to ES
        """
        es_items = []
        for jira_id, issue_data in upload_data.items():
            issue_description = self.__tag_long_run.jira_operations.get_issue_description(jira_id=jira_id, state='any')
            cost_estimation = float(issue_description.get('CostEstimation', 0))
            cost_estimation += float(self.__tag_long_run.jira_operations.get_issue_sub_tasks_cost_estimation(jira_id=jira_id))
            if 'CLGOVN' not in jira_id:
                jira_id = f"CLGOVN-{jira_id}"
            running_days, tags, instance_count, instance_ids, instance_states, instance_prices, instance_types = issue_data
            launch_date = self.__ec2_operations.get_tag_value_from_tags(tags, 'LaunchTime')
            launch_date = launch_date.split()[0] if launch_date else str(datetime.datetime.now().date().strftime("%Y/%m/%d"))
            long_run_days = int(self.__ec2_operations.get_tag_value_from_tags(tags, 'LongRunDays'))
            approved_manager = self.__ec2_operations.get_tag_value_from_tags(tags, 'ApprovedManager')
            es_items.append({
                'cloud_name': self.__cloud_name,
                'jira_id': jira_id,
                'user': self.__ec2_operations.get_tag_value_from_tags(tags, 'User'),
                'approved_manager': approved_manager,
                'region': self.__region_name,
                'cost_estimation': cost_estimation,
                'project': self.__ec2_operations.get_tag_value_from_tags(tags, 'Project'),
                'launch_date': launch_date,
                'running_days': running_days,
                'long_run_days': long_run_days,
                'remaining_days': long_run_days - running_days,
                'instance_ids': instance_ids,
                'instance_types': [instance_types],
                'instance_state': instance_states,
                'instance_prices': instance_prices,
                'timestamp': datetime.datetime.utcnow(),
                'jira_id_state': 'in-progress'
            })
        self.__es_upload.es_upload_data(items=es_items, es_index=self.__es_index, set_index='jira_id')

    def __long_run(self):
        tag_response = self.__tag_long_run.run()
        if tag_response:
            logger.info(f'Tags are added to the JiraId tag instances: {tag_response}')
        monitor_response = self.__monitor_long_run.run()
        if monitor_response:
            self.prepare_to_upload_es(monitor_response)

    def run(self):
        """
        This method run the long run methods
        """
        return self.__long_run()
