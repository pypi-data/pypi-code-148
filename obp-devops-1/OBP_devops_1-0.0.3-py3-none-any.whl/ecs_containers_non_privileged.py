import logging

from botocore.exceptions import ClientError

from OBP_devops_1.utils import get_regions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def ecs_containers_non_privileged(self, regions) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside OBP DevOps :: ecs_containers_non_privileged()")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id7.2'
    compliance_type = "ecs_containers_non_privileged"
    description = "Checks if the privileged parameter in the container definition of ECSTaskDefinitions is set to ‘true’. "
    resource_type = "AWS ECS TaskDefinition"
    risk_level = 'High'

    regions = self.session.get_available_regions('ecs')

    for region in regions:
        try:
            client = self.session.client('ecs', region_name=region)
            task_definitions = client.list_task_definitions()['taskDefinitionArns']
            for task_definition in task_definitions:
                resp = client.describe_task_definition(taskDefinition=task_definition)
                container_definitions = resp['taskDefinition']['containerDefinitions']
                for definition in container_definitions:

                    try:
                        if definition['privileged'] == 'False':
                            raise KeyError

                    except KeyError:
                        result = False
                        offenders.append(definition['name'])
                        failReason = "The privileged parameter in the container definition of ECSTaskDefinitions is set to False"
                        continue
        
        except ClientError as e:
            logger.error("Something went wrong with the region {}: {}".format(region, e))
            
    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }
