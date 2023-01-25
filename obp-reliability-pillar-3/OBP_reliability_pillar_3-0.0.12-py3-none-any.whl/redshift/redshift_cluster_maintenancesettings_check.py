import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks compliance for redshift cluster maintenance settings check
def redshift_cluster_maintenance_settings_check(self) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside redshift :: redshift_cluster_maintenance_settings_check()")

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.83'
    compliance_type = "Redshift cluster maintenance settings check"
    description = "Checks whether Amazon Redshift clusters have the specified maintenance settings"
    resource_type = "Redshift"
    risk_level = 'Medium'

    regions = self.session.get_available_regions('redshift')

    for region in regions:
        try:
            client = self.session.client('redshift', region_name=region)
            marker = ''
            while True:
                if marker == '' or marker is None:
                    response = client.describe_clusters()
                else:
                    response = client.describe_clusters(
                        Marker=marker
                    )
                for cluster in response['Clusters']:
                    version_upgrade = cluster['AllowVersionUpgrade']
                    window = cluster['PreferredMaintenanceWindow']
                    automated_snapshot_retention_period = cluster['AutomatedSnapshotRetentionPeriod']

                    if not version_upgrade and automated_snapshot_retention_period > 0:
                        result = False
                        failReason = 'allowVersionUpgrade is not enabled'
                        offenders.append(cluster['ClusterIdentifier'])

                try:
                    marker = response['Marker']
                    if marker == '':
                        break
                except KeyError:
                    break

        except ClientError as e:
            logger.error("Something went wrong with the region {}: {}".format(region, e))

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'ControlId': control_id,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level
    }
