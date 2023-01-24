"""
Abstract base class for tracker APIs
"""

import abc
import builtins

import aiobtclientapi

from .. import errors, jobs, utils
from ..utils import cached_property, release

import logging  # isort:skip
_log = logging.getLogger(__name__)


class TrackerConfigBase(dict):
    """
    Dictionary with default values that are defined by the subclass

    Some keys defined by this base class always exist.
    """

    _defaults = {
        'source': utils.configfiles.config_value(
            value='',
            description='Value of the "source" field in generated torrents.',
        ),
        'exclude': utils.configfiles.config_value(
            value=[],
            description='List of regular expressions. Matching files are excluded from generated torrents.',
        ),
        'add_to': utils.configfiles.config_value(
            value=utils.types.Choice(
                value='',
                empty_ok=True,
                options=aiobtclientapi.client_names(),
            ),
            description=('BitTorrent client to add torrent to after submission.'),
        ),
        'copy_to': utils.configfiles.config_value(
            value='',
            description='Directory path to copy torrent to after submission.',
        ),
    }

    defaults = {}
    """Default values"""

    argument_definitions = {}
    """CLI argument definitions (see :attr:`.CommandBase.argument_definitions`)"""

    def __new__(cls, config={}):
        # Merge generic and tracker-specific defaults
        combined_defaults = cls._merge(cls._defaults, cls.defaults)

        # Check user-given config for unknown options
        for k in config:
            if k not in combined_defaults:
                raise TypeError(f'Unknown option: {k!r}')

        # Merge user-given config with defaults
        obj = super().__new__(cls)
        obj.update(cls._merge(combined_defaults, config))
        return obj

    @staticmethod
    def _merge(a, b):
        # Copy a
        combined = {}
        combined.update(a)

        # Update a with values from b
        for k, v in b.items():
            if k in combined:
                # Ensure same value type from a
                cls = type(combined[k])
                combined[k] = cls(v)
            else:
                # Append new value
                combined[k] = v

        return combined

    # If the config is passed as config={...}, super().__init__() will interpret
    # as a key-value pair that ends up in the config.
    def __init__(cls, *args, **kwargs):
        pass


class TrackerJobsBase(abc.ABC):
    """
    Base class for tracker-specific :class:`jobs <upsies.jobs.base.JobBase>`

    This base class defines general-purpose jobs that can be used by subclasses
    by returning them in their :attr:`jobs_before_upload` or
    :attr:`jobs_after_upload` attributes. It also provides all objects that are
    needed by any one of those jobs.

    Job instances are provided as :func:`functools.cached_property`, i.e. jobs
    are created only once per session.

    Subclasses that need to run background tasks should pass them to
    :meth:`.JobBase.attach_task` or to :meth:`.TrackerBase.attach_task`.

    For a description of the arguments see the corresponding properties.
    """

    def __init__(self, *, content_path, tracker,
                 reuse_torrent_path=None, torrent_destination=None, check_after_add=False,
                 exclude_files=(), options=None, image_host=None,
                 bittorrent_client=None, common_job_args=None):
        self._content_path = content_path
        self._reuse_torrent_path = reuse_torrent_path
        self._tracker = tracker
        self._image_host = image_host
        self._bittorrent_client = bittorrent_client
        self._torrent_destination = torrent_destination
        self._check_after_add = check_after_add
        self._exclude_files = exclude_files
        self._common_job_args = common_job_args or {}
        self._options = options or {}
        self._signal = utils.signal.Signal('warning', 'error', 'exception')

    @property
    def content_path(self):
        """
        Content path to generate metadata for

        This is the same object that was passed as a initialization argument.
        """
        return self._content_path

    @property
    def tracker(self):
        """
        :class:`~.trackers.base.TrackerBase` subclass

        This is the same object that was passed as a initialization argument.
        """
        return self._tracker

    @property
    def reuse_torrent_path(self):
        """
        Path to an existing torrent file that matches :attr:`content_path`

        See :func:`.torrent.create`.
        """
        return self._reuse_torrent_path

    @property
    def torrent_destination(self):
        """
        Where to copy the generated torrent file to or `None`

        This is the same object that was passed as a initialization argument.
        """
        return self._torrent_destination

    @property
    def check_after_add(self):
        """Whether to hash existing files after adding the torrent to a client"""
        return self._check_after_add

    @property
    def exclude_files(self):
        """
        Sequence of glob and regular expression patterns to exclude from the
        generated torrent

        See the ``exclude_files`` argument of
        :meth:`.CreateTorrentJob.initialize`.
        """
        return self._exclude_files

    @property
    def options(self):
        """
        Configuration options provided by the user

        This is the same object that was passed as a initialization argument.
        """
        return self._options

    @property
    def image_host(self):
        """
        :class:`~.base.ImageHostBase` instance or `None`

        This is the same object that was passed as a initialization argument.
        """
        return self._image_host

    @property
    def bittorrent_client(self):
        """
        :class:`~.base.ClientApiBase` instance or `None`

        This is the same object that was passed as a initialization argument.
        """
        return self._bittorrent_client

    def common_job_args(self, **overload):
        """
        Keyword arguments that are passed to all jobs or empty `dict`

        :param overload: Keyword arguments add or replace values from the
            initialization argument
        """
        return {
            **self._common_job_args,
            **overload,
        }

    @property
    @abc.abstractmethod
    def jobs_before_upload(self):
        """
        Sequence of jobs that need to finish before :meth:`~.TrackerBase.upload` can
        be called
        """

    @cached_property
    def jobs_after_upload(self):
        """
        Sequence of jobs that are started after :meth:`~.TrackerBase.upload`
        finished

        .. note:: Jobs returned by this class should have
                  :attr:`~.JobBase.autostart` set to `False` or they will be
                  started before submission is attempted.

        By default, this returns :attr:`add_torrent_job` and
        :attr:`copy_torrent_job`.
        """
        return (
            self.add_torrent_job,
            self.copy_torrent_job,
        )

    @property
    def isolated_jobs(self):
        """
        Sequence of job names (e.g. ``"imdb_job"``) that were singled out by the
        user (e.g. with a CLI argument) to create only a subset of the usual
        metadata

        If this sequence is empty, all jobs in :attr:`jobs_before_upload` and
        :attr:`jobs_after_upload` are enabled.
        """
        return ()

    @property
    def submission_ok(self):
        """
        Whether the created metadata should be submitted

        The base class implementation returns `False` if there are any
        :attr:`isolated_jobs`. Otherwise, it returns `True` only if all
        :attr:`jobs_before_upload` have an :attr:`~.base.JobBase.exit_code` of
        ``0`` or a falsy :attr:`~.base.JobBase.is_enabled` value.

        Subclasses should always call the parent class implementation to ensure
        all metadata was created successfully.
        """
        if self.isolated_jobs:
            # If some jobs are disabled, required metadata is missing and we
            # can't submit
            return False
        else:
            enabled_jobs_before_upload = tuple(
                job for job in self.jobs_before_upload
                if job and job.is_enabled
            )
            enabled_jobs_succeeded = all(
                job.exit_code == 0
                for job in enabled_jobs_before_upload
            )
            return bool(
                enabled_jobs_before_upload
                and enabled_jobs_succeeded
            )

    @property
    def signal(self):
        """
        :class:`~.signal.Signal` instance with the signals ``warning``, ``error``
        and ``exception``
        """
        return self._signal

    def warn(self, warning):
        """
        Emit ``warning`` signal (see :attr:`signal`)

        Emit a warning for any non-critical issue that the user can choose to
        ignore or fix.
        """
        self.signal.emit('warning', warning)

    def error(self, error):
        """
        Emit ``error`` signal (see :attr:`signal`)

        Emit an error for any critical but expected issue that can't be
        recovered from (e.g. I/O error).
        """
        self.signal.emit('error', error)

    def exception(self, exception):
        """
        Emit ``exception`` signal (see :attr:`signal`)

        Emit an exception for any critical and unexpected issue that should be
        reported as a bug.
        """
        self.signal.emit('exception', exception)

    @cached_property
    def imdb(self):
        """:class:`~.webdbs.imdb.ImdbApi` instance"""
        return utils.webdbs.webdb('imdb')

    @cached_property
    def tmdb(self):
        """:class:`~.webdbs.tmdb.TmdbApi` instance"""
        return utils.webdbs.webdb('tmdb')

    @cached_property
    def tvmaze(self):
        """:class:`~.webdbs.tvmaze.TvmazeApi` instance"""
        return utils.webdbs.webdb('tvmaze')

    def get_job_name(self, name):
        """
        Return job name that is unique for this tracker

        It's important for tracker jobs to have unique names to avoid re-using
        cached output from another tracker's job with the same name.

        Standard jobs have names so that cached output will be re-used by other
        trackers if possible. This function is mainly for unique and custom jobs
        that are only used for one tracker but might share the same name with
        other trackers.
        """
        prefix = f'{self.tracker.name}-'
        if name.startswith(prefix):
            return name
        else:
            return f'{prefix}{name}'

    @cached_property
    def create_torrent_job(self):
        """:class:`~.jobs.torrent.CreateTorrentJob` instance"""
        return jobs.torrent.CreateTorrentJob(
            content_path=self.content_path,
            reuse_torrent_path=self.reuse_torrent_path,
            tracker=self.tracker,
            exclude_files=self._exclude_files,
            condition=self.make_job_condition('create_torrent_job'),
            **self.common_job_args(),
        )

    torrent_piece_size_min = 2**20  # 1 MiB
    """Minimum torrent piece size for this tracker"""

    torrent_piece_size_max = 16 * 2**20  # 16 MiB
    """Maximum torrent piece size for this tracker"""

    @cached_property
    def add_torrent_job(self):
        """:class:`~.jobs.torrent.AddTorrentJob` instance"""
        if self.bittorrent_client and self.create_torrent_job:
            add_torrent_job = jobs.torrent.AddTorrentJob(
                autostart=False,
                client_api=self.bittorrent_client,
                download_path=utils.fs.dirname(self.content_path),
                check_after_add=self._check_after_add,
                condition=self.make_job_condition('add_torrent_job'),
                **self.common_job_args(),
            )
            # Pass CreateTorrentJob output to AddTorrentJob input.
            self.create_torrent_job.signal.register('output', add_torrent_job.enqueue)
            # Tell AddTorrentJob to finish the current upload and then finish.
            self.create_torrent_job.signal.register('finished', self.finalize_add_torrent_job)
            return add_torrent_job

    def finalize_add_torrent_job(self, _):
        self.add_torrent_job.finalize()

    @cached_property
    def copy_torrent_job(self):
        """:class:`~.jobs.torrent.CopyTorrentJob` instance"""
        if self.torrent_destination and self.create_torrent_job:
            copy_torrent_job = jobs.torrent.CopyTorrentJob(
                autostart=False,
                destination=self.torrent_destination,
                condition=self.make_job_condition('copy_torrent_job'),
                **self.common_job_args(),
            )
            # Pass CreateTorrentJob output to CopyTorrentJob input.
            self.create_torrent_job.signal.register('output', copy_torrent_job.enqueue)
            # Tell CopyTorrentJob to finish when CreateTorrentJob is done.
            self.create_torrent_job.signal.register('finished', self.finalize_copy_torrent_job)
            return copy_torrent_job

    def finalize_copy_torrent_job(self, _):
        self.copy_torrent_job.finalize()

    @cached_property
    def release_name(self):
        """
        :class:`~.release.ReleaseName` instance with
        :attr:`release_name_translation` applied
        """
        return release.ReleaseName(
            path=self.content_path,
            translate=self.release_name_translation,
            separator=self.release_name_separator,
        )

    release_name_separator = None
    """See :attr:`.ReleaseName.separator`"""

    release_name_translation = {}
    """See ``translate`` argument of :attr:`~.utils.release.ReleaseName`"""

    @cached_property
    def release_name_job(self):
        """
        :class:`~.jobs.dialog.TextFieldJob` instance with text set to
        :attr:`release_name`

        The text is automatically updated when :attr:`imdb_job` sends an ID.
        """
        return jobs.dialog.TextFieldJob(
            name=self.get_job_name('release-name'),
            label='Release Name',
            text=str(self.release_name),
            callbacks={
                'output': self.release_name.set_release_info,
            },
            condition=self.make_job_condition('release_name_job'),
            **self.common_job_args(),
        )

    async def update_release_name_from(self, webdb, webdb_id):
        """
        Update :attr:`release_name_job` with web DB information

        :param webdb: :class:`~.webdbs.base.WebDbApiBase` instance
        :param webdb_id: ID for `webdb`

        This is a convenience wrapper around :meth:`.ReleaseName.fetch_info` and
        :meth:`.TextFieldJob.fetch_text`.
        """
        await self.release_name_job.fetch_text(
            coro=self.release_name.fetch_info(webdb=webdb, webdb_id=webdb_id),
            nonfatal_exceptions=(errors.RequestError,),
        )
        _log.debug('Updated release name: %s', self.release_name)

    @cached_property
    def imdb_job(self):
        """:class:`~.jobs.webdb.WebDbSearchJob` instance"""
        return jobs.webdb.WebDbSearchJob(
            query=self.content_path,
            db=self.imdb,
            callbacks={
                'output': self._handle_imdb_id,
            },
            condition=self.make_job_condition('imdb_job'),
            **self.common_job_args(),
        )

    def _handle_imdb_id(self, imdb_id):
        # Update other webdb queries with IMDb info
        self.tracker.attach_task(self._propagate_webdb_info(self.imdb, imdb_id))

        # Upload poster image from appropriate webdb
        if self._poster_webdb is self.imdb:
            self._start_poster_job(self.imdb, imdb_id)

    @property
    def imdb_id(self):
        """IMDb ID if :attr:`imdb_job` is finished or `None`"""
        return self._get_webdb_id_from_job(self.imdb_job)

    @cached_property
    def tmdb_job(self):
        """:class:`~.jobs.webdb.WebDbSearchJob` instance"""
        return jobs.webdb.WebDbSearchJob(
            query=self.content_path,
            db=self.tmdb,
            callbacks={
                'output': self._handle_tmdb_id,
            },
            condition=self.make_job_condition('tmdb_job'),
            **self.common_job_args(),
        )

    def _handle_tmdb_id(self, tmdb_id):
        # Update other webdb queries with TMDb info
        self.tracker.attach_task(self._propagate_webdb_info(self.tmdb, tmdb_id))

        if self._poster_webdb is self.tmdb:
            self._start_poster_job(self.tmdb, tmdb_id)

    @property
    def tmdb_id(self):
        """TMDb ID if :attr:`tmdb_job` is finished or `None`"""
        return self._get_webdb_id_from_job(self.tmdb_job)

    @cached_property
    def tvmaze_job(self):
        """:class:`~.jobs.webdb.WebDbSearchJob` instance"""
        return jobs.webdb.WebDbSearchJob(
            query=self.content_path,
            db=self.tvmaze,
            callbacks={
                'output': self._handle_tvmaze_id,
            },
            condition=self.make_job_condition('tvmaze_job'),
            **self.common_job_args(),
        )

    def _handle_tvmaze_id(self, tvmaze_id):
        # Update other webdb queries with TVmaze info
        self.tracker.attach_task(self._propagate_webdb_info(self.tvmaze, tvmaze_id))

        if self._poster_webdb is self.tvmaze:
            self._start_poster_job(self.tvmaze, tvmaze_id)

    @property
    def tvmaze_id(self):
        """TVmaze ID if :attr:`tvmaze_job` is finished or `None`"""
        return self._get_webdb_id_from_job(self.tvmaze_job)

    def _get_webdb_id_from_job(self, webdb_job):
        if webdb_job.is_finished and webdb_job.output:
            return webdb_job.output[0]

    async def _propagate_webdb_info(self, webdb, webdb_id):
        target_webdb_jobs = [
            j for j in (getattr(self, f'{name}_job') for name in utils.webdbs.webdb_names())
            if (
                webdb.name not in j.name
                and j.is_enabled
                and not j.is_finished
            )
        ]

        title_english = await webdb.title_english(webdb_id)
        title_original = await webdb.title_original(webdb_id)
        query = utils.webdbs.Query(
            type=await webdb.type(webdb_id),
            title=title_english or title_original,
            year=await webdb.year(webdb_id),
        )

        _log.debug('Propagating %s info to: %r: %s', webdb.name, [j.name for j in target_webdb_jobs], query)
        for job in target_webdb_jobs:
            job.query.update(query)

        await self.update_release_name_from(webdb, webdb_id)

    @cached_property
    def screenshots_job(self):
        """
        :class:`~.jobs.screenshots.ScreenshotsJob` instance

        The number of screenshots to make is taken from the ``screenshots``
        value in :attr:`options`.
        """
        return jobs.screenshots.ScreenshotsJob(
            content_path=self.content_path,
            count=self.options.get('screenshots'),
            condition=self.make_job_condition('screenshots_job'),
            **self.common_job_args(),
        )

    image_host_config = {}
    """
    Dictionary that maps an image hosting service :attr:`~.ImageHostBase.name`
    to :attr:`~.ImageHostBase.default_config` values

    ``common`` is a special image host whose values are always applied.

    Example:

    >>> image_host_config = {
    ...     # Always generate 300p thumbnails
    ...     'common': {'thumb_width': 300},
    ...     # If "myhost" is used, use this API key, but only for this tracker
    ...     'myhost': {'apikey': 'd34db33f'},
    ... }
    """

    @cached_property
    def upload_screenshots_job(self):
        """:class:`~.jobs.imghost.ImageHostJob` instance"""
        if self.image_host and self.screenshots_job:
            imghost_job = jobs.imghost.ImageHostJob(
                imghost=self.image_host,
                condition=self.make_job_condition('upload_screenshots_job'),
                **self.common_job_args(),
            )
            # Timestamps are calculated in a subprocess, we have to wait for
            # that until we can set the number of expected screenhots.
            self.screenshots_job.signal.register(
                'timestamps',
                lambda timestamps: imghost_job.set_images_total(len(timestamps)),
            )
            # Pass ScreenshotsJob's output to ImageHostJob input.
            self.screenshots_job.signal.register('output', imghost_job.enqueue)
            # Tell imghost_job to finish the current upload and then finish.
            self.screenshots_job.signal.register('finished', self.finalize_upload_screenshots_job)
            return imghost_job

    def finalize_upload_screenshots_job(self, _):
        self.upload_screenshots_job.finalize()

    @cached_property
    def poster_job(self):
        """
        :class:`~.jobs.poster.PosterJob` instance

        This is started automatically when an appropriate webdb job finishes.
        """
        return jobs.poster.PosterJob(
            autostart=False,
            webdb_id=None,
            webdb=None,
            imghost=self.image_host,
            width=self.poster_max_width,
            height=self.poster_max_height,
            condition=self.make_job_condition('poster_job'),
            **self.common_job_args(),
        )

    def _start_poster_job(self, webdb, webdb_id):
        self.poster_job.start(
            webdb=webdb,
            webdb_id=webdb_id,
            season=self.release_name.only_season,
        )

    poster_max_width = 300
    """Maximum poster image width"""

    poster_max_height = 500
    """Maximum poster image height"""

    @cached_property
    def _poster_webdb(self):
        """:class:`~.webdbs.base.WebDbApiBase` instance for finding poster image"""
        if (
                self.poster_job.is_enabled
                and not self.poster_job.is_started
                and self.poster_job in self.jobs_before_upload
        ):
            if (
                    self.tvmaze_job.is_enabled
                    and self.tvmaze_job in self.jobs_before_upload
                    and self.release_name.type in (release.ReleaseType.season,
                                                   release.ReleaseType.episode)
            ):
                return self.tvmaze

            elif (
                    self.imdb_job.is_enabled
                    and self.imdb_job in self.jobs_before_upload
            ):
                return self.imdb

            elif (
                    self.tmdb_job.is_enabled
                    and self.tmdb_job in self.jobs_before_upload
            ):
                return self.tmdb

            else:
                raise RuntimeError('You must add a WebDbSearchJob instance to jobs_before_upload')

    @cached_property
    def mediainfo_job(self):
        """:class:`~.jobs.mediainfo.MediainfoJob` instance"""
        return jobs.mediainfo.MediainfoJob(
            content_path=self.content_path,
            condition=self.make_job_condition('mediainfo_job'),
            **self.common_job_args(),
        )

    @cached_property
    def scene_check_job(self):
        """:class:`~.jobs.scene.SceneCheckJob` instance"""
        common_job_args = self.common_job_args(ignore_cache=True)
        common_job_args['force'] = self.options.get('is_scene')
        return jobs.scene.SceneCheckJob(
            content_path=self.content_path,
            condition=self.make_job_condition('scene_check_job'),
            **common_job_args,
        )

    def make_job_condition(self, job_attr):
        """
        Return :attr:`~.base.JobBase.condition` function for job

        :param str job_attr: Name of the job attribute this condition is for

            By convention, this should be ``"<name>_job"``.

        The returned function takes into account :attr:`jobs_before_upload`,
        :attr:`jobs_after_upload` and :attr:`isolated_job`.
        """
        def condition():
            job = getattr(self, job_attr)
            if not (
                    job in self.jobs_before_upload
                    or job in self.jobs_after_upload
            ):
                # Subclass doesn't use this job
                return False

            isolated_jobs = self.isolated_jobs
            if isolated_jobs and job in isolated_jobs:
                # Jobs was isolated by user (i.e. other jobs are disabled)
                return True

            if not isolated_jobs:
                # No isolated jobs means all jobs in jobs_before/after_upload are enabled
                return True

            return False

        # Rename condition function to make debugging more readable
        condition.__qualname__ = f'{job_attr}_condition'
        return condition

    _NO_DEFAULT = object()

    def get_job_output(self, job, slice=None, default=_NO_DEFAULT):
        """
        Helper method for getting output from job

        `job` must be finished.

        :param job: :class:`~.jobs.base.JobBase` instance
        :param slice: :class:`int` to get a specific item from `job`'s output,
            `None` to return all output as a list, or a :class:`slice` object to
            return only one or more items of the output
        :param default: Default value if `job` is not finished or getting
            `slice` from `job`'s output fails.

        :raise RuntimeError: if `job` is not finished or getting `slice` from
            :attr:`~.base.JobBase.output` raises an :class:`IndexError`
        :return: :class:`list` or :class:`str`
        """
        if not job.is_finished:
            if default is not self._NO_DEFAULT:
                return default
            else:
                raise RuntimeError(f'Unfinished job: {job.name}')
        else:
            if slice is None:
                slice = builtins.slice(None, None)
            try:
                return job.output[slice]
            except IndexError:
                raise RuntimeError(f'Job finished with insufficient output: {job.name}: {job.output}')

    def get_job_attribute(self, job, attribute, default=_NO_DEFAULT):
        """
        Helper method for getting an attribute from job

        :param job: :class:`~.jobs.base.JobBase` instance
        :param str attribute: Name of attribute to get from `job`
        :param default: Default value if `job` is not finished

        :raise RuntimeError: if `job` is not finished
        :raise AttributeError: if `attribute` is not an attribute of `job`
        """
        if not job.is_finished:
            if default is not self._NO_DEFAULT:
                return default
            else:
                raise RuntimeError(f'Unfinished job: {job.name}')
        else:
            return getattr(job, attribute)


class TrackerBase(abc.ABC):
    """
    Base class for tracker-specific operations, e.g. uploading

    :param options: User configuration options for this tracker,
        e.g. authentication details, announce URL, etc
    :type options: :class:`dict`-like
    """

    @property
    @abc.abstractmethod
    def TrackerJobs(self):
        """Subclass of :class:`TrackerJobsBase`"""

    @property
    @abc.abstractmethod
    def TrackerConfig(self):
        """Subclass of :class:`TrackerConfigBase`"""

    def __init__(self, options=None):
        self._options = options or {}
        self._signal = utils.signal.Signal('warning', 'error', 'exception')

    @property
    @abc.abstractmethod
    def name(self):
        """Lower-case tracker name abbreviation for internal use"""

    @property
    @abc.abstractmethod
    def label(self):
        """User-facing tracker name abbreviation"""

    setup_howto_template = 'Nobody has written a setup howto yet.'
    """
    Step-by-step guide that explains how to make your first upload

    .. note:: This MUST be a class attribute and not a property.
    """

    @classmethod
    def generate_setup_howto(cls):
        # `howto` is now in the local namespace (see `locals()`) and
        # `evalute_fstring()` can access its properties to replace, for example,
        # "{howto.current}" in `setup_howto_template` with the current section
        # number.
        howto = _Howto(tracker_cls=cls)  # noqa: F841 local variable 'howto' is assigned to but never used
        return utils.string.evaluate_fstring(cls.setup_howto_template)

    @property
    def options(self):
        """
        Configuration options provided by the user

        This is the :class:`dict`-like object from the initialization argument
        of the same name.
        """
        return self._options

    @cached_property
    def _tasks(self):
        return []

    def attach_task(self, coro, callback=None):
        """
        Run awaitable `coro` in background task

        :param coro: Any awaitable

        :param callback: Callable that is called with the return value or
            exception from `coro`
        """
        task = utils.run_task(coro, callback=callback)
        self._tasks.append(task)
        return task

    async def await_tasks(self):
        """Wait for all awaitables passed to :meth:`attach_task`"""
        for task in self._tasks:
            await task

    @abc.abstractmethod
    async def login(self):
        """Start user session"""

    @abc.abstractmethod
    async def logout(self):
        """End user session"""

    @property
    @abc.abstractmethod
    def is_logged_in(self):
        """Whether a user session is active"""

    @abc.abstractmethod
    async def get_announce_url(self):
        """Get announce URL from tracker website"""

    @abc.abstractmethod
    async def upload(self, tracker_jobs):
        """
        Upload torrent and other metadata from jobs

        :param TrackerJobsBase tracker_jobs: :attr:`TrackerJobs` instance
        """

    @property
    def signal(self):
        """
        :class:`~.signal.Signal` instance with the signals ``warning``, ``error``
        and ``exception``
        """
        return self._signal

    def warn(self, warning):
        """
        Emit ``warning`` signal (see :attr:`signal`)

        Emit a warning for any non-critical issue that the user can choose to
        ignore or fix.
        """
        self.signal.emit('warning', warning)

    def error(self, error):
        """
        Emit ``error`` signal (see :attr:`signal`)

        Emit an error for any critical but expected issue that can't be
        recovered from (e.g. I/O error).
        """
        self.signal.emit('error', error)

    def exception(self, exception):
        """
        Emit ``exception`` signal (see :attr:`signal`)

        Emit an exception for any critical and unexpected issue that should be
        reported as a bug.
        """
        self.signal.emit('exception', exception)


class _Howto:
    def __init__(self, tracker_cls):
        self._tracker_cls = tracker_cls
        self._section = 0

    def _autobump(self, sections):
        self._section += len(sections)
        return '\n'.join(sections).strip()

    @property
    def current_section(self):
        return self._section

    @property
    def bump_section(self):
        self._section += 1
        return ''

    @property
    def introduction(self):
        return self._autobump((
            (
                f'{self._section}. How To Read This Howto\n'
                '\n'
                f'   {self._section}.1 Words in ALL_CAPS_AND_WITH_UNDERSCORES are placeholders.\n'
                f'   {self._section}.2 Everything after "$" is a terminal command.\n'
            ),
        ))

    @property
    def screenshots(self):
        return self._autobump((
            (
                f'{self._section}. Screenshots (Optional)\n'
                '\n'
                f'   {self._section}.1 Specify how many screenshots to make.\n'
                f'       $ upsies set trackers.{self._tracker_cls.name}.screenshots NUMBER_OF_SCREENSHOTS\n'
            ),
            (
                f'   {self._section}.2 Specify where to host images.\n'
                f'       $ upsies set trackers.{self._tracker_cls.name}.image_host IMAGE_HOST\n'
                f'       Supported services: ' + ', '.join(utils.imghosts.imghost_names()) + '\n'
                '\n'
                f'   {self._section}.3 Configure image hosting service.\n'
                f'       $ upsies upload-images IMAGE_HOST --help\n'
            ),
        ))

    @property
    def autoseed(self):
        return self._autobump((
            (
                f'{self._section}. Add Uploaded Torrents To Client (Optional)\n'
                '\n'
                f'   {self._section}.1 Specify which client to add uploaded torrents to.\n'
                f'       $ upsies set trackers.{self._tracker_cls.name}.add_to CLIENT_NAME\n'
                f'       Supported clients: ' + ', '.join(aiobtclientapi.client_names()) + '\n'
            ),
            (
                f'   {self._section}.2 Specify your client connection.\n'
                '       $ upsies set clients.CLIENT_NAME.url URL\n'
                '       $ upsies set clients.CLIENT_NAME.username USERNAME\n'
                '       $ upsies set clients.CLIENT_NAME.password PASSWORD\n'
                '\n'
                f'{self._section + 1}. Copy Uploaded Torrents To Directory (Optional)\n'
                '\n'
                f'   $ upsies set trackers.{self._tracker_cls.name}.copy_to /path/to/directory\n'
            ),
        ))

    @property
    def upload(self):
        return self._autobump((
            (
                f'{self._section}. Upload\n'
                '\n'
                f'   $ upsies submit {self._tracker_cls.name} /path/to/content\n'
            ),
        ))
