"""
WARNING: AUTOGENERATED CODE

    This code was generated by a tool.
    Autogenerated on: 2023-01-10 10:57:29
    
    Manual changes to this file may cause unexpected behavior in your application.
    Manual changes to this file will be overwritten if the code is regenerated.
"""

from pyopencga.rest_clients._parent_rest_clients import _ParentRestClient


class Project(_ParentRestClient):
    """
    This class contains methods for the 'Projects' webservices
    Client version: 2.6.0-SNAPSHOT [cd4c96caf1cb7afcdec5f54a7de72bde4f63820e]
    PATH: /{apiVersion}/projects
    """

    def __init__(self, configuration, token=None, login_handler=None, *args, **kwargs):
        super(Project, self).__init__(configuration, token, login_handler, *args, **kwargs)

    def create(self, data=None, **options):
        """
        Create a new project.
        PATH: /{apiVersion}/projects/create

        :param dict data: JSON containing the mandatory parameters. (REQUIRED)
        :param str include: Fields included in the response, whole JSON path
            must be provided.
        :param str exclude: Fields excluded in the response, whole JSON path
            must be provided.
        :param bool include_result: Flag indicating to include the created or
            updated document result in the response.
        """

        return self._post(category='projects', resource='create', data=data, **options)

    def search(self, **options):
        """
        Search projects.
        PATH: /{apiVersion}/projects/search

        :param str include: Fields included in the response, whole JSON path
            must be provided.
        :param str exclude: Fields excluded in the response, whole JSON path
            must be provided.
        :param int limit: Number of results to be returned.
        :param int skip: Number of results to skip.
        :param str owner: Owner of the project.
        :param str id: Project [user@]project where project can be either the
            ID or the alias.
        :param str name: Project name.
        :param str fqn: Project fqn.
        :param str organization: Project organization.
        :param str description: Project description.
        :param str study: Study id.
        :param str creation_date: Creation date. Format: yyyyMMddHHmmss.
            Examples: >2018, 2017-2018, <201805.
        :param str modification_date: Modification date. Format:
            yyyyMMddHHmmss. Examples: >2018, 2017-2018, <201805.
        :param str internal_status: Filter by internal status.
        :param str attributes: Attributes.
        """

        return self._get(category='projects', resource='search', **options)

    def aggregation_stats(self, projects, **options):
        """
        Fetch catalog project stats.
        PATH: /{apiVersion}/projects/{projects}/aggregationStats

        :param str projects: Comma separated list of projects [user@]project
            up to a maximum of 100. (REQUIRED)
        :param bool default: Calculate default stats.
        :param str file_fields: List of file fields separated by semicolons,
            e.g.: studies;type. For nested fields use >>, e.g.:
            studies>>biotype;type.
        :param str individual_fields: List of individual fields separated by
            semicolons, e.g.: studies;type. For nested fields use >>, e.g.:
            studies>>biotype;type.
        :param str family_fields: List of family fields separated by
            semicolons, e.g.: studies;type. For nested fields use >>, e.g.:
            studies>>biotype;type.
        :param str sample_fields: List of sample fields separated by
            semicolons, e.g.: studies;type. For nested fields use >>, e.g.:
            studies>>biotype;type.
        :param str cohort_fields: List of cohort fields separated by
            semicolons, e.g.: studies;type. For nested fields use >>, e.g.:
            studies>>biotype;type.
        :param str job_fields: List of job fields separated by semicolons,
            e.g.: studies;type. For nested fields use >>, e.g.:
            studies>>biotype;type.
        """

        return self._get(category='projects', resource='aggregationStats', query_id=projects, **options)

    def info(self, projects, **options):
        """
        Fetch project information.
        PATH: /{apiVersion}/projects/{projects}/info

        :param str projects: Comma separated list of projects [user@]project
            up to a maximum of 100. (REQUIRED)
        :param str include: Fields included in the response, whole JSON path
            must be provided.
        :param str exclude: Fields excluded in the response, whole JSON path
            must be provided.
        """

        return self._get(category='projects', resource='info', query_id=projects, **options)

    def inc_release(self, project, **options):
        """
        Increment current release number in the project.
        PATH: /{apiVersion}/projects/{project}/incRelease

        :param str project: Project [user@]project where project can be either
            the ID or the alias. (REQUIRED)
        """

        return self._post(category='projects', resource='incRelease', query_id=project, **options)

    def studies(self, project, **options):
        """
        Fetch all the studies contained in the project.
        PATH: /{apiVersion}/projects/{project}/studies

        :param str project: Project [user@]project where project can be either
            the ID or the alias. (REQUIRED)
        :param str include: Fields included in the response, whole JSON path
            must be provided.
        :param str exclude: Fields excluded in the response, whole JSON path
            must be provided.
        :param int limit: Number of results to be returned.
        :param int skip: Number of results to skip.
        """

        return self._get(category='projects', resource='studies', query_id=project, **options)

    def update(self, project, data=None, **options):
        """
        Update some project attributes.
        PATH: /{apiVersion}/projects/{project}/update

        :param dict data: JSON containing the params to be updated. It will be
            only possible to update organism fields not previously defined.
            (REQUIRED)
        :param str project: Project [user@]project where project can be either
            the ID or the alias. (REQUIRED)
        :param str include: Fields included in the response, whole JSON path
            must be provided.
        :param str exclude: Fields excluded in the response, whole JSON path
            must be provided.
        :param bool include_result: Flag indicating to include the created or
            updated document result in the response.
        """

        return self._post(category='projects', resource='update', query_id=project, data=data, **options)

