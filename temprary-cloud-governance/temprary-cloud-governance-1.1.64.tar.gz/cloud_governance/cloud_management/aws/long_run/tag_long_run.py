import boto3

from cloud_governance.common.logger.init_logger import logger
from cloud_governance.common.logger.logger_time_stamp import logger_time_stamp

from cloud_governance.common.clouds.aws.ec2.ec2_operations import EC2Operations
from cloud_governance.common.jira.jira_operations import JiraOperations
from cloud_governance.main.environment_variables import environment_variables


class TagLongRun:

    DEFAULT_SEARCH_TAG = 'JiraId'
    KEY = 'Key'
    VALUE = 'Value'

    def __init__(self, region_name: str = ''):
        self.__environment_variables_dict = environment_variables.environment_variables_dict
        self.__region_name = region_name if region_name else self.__environment_variables_dict.get('AWS_DEFAULT_REGION')
        self.__ec2_client = boto3.client('ec2', region_name=self.__region_name)
        self.__ec2_operations = EC2Operations(region=self.__region_name)
        self.jira_operations = JiraOperations()

    @logger_time_stamp
    def tag_extend_instances(self, sub_tasks: list, jira_id: str):
        """This method extend the tags of longrun"""
        filters = {'Filters': [{'Name': 'tag:JiraId', 'Values': [jira_id]}]}
        extend_long_run_days = 0
        for task_id in sub_tasks:
            description = self.jira_operations.get_issue_description(jira_id=task_id, sub_task=True)
            extend_long_run_days += int(description.get('Days'))
        instances = self.__ec2_operations.get_instances(**filters)
        long_run_days = 0
        instance_ids = []
        for instance in instances:
            for resource in instance['Instances']:
                tags = resource.get('Tags')
                if tags:
                    long_run_days = int(
                        self.__ec2_operations.get_tag_value_from_tags(tag_name='LongRunDays', tags=tags))
                instance_ids.append(resource.get('InstanceId'))
        if long_run_days > 0:
            long_run_days += extend_long_run_days
            tag = [{'Key': 'LongRunDays', 'Value': str(long_run_days)}]
            self.__ec2_client.create_tags(Resources=instance_ids, Tags=tag)
            for task_id in sub_tasks:
                self.jira_operations.move_issue_state(jira_id=task_id, state='closed')

    @logger_time_stamp
    def __tag_jira_id_attach_instance(self, jira_id: str, instance_id: str):
        """
        This method tag the long run instance with tags
        """
        jira_description = self.jira_operations.get_issue_description(jira_id=jira_id, state='31')
        if jira_description:
            long_run_days = jira_description.get('Days')
            manager_approved = jira_description.get('ApprovedManager')
            if not manager_approved:
                manager_approved = jira_description.get('ManagerApprovalAddress')
            user_email = jira_description.get('EmailAddress')
            user = user_email.split('@')[0]
            project = jira_description.get('Project')
            tags = [{self.KEY: 'LongRunDays', self.VALUE: long_run_days},
                    {self.KEY: 'ApprovedManager', self.VALUE: manager_approved},
                    {self.KEY: 'Project', self.VALUE: project.upper()},
                    {self.KEY: 'Email', self.VALUE: user_email},
                    {self.KEY: self.DEFAULT_SEARCH_TAG, self.VALUE: jira_id},
                    {self.KEY: 'User', self.VALUE: user}]
            self.__ec2_client.create_tags(Resources=[instance_id], Tags=tags)
            self.jira_operations.move_issue_state(jira_id=jira_id, state='inprogress')
            logger.info(f'Extra tags are added to the instances: {instance_id}, had an jira_id: {jira_id}')
            return True
        return False

    @logger_time_stamp
    def __find_tag_instances(self):
        """
        This method list the instances and tagged the instances which have the tag IssueId
        """
        instances = self.__ec2_operations.get_instances()
        jira_id_instances = {}
        for instance in instances:
            for resource in instance['Instances']:
                instance_id = resource.get('InstanceId')
                jira_id = ''
                if resource.get('Tags'):
                    jira_id = self.__ec2_operations.get_tag_value_from_tags(tags=resource.get('Tags'), tag_name=self.DEFAULT_SEARCH_TAG)
                if jira_id:
                    long_run_days = self.__ec2_operations.get_tag_value_from_tags(tags=resource.get('Tags'), tag_name='LongRunDays')
                    if not long_run_days:
                        if self.__tag_jira_id_attach_instance(jira_id=jira_id, instance_id=instance_id):
                            jira_id_instances.setdefault(jira_id, []).append(instance_id)
        return jira_id_instances

    def run(self):
        """
        This method run the tagging of long run
        """
        return self.__find_tag_instances()
