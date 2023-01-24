"""
Concrete :class:`~.base.TrackerJobsBase` subclass for MTV
"""

import re

from ... import __homepage__, __project_name__, jobs, utils
from ...utils import cached_property
from ...utils.release import ReleaseType
from ..base import TrackerJobsBase

import logging  # isort:skip
_log = logging.getLogger(__name__)


class MtvTrackerJobs(TrackerJobsBase):

    torrent_piece_size_max = 8 * 2**20  # 8 MiB

    @cached_property
    def jobs_before_upload(self):
        return (
            # Background jobs
            self.create_torrent_job,
            self.mediainfo_job,
            self.screenshots_job,
            self.upload_screenshots_job,

            # Interactive jobs
            self.category_job,
            self.imdb_job,
            self.scene_check_job,
            self.title_job,
            self.description_job,
        )

    @property
    def isolated_jobs(self):
        if self.options.get('only_description', False):
            return (
                self.mediainfo_job,
                self.screenshots_job,
                self.upload_screenshots_job,
                self.description_job,
            )
        elif self.options.get('only_title', False):
            return (
                self.category_job,
                self.imdb_job,
                self.scene_check_job,
                self.title_job,
            )
        else:
            # Activate all jobs
            return ()

    @cached_property
    def category_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('category'),
            label='Category',
            condition=self.make_job_condition('category_job'),
            autodetect=self.autodetect_category,
            choices=[
                (c['label'], c['value'])
                for c in self._categories
            ],
            **self.common_job_args(),
        )

    _categories = (
        {'label': 'HD Season', 'value': '5', 'type': ReleaseType.season},
        {'label': 'HD Episode', 'value': '3', 'type': ReleaseType.episode},
        {'label': 'HD Movie', 'value': '1', 'type': ReleaseType.movie},
        {'label': 'SD Season', 'value': '6', 'type': ReleaseType.season},
        {'label': 'SD Episode', 'value': '4', 'type': ReleaseType.episode},
        {'label': 'SD Movie', 'value': '2', 'type': ReleaseType.movie},
    )

    _category_value_type_map = {
        c['value']: c['type']
        for c in _categories
    }

    def autodetect_category(self, _):
        # "HD" or "SD"
        if (
            utils.video.height(self.content_path) >= 720
            or utils.video.width(self.content_path) >= 1280
        ):
            resolution = 'HD'
        else:
            resolution = 'SD'

        # "Movie", "Episode" or "Season"
        if self.release_name.type is ReleaseType.movie:
            typ = 'Movie'
        elif self.release_name.type is ReleaseType.season:
            typ = 'Season'
        elif self.release_name.type is ReleaseType.episode:
            typ = 'Episode'
        else:
            raise RuntimeError(f'Unsupported type: {self.release_name.type}')

        category = f'{resolution} {typ}'
        _log.debug('Autodetected category: %r', category)
        return category

    @property
    def chosen_release_type(self):
        """
        :class:`~.types.ReleaseType` enum derived from :attr:`category_job` or
        `None` if :attr:`category_job` is not finished yet
        """
        if self.category_job.is_finished:
            choice = self.get_job_attribute(self.category_job, 'choice')
            return self._category_value_type_map.get(choice)

    release_name_separator = '.'

    release_name_translation = {
        'group': {
            re.compile(r'^NOGROUP$'): r'NOGRP',
        },
    }

    @cached_property
    def title_job(self):
        """
        :class:`~.jobs.dialog.TextFieldJob` instance with text set to the
        release title

        Unlike :attr:`~.TrackerJobsBase.release_name_job`, this uses the
        original scene release name for movie and episode scene releases.
        """
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('title'),
            label='Title',
            prejobs=(self.category_job, self.scene_check_job, self.imdb_job),
            text=self.generate_title,
            condition=self.make_job_condition('title_job'),
            **self.common_job_args(),
        )

    async def generate_title(self):
        assert self.scene_check_job.is_finished
        assert self.imdb_job.is_finished

        if self.chosen_release_type in (ReleaseType.movie, ReleaseType.episode):
            if self.scene_check_job.is_scene_release:
                # Use the scene release name. We rely on scene_check_job making sure
                # that the file/directory name is the correct release name.
                search_results = await utils.predbs.MultiPredbApi().search(self.content_path)
                assert len(search_results) >= 1, search_results
                return search_results[0]

        # Non-scene release or season pack. We may generate a title.
        await self.release_name.fetch_info(webdb=self.imdb, webdb_id=self.imdb_id)
        return str(self.release_name)

    @cached_property
    def description_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('description'),
            label='Description',
            prejobs=(self.mediainfo_job, self.upload_screenshots_job),
            text=self.generate_description,
            condition=self.make_job_condition('description_job'),
            autofinish=True,
            read_only=True,
            hidden=True,
            # Don't cache job output because the number of screenshots can be
            # changed by the user between runs.
            **self.common_job_args(ignore_cache=True),
        )

    async def generate_description(self):
        assert self.mediainfo_job.is_finished
        assert self.upload_screenshots_job.is_finished

        mediainfo = (
            '[mediainfo]'
            + self.get_job_output(self.mediainfo_job, slice=0)
            + '[/mediainfo]'
        )

        screenshots = []
        for screenshot in self.upload_screenshots_job.uploaded_images:
            screenshots.append(f'[img]{screenshot}[/img]')

        screenshots_wrapped = (
            '[spoiler=Screenshots][center]'
            + '\n'.join(screenshots)
            + '[/center][/spoiler]'
        )

        promotion = (
            '[align=right][size=1]'
            f'Shared with [url={__homepage__}]{__project_name__}[/url]'
            '[/size][/align]'
        )

        return (
            mediainfo
            + '\n\n'
            + screenshots_wrapped
            + '\n\n'
            + promotion
        )

    @property
    def post_data_autofill(self):
        return {
            'submit': 'true',
            'MAX_FILE_SIZE': '2097152',
            'fillonly': 'auto fill',
            'category': '0',
            'Resolution': '0',
            'source': '12',
            'origin': '6',
            'title': '',
            'genre_tags': '---',
            'taglist': '',
            'autocomplete_toggle': 'on',
            'image': '',
            'fontfont': '-1',
            'fontsize': '-1',
            'desc': '',
            'fontfont': '-1',
            'fontsize': '-1',
            'groupDesc': '',
            'anonymous': '0',
        }

    @property
    def post_data_upload(self):
        return {
            'submit': 'true',
            'category': self.get_job_attribute(self.category_job, 'choice'),
            'Resolution': '0',
            'source': '12',
            'origin': '6',
            'title': self.get_job_output(self.title_job, slice=0),
            'genre_tags': '---',
            'autocomplete_toggle': 'on',
            'image': '',
            'fontfont': '-1',
            'fontsize': '-1',
            'desc': self.get_job_output(self.description_job, slice=0),
            'fontfont': '-1',
            'fontsize': '-1',
            'groupDesc': '',
            'anonymous': '1' if self.options['anonymous'] else '0',
            'ignoredupes': '1' if self.options['ignore_dupes'] else None,
            'imdbID': self.get_job_output(self.imdb_job, slice=0),
            # 'tmdbID': ...,
            # 'thetvdbID': ...,
            # 'tvmazeID': ...,
        }

    @property
    def torrent_filepath(self):
        return self.get_job_output(self.create_torrent_job, slice=0)
