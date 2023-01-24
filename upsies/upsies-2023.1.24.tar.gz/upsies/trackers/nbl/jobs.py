"""
Concrete :class:`~.base.TrackerJobsBase` subclass for NBL
"""

from ... import jobs
from ...utils import cached_property
from .. import base

import logging  # isort:skip
_log = logging.getLogger(__name__)


class NblTrackerJobs(base.TrackerJobsBase):
    @cached_property
    def jobs_before_upload(self):
        return (
            self.create_torrent_job,
            self.mediainfo_job,
            self.tvmaze_job,
            self.category_job,
        )

    @cached_property
    def category_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('category'),
            label='Category',
            condition=self.make_job_condition('category_job'),
            choices=(
                ('Season', '3'),
                ('Episode', '1'),
            ),
            autodetected=str(self.release_name.type).capitalize(),
            **self.common_job_args(),
        )

    @property
    def post_data(self):
        return {
            'api_key': self.options['apikey'],
            'category': self.get_job_attribute(self.category_job, 'choice'),
            'tvmazeid': self.get_job_output(self.tvmaze_job, slice=0),
            'mediainfo': self.get_job_output(self.mediainfo_job, slice=0),
        }

    @property
    def torrent_filepath(self):
        return self.get_job_output(self.create_torrent_job, slice=0)
