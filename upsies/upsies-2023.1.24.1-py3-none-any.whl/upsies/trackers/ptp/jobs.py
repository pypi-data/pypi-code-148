"""
Concrete :class:`~.base.TrackerJobsBase` subclass for PTP
"""

from datetime import datetime

from ... import errors, jobs, utils
from ...utils import cached_property
from ...utils.release import ReleaseType
from ..base import TrackerJobsBase
from ._ptp_tags import PTP_TAGS

import logging  # isort:skip
_log = logging.getLogger(__name__)


class PtpTrackerJobs(TrackerJobsBase):

    @cached_property
    def jobs_before_upload(self):
        return (
            # Common background jobs
            self.create_torrent_job,
            self.mediainfo_job,
            self.screenshots_job,
            self.upload_screenshots_job,
            self.ptp_group_id_job,

            # Common interactive jobs
            self.type_job,
            self.imdb_job,
            self.title_job,

            # Jobs that only run if movie exists on PTP and we add a release

            # Jobs that only run if movie does not exists on PTP yet
            self.year_job,
            self.plot_job,
            self.tags_job,
            self.cover_art_job,
        )

    @cached_property
    def type_job(self):
        return jobs.dialog.ChoiceJob(
            name=self.get_job_name('type'),
            label='Type',
            condition=self.make_job_condition('type_job'),
            autodetect=self.autodetect_type,
            choices=(
                ('Feature Film', 'Feature Film'),
                ('Short Film', 'Short Film'),
                ('Miniseries', 'Miniseries'),
                ('Stand-up Comedy', 'Stand-up Comedy'),
                ('Live Performance', 'Live Performance'),
                ('Movie Collection', 'Movie Collection'),
            ),
            **self.common_job_args(),
        )

    def autodetect_type(self, _):
        if self.release_name.type == ReleaseType.season:
            return 'Miniseries'

        first_video = utils.video.first_video(self.content_path)

        # Short film if runtime 45 min or less (Rule 1.1.1)
        if utils.video.duration(first_video) <= 45 * 60:
            return 'Short Film'

    @cached_property
    def imdb_job(self):
        imdb_job = super().imdb_job
        imdb_job.signal.register('output', self._start_getting_ptp_group_id)
        return imdb_job

    @property
    def imdb_id(self):
        if self.imdb_job.is_finished:
            return self.imdb_job.output[0]

    def _start_getting_ptp_group_id(self, _):
        _log.debug('Starting %r', self.ptp_group_id_job)
        self.ptp_group_id_job.start()

    @cached_property
    def ptp_group_id_job(self):
        return jobs.custom.CustomJob(
            name=self.get_job_name('ptp-group-id'),
            label='PTP Group ID',
            condition=self.make_job_condition('ptp_group_id_job'),
            prejobs=(self.imdb_job,),
            worker=self.fetch_ptp_group_id,
            catch=(errors.RequestError,),
            **self.common_job_args(),
        )

    async def fetch_ptp_group_id(self, _):
        assert self.imdb_job.is_finished
        group_id = await self.tracker.get_ptp_group_id_by_imdb_id(self.imdb_id)
        _log.debug('Group ID: %r', group_id)
        return '' if group_id is None else group_id

    @property
    def ptp_group_id(self):
        """
        PTP group ID if :attr:`ptp_group_id_job` is finished and group ID was found,
        `None` otherwise
        """
        if self.ptp_group_id_job.is_finished:
            if self.ptp_group_id_job.output:
                return self.ptp_group_id_job.output[0]

    @cached_property
    def title_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('title'),
            label='Title',
            condition=self.make_job_condition('title_job'),
            prejobs=(self.imdb_job,),
            text=self.fetch_title,
            normalizer=self.normalize_title,
            validator=self.validate_title,
            **self.common_job_args(),
        )

    async def fetch_title(self):
        assert self.imdb_job.is_finished
        _log.debug('!!!!!! Filling in new title')
        info = await self.tracker.get_ptp_metadata(self.imdb_id)
        _log.debug('PTP metadata: %r', info)
        return info['title']

    def normalize_title(self, text):
        return text.strip()

    def validate_title(self, text):
        if not text:
            raise ValueError('Title must not be empty')

    @cached_property
    def year_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('year'),
            label='Year',
            condition=self.make_job_condition('year_job'),
            prejobs=(self.imdb_job,),
            text=self.fetch_year,
            normalizer=self.normalize_year,
            validator=self.validate_year,
            **self.common_job_args(),
        )

    async def fetch_year(self):
        assert self.imdb_job.is_finished
        _log.debug('!!!!!! Filling in new year')
        info = await self.tracker.get_ptp_metadata(self.imdb_id)
        _log.debug('PTP metadata: %r', info)
        return info['year']

    def normalize_year(self, text):
        return text.strip()

    def validate_year(self, text):
        try:
            year = int(text)
        except ValueError:
            raise ValueError('Year is not a number')
        else:
            if not 1800 < year < datetime.now().year + 10:
                raise ValueError('Year is not reasonable')

    @cached_property
    def tags_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('tags'),
            label='Tags',
            condition=self.make_job_condition('tags_job'),
            prejobs=(self.imdb_job,),
            text=self.fetch_tags,
            normalizer=self.normalize_tags,
            validator=self.validate_tags,
            **self.common_job_args(),
        )

    async def fetch_tags(self):
        assert self.imdb_job.is_finished
        _log.debug('!!!!!! Filling in new tags')
        info = await self.tracker.get_ptp_metadata(self.imdb_id)
        _log.debug('PTP metadata: %r', info)
        return info['tags']

    def normalize_tags(self, text):
        tags = [tag.strip() for tag in text.split(',')]
        deduped = list(dict.fromkeys(tags))
        return ', '.join(tag for tag in deduped if tag)

    def validate_tags(self, text):
        for tag in text.split(','):
            if tag.strip() not in PTP_TAGS:
                raise ValueError(f'Tag is not valid: {tag}')

    @cached_property
    def cover_art_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('cover_art'),
            label='Cover Art',
            condition=self.make_job_condition('cover_art_job'),
            prejobs=(self.imdb_job,),
            text=self.fetch_cover_art,
            autofinish=True,
            **self.common_job_args(),
        )

    async def fetch_cover_art(self):
        assert self.imdb_job.is_finished
        _log.debug('!!!!!! Filling in new cover_art')
        info = await self.tracker.get_ptp_metadata(self.imdb_id)
        _log.debug('PTP metadata: %r', info)
        return info['art']

    @cached_property
    def plot_job(self):
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('plot'),
            label='Plot',
            condition=self.make_job_condition('plot_job'),
            prejobs=(self.imdb_job,),
            text=self.fetch_plot,
            normalizer=self.normalize_plot,
            validator=self.validate_plot,
            autofinish=True,
            **self.common_job_args(),
        )

    async def fetch_plot(self):
        assert self.imdb_job.is_finished
        return await self.tracker.get_ptp_metadata(self.imdb_id, key='plot')

    def normalize_plot(self, text):
        return text.strip()

    def validate_plot(self, text):
        if not text:
            raise ValueError('Plot must not be empty')

    @property
    def post_data(self):
        post_data = self._post_data_common

        _log.debug('PTP group ID: %r', self.ptp_group_id)
        if self.ptp_group_id:
            _log.debug('Adding format to existing group')
            post_data.update(self._post_data_add_format)
        else:
            _log.debug('Creating new group')
            post_data.update(self._post_data_add_movie)

        return post_data

    @property
    def _post_data_common(self):
        return {
            'type': self.get_job_attribute(self.type_job, 'choice'),
            # 'remaster_year': releaseInfo.RemasterYear,
            # 'remaster_title': releaseInfo.RemasterTitle,
            # 'codec': 'Other',  # Sending the codec as custom.
            # 'other_codec': releaseInfo.Codec,
            # 'container': 'Other',  # Sending the container as custom.
            # 'other_container': releaseInfo.Container,
            # 'resolution': releaseInfo.ResolutionType,
            # 'other_resolution': releaseInfo.Resolution,
            # 'source': 'Other',  # Sending the source as custom.
            # 'other_source': releaseInfo.Source,
            # 'release_desc': releaseDescription,
            # 'nfo_text': releaseInfo.Nfo,
            # 'subtitles[]': releaseInfo.Subtitles,
            # 'trumpable[]': releaseInfo.Trumpable,
        }

    # if releaseInfo.Source == "Other":
    #     paramList["other_source"]: releaseInfo.SourceOther

    # # personal rip only needed if it is specified
    # if releaseInfo.PersonalRip:
    #     paramList.update({"internalrip": "on"})

    # # scene only needed if it is specified
    # if releaseInfo.SceneRelease:
    #     paramList.update({"scene": "on"})
    # # other category is only needed if it is specified
    # if releaseInfo.SpecialRelease:
    #     paramList.update({"special": "on"})
    # # remaster is only needed if it is specified
    # if len(releaseInfo.RemasterYear) > 0 or len(releaseInfo.RemasterTitle) > 0:
    #     paramList.update({"remaster": "on"})
    #     }

    @property
    def _post_data_add_format(self):
        return {
            'groupid': self.ptp_group_id,
        }

    @property
    def _post_data_add_movie(self):
        post_data = {
            'imdb': self.tracker.normalize_imdb_id(self.imdb_id),
            'title': self.get_job_output(self.title_job, slice=0),
            'year': self.get_job_output(self.year_job, slice=0),
            'album_desc': self.get_job_output(self.plot_job, slice=0),
            'tags': self.get_job_output(self.tags_job, slice=0),
            # 'trailer': releaseInfo.YouTubeId,
            'image': self.get_job_output(self.cover_art_job, slice=0),
        }

        # TODO: Send artists
        # # ???: For some reason PtpUploader uses "artist" and "importance" in the
        # #      POST data while the website form uses "artists", "importances"
        # #      and "roles".
        # artists = self.get_job_output(self.artists_job):
        # if artists:
        #     post_data['artist'] = []
        #     post_data['importance'] = []
        #     for name in artists:
        #         # `importance` is the artist type:
        #         # 1: Director
        #         # 2: Writer
        #         # 3: Producer
        #         # 4: Composer
        #         # 5: Actor
        #         # 6: Cinematographer
        #         post_data['importance'].append('1')
        #         post_data['artist'].append(name)
        #         post_data['role'].append(name)

        return post_data

    @property
    def torrent_filepath(self):
        return self.get_job_output(self.create_torrent_job, slice=0)
