import datetime

from cloud_governance.cloud_management.aws.long_run.tag_long_run import TagLongRun
from cloud_governance.common.clouds.aws.price.price import AWSPrice
from cloud_governance.common.elasticsearch.elastic_upload import ElasticUpload
from cloud_governance.common.jira.jira import logger
from cloud_governance.common.jira.jira_operations import JiraOperations
from cloud_governance.common.ldap.ldap_search import LdapSearch
from cloud_governance.common.mails.mail_message import MailMessage
from cloud_governance.common.mails.postfix import Postfix
from cloud_governance.main.environment_variables import environment_variables

from cloud_governance.common.clouds.aws.ec2.ec2_operations import EC2Operations


class MonitorLongRun:
    FIRST_ALERT: int = 5
    SECOND_ALERT: int = 3
    DEFAULT_ADMINS = []#['athiruma@redhat.com', 'ebattat@redhat.com']#, 'natashba@redhat.com']
    HOURS_IN_SECONDS = 3600
    JIRA_ID = 'JiraId'

    def __init__(self, region_name: str = ''):
        self.__environment_variables_dict = environment_variables.environment_variables_dict
        self.__region_name = region_name if region_name else self.__environment_variables_dict.get('AWS_DEFAULT_REGION')
        self.__ec2_operations = EC2Operations(region=self.__region_name)
        self.__ldap_search = LdapSearch(ldap_host_name=self.__environment_variables_dict.get('LDAP_HOST_NAME'))
        self.__tag_long_run = TagLongRun()
        self.jira_operations = JiraOperations()
        self.__es_upload = ElasticUpload()
        self.__es_index = self.__environment_variables_dict.get('es_index')
        self.__aws_price = AWSPrice()
        self.__mail_message = MailMessage()
        self.__postfix = Postfix()

    def __get_instances_by_filtering(self, tag_key_name: str):
        """This method get the instances with the tag-key filter"""
        filters = {
            'Filters': [
                {
                    'Name': 'tag-key',
                    'Values': [tag_key_name]
                }
            ]
        }
        return self.__ec2_operations.get_instances(**filters)

    def __update_data_and_close_ticket(self, jira_id: str):
        """
        This method update data in the es and close the ticket
        """
        update_data = {'jira_id_state': 'Closed', 'instance_state': 'terminated', 'timestamp': datetime.datetime.utcnow()}
        self.__es_upload.elastic_search_operations.update_elasticsearch_index(index=self.__es_index, metadata=update_data, id=jira_id)
        self.jira_operations.move_issue_state(jira_id=jira_id, state='closed')

    def monitor_progress_issues(self):
        """
        This method monitor the in-progress issues, and closed the issue if the instance is terminated
        """
        jira_ids = self.jira_operations.get_all_issues_in_progress()
        es_jira_ids = []
        for jira_id in jira_ids:
            if self.__es_upload.elastic_search_operations.verify_elastic_index_doc_id(index=self.__es_index, doc_id=jira_id):
                es_jira_ids.append(jira_id)
        long_run_jira_ids = []
        long_run_instances = self.__get_instances_by_filtering(tag_key_name='JiraId')
        for instance in long_run_instances:
            for resource in instance['Instances']:
                jira_id = self.__ec2_operations.get_tag_value_from_tags(tags=resource.get('Tags'), tag_name='JiraId')
                if 'CLGOVN' not in jira_id:
                    jira_id = f'CLGOVN-{jira_id}'
                long_run_jira_ids.append(jira_id)
        terminated_jira_ids = set(es_jira_ids) - set(long_run_jira_ids)
        for jira_id in terminated_jira_ids:
            self.__update_data_and_close_ticket(jira_id=jira_id)
        return terminated_jira_ids

    def __calculate_days(self, launch_date: datetime):
        """This method return the no. of days"""
        today = datetime.date.today()
        diff_date = today - launch_date.date()
        return diff_date.days

    def __get_attached_time(self, volume_list: list):
        """
        This method return the root volume attached time
        """
        for mapping in volume_list:
            if mapping.get('Ebs').get('DeleteOnTermination'):
                return mapping.get('Ebs').get('AttachTime')
        return ''

    def __alert_instance_user(self, issues_data: dict):
        """
        This method alert the instance user, if the LongRunDays are running out
        """
        for jira_id, issue in issues_data.items():
            if '-' not in jira_id:
                jira_id = f'CLGOVN-{jira_id}'
            running_days, tags, instance_count, _, _, _, _ = issue
            long_run_days = int(self.__ec2_operations.get_tag_value_from_tags(tags=tags, tag_name='LongRunDays'))
            cc = self.DEFAULT_ADMINS
            user = 'athiruma'  # self.__ec2_operations.get_tag_value_from_tags(tags=tags, tag_name='User')
            name = self.__ec2_operations.get_tag_value_from_tags(tags=tags, tag_name='Name')
            approved_manager = self.__ec2_operations.get_tag_value_from_tags(tags=tags, tag_name='ApprovedManager')
            if approved_manager:
                cc.append(approved_manager)
            user_details = self.__ldap_search.get_user_details(user_name=user)
            if user_details:
                cc.append(f'{user_details.get("managerId")}@redhat.com')
            if running_days >= long_run_days - self.FIRST_ALERT:
                sub_tasks = self.jira_operations.get_jira_id_sub_tasks(jira_id=jira_id)
                if sub_tasks:
                    self.__tag_long_run.tag_extend_instances(sub_tasks=sub_tasks, jira_id=jira_id)
            subject, body = '', ''
            if running_days == long_run_days - self.FIRST_ALERT:
                subject, body = self.__mail_message.get_long_run_alert(user=user, days=self.FIRST_ALERT, jira_id=jira_id)
            elif running_days == long_run_days - self.SECOND_ALERT:
                subject, body = self.__mail_message.get_long_run_alert(user=user, days=self.FIRST_ALERT, jira_id=jira_id)
            else:
                if running_days >= long_run_days:
                    subject, body = self.__mail_message.get_long_run_expire_alert(user=user, jira_id=jira_id)
            if subject and body:
                self.__postfix.send_email_postfix(subject=subject, to=user, cc=cc, content=body, mime_type='html')

    def __diff_hours(self, launch_time: datetime):
        """This method return the total hours"""
        time_now = datetime.datetime.now(datetime.timezone.utc)
        diff_time = time_now - launch_time
        hours = divmod(diff_time.total_seconds(), self.HOURS_IN_SECONDS)
        return int(hours[0])

    def __monitor_instances(self):
        """
        This method monitoring the LongRun instances which have tag LongRunDays
        """
        jira_id_alerts = {}
        long_run_instances = self.__get_instances_by_filtering(tag_key_name='LongRunDays')
        for instance in long_run_instances:
            for resource in instance['Instances']:
                instance_id = resource.get('InstanceId')
                launch_datetime = self.__get_attached_time(volume_list=resource.get('BlockDeviceMappings'))
                if not launch_datetime:
                    launch_datetime = resource.get('LaunchTime')
                running_days = self.__calculate_days(launch_date=launch_datetime)
                tags = resource.get('Tags')
                hours = self.__diff_hours(launch_time=launch_datetime)
                price = round(float(self.__aws_price.get_price(instance=resource.get('InstanceType'), region=self.__aws_price.get_region_name(self.__region_name), os='Linux')) * hours, 3)
                jira_id = self.__ec2_operations.get_tag_value_from_tags(tag_name=self.JIRA_ID, tags=tags)
                instance_type = resource.get('InstanceType')
                if jira_id not in jira_id_alerts:
                    jira_id_alerts[jira_id] = [running_days, tags, 1, [instance_id], [resource.get('State')['Name']], [price], {instance_type: 1}]
                else:
                    jira_id_alerts[jira_id][2] += 1
                    jira_id_alerts[jira_id][3].append(instance_id)
                    jira_id_alerts[jira_id][4].append(resource.get('State')['Name'])
                    jira_id_alerts[jira_id][5].append(price)
                    jira_id_alerts[jira_id][6].setdefault(instance_type, 1)+1
        self.__alert_instance_user(issues_data=jira_id_alerts)
        return jira_id_alerts

    def run(self):
        """
        This method run the long run monitoring methods
        """
        response = self.monitor_progress_issues()
        logger.info(f"Closed JiraId's: {response}")
        return self.__monitor_instances()


