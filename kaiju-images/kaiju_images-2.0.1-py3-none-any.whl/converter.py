from collections import namedtuple
from enum import Enum
from typing import List

from willow import Image
from willow.registry import registry

import kaiju_tools.jsonschema as schema
from kaiju_tools.serialization import Serializable
from kaiju_files.abc import AbstractFileConverter
from kaiju_files.converters import converters

from .functions import *   # required import

__all__ = ['ImageConverter']


class ImageConverter(AbstractFileConverter):
    """
    A class for image conversion/processing.

    Converter accepts a specific set instructions (see `ImageConverter.Settings`)
    of how it will process images. Here is an example of such instruction. You can set
    multiple parameters including version names, which image acts as a source for each
    version, version metadata, extensions etc.

    .. code-block:: python

        {
            'ext': ['jpg', 'jpeg'],
            'filename_mask': 'image[0-9]*',
            'directory_mask': None,
            'meta': {
                'some_meta': True,
            },
            'operations': [
                {'name': 'blur'}
            ],
            'versions': [

                {
                    'version': 'original',
                    'format': 'png',
                    'source': 'unprocessed_original'
                },

                {
                    'version': 'resized',
                    'format': 'jpeg',
                    'source': 'unprocessed_original',
                    'operations': [
                        {'name': 'resize', 'params': [200, 200]}
                    ],
                    'meta': {
                        'tag': 'some_tag'
                    }
                },

                {
                    'version': 'scaled',
                    'format': 'jpeg',
                    'source': 'processed_original',
                    'operations': [
                        {'name': 'scale', 'params': 0.5},
                        {'name': 'flip_vertical'}
                    ],
                    'save_settings': {
                        'quality': 10
                    }
                }

            ]
        }


    Settings object should contain a base settings and version settings. Here is base settings summary:

    .. code-block::

        {
            'ext': ['jpg', 'jpeg'],             # accepted extensions
            'filename_mask': 'image[0-9]*',     # accepted filenames
            'directory_mask': None,             # accpeted dirs
            'meta': {                           # additional user metadata for each version
                'some_meta': True,
            },
            'operations': [         # operations to perform on a base image
                                    # this base processed image can be passed to a version by specifying
                                    # 'source': 'processed_original' in a version settings
                {'name': 'blur'}
            ],
            "versions": [...]       # a list of versions
        }


    Here is a short description of parameters accepted by an image version:

    .. code-block::

        {
            'version': 'resized',  # version name used in metadata under 'version' key
            'format': 'jpeg',      # version format (perform an automatic conversion)
            'source': 'unprocessed_original',   # source of a base image for this version
            'operations': [        # sequential list of operations (see `kaiju_image.functions`)
                {'name': 'resize', 'params': [200, 200]}
            ],
            'meta': {              # additional metadata for this particular version
                'tag': 'some_tag'
            },
            'save_settings': {     # optional args for PIL 'save image' command
                'quality': 10
            },
            "output_extension": "xxx"  # you may provide a different output extension for a file if you really want
        }


    The use of converter itself is pretty straightforward. You can yield versions from
    `ImageConverter.convert` method.

    .. code-block:: python

        for file, metadata in image_converter.convert(test_image_file, **test_meta):
            ...


    Each metadata dict looks like this:

    .. code-block:: python

        {
            'some_meta': True,
            'version': 'scaled',
            'source': 'processed_original',
            'format': 'jpeg',
            'output_extension': None,
            'size': (270, 152)
        }


    Metadata contains essential information about a version as well as user data. File is
    a temporary file object where the version is stored.

    """

    class Settings(AbstractFileConverter.Settings):
        """Image converter settings object."""

        class Version(Serializable):
            """Image version with specific processing."""

            class Sources(Enum):
                """Base image sources for different versions."""

                unprocessed_original = 'unprocessed_original'
                processed_original = 'processed_original'
                previous_version = 'previous_version'

            Operation = namedtuple('Operation', 'name params')
            FORMATS = frozenset(['jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'])
            DEFAULT_SOURCE = Sources.processed_original

            __slots__ = (
                'version', 'source', 'operations', 'format', 'save_settings',
                'output_extension', '_meta')

            def __init__(
                    self, version: str, format: str = None, source: str = None,
                    operations: List[dict] = None, save_settings: dict = None,
                    meta: dict = None, output_extension: str = None):
                """
                :param version: version name (will appear in metadata)
                :param format: image file extension
                :param source: image source (see `Sources`)
                :param operations: list of sequential file processing operations
                    (see `kaiju.files.images.operations`)
                :param save_settings: specific format saving settings (quality etc.)
                :param meta: specific file metadata for this version
                :param output_extension: output file extension
                """

                self.version = str(version)
                self.source = self.Sources[source] if source else self.DEFAULT_SOURCE
                self.operations = self.init_operations(operations)
                if format not in self.FORMATS:
                    raise ValueError(
                        'Can\'t convert to %s format. Allowed formats are: %s.',
                        format, list(self.FORMATS))
                self.format = format
                self._meta = meta
                self.save_settings = {} if save_settings is None else save_settings
                self.output_extension = str(output_extension) if output_extension else self.format

            def repr(self) -> dict:
                return {
                    'version': self.version,
                    'source': self.source.value,
                    'operations': [
                        dict(zip(op._fields, iter(op)))
                        for op in self.operations
                    ],
                    'format': self.format,
                    'meta': self.meta,
                    'save_settings': self.save_settings,
                    'output_extension': self.output_extension
                }

            @property
            def meta(self) -> dict:
                _meta = {
                    'version': self.version,
                    'source': self.source.value,
                    'format': self.format,
                    'output_extension': self.output_extension
                }
                if self._meta:
                    _meta.update(self._meta)
                return _meta

            @classmethod
            def init_operations(cls, operations):

                def _create_operation(name, params=None, **__):
                    if not registry.operation_exists(name):
                        raise ValueError(
                            'Image operation %s doesn\'t exist. Must be one of: %s.',
                            name, list(registry._registered_operations.keys()))
                    return cls.Operation(name=name, params=params)

                if operations is None:
                    return []
                return [
                    _create_operation(**op)
                    for op in operations
                ]

            def perform_operations(self, image: Image) -> Image:
                for op in self.operations:
                    func = getattr(image, op.name)
                    if isinstance(op.params, dict):
                        image = func(**op.params)
                    elif op.params is None:
                        image = func()
                    else:
                        image = func(op.params)
                return image

            def save(self, image: Image, path, mode='wb'):
                func = getattr(image, f'save_as_{self.format}')
                func(path, **self.save_settings)
                return path

        __slots__ = tuple([
            *AbstractFileConverter.Settings.__slots__,
            'operations', 'versions'
        ])

        def __init__(self, versions: List[dict], *args, operations: List[dict] = None, **kws):
            super().__init__(*args, **kws)
            if self.ext is None:
                self.ext = self.Version.FORMATS
            self.operations = self.init_operations(operations)
            self.versions = tuple(
                self.Version(**version)
                for version in versions
            )

        def repr(self) -> dict:
            return {
                **super().repr(),
                'operations': [
                    dict(zip(op._fields, iter(op)))
                    for op in self.operations
                ],
                'versions': [
                    version.repr()
                    for version in self.versions
                ]
            }

        @classmethod
        def spec(cls) -> schema.Object:
            operations = {}
            for ops in registry._registered_operations.values():
                for op, f in ops.items():
                    spec = getattr(f, '__json_spec__', None)
                    if spec is None:
                        spec = schema.Null
                        required = ['name']
                    else:
                        required = ['name', 'params']
                    operations[op] = schema.Object(
                        title=op,
                        description=f.__doc__,
                        name=schema.Constant(
                            op,
                            title='Specific image operation name.'
                        ),
                        params=spec,
                        required=required,
                        additionalProperties=False
                    )

            operations = list(operations.items())
            operations.sort()
            operations = schema.Array(
                items=schema.AnyOf(*(spec for name, spec in operations)),
                nullable=True,
                title='A list of image pre-version conversion operations settings.'
            )

            spec = super().spec().repr()
            properties = spec.pop('properties')

            return schema.Object(
                **spec, **properties,
                operations=operations,
                versions=schema.Array(
                    items=schema.Object(
                        version=schema.String(
                            minLength=1,
                            title='Version name (tag) is required.'
                        ),
                        format=schema.String(
                            enum=list(cls.Version.FORMATS),
                            title='Image format.'
                        ),
                        source=schema.String(
                            enum=[source.value for source in cls.Version.Sources],
                            default=cls.Version.DEFAULT_SOURCE.value,
                            nullable=True,
                            title='Source image for this version.'
                        ),
                        operations=operations,
                        save_settings=schema.Object(
                            nullable=True,
                            title='Conversion settings for a specific format.',
                            description='For JPEG it\'s quality (integer) and optimize (bool). For others may vary.'
                        ),
                        meta=schema.Object(
                            nullable=True,
                            title='Specific version metadata.'
                        ),
                        output_extension=schema.String(
                            nullable=True, minLength=1,
                            title='Output extension for a specific version.'
                        ),
                        additionalProperties=False
                    ),
                    minItems=1, nullable=False,
                    title='A list of image version settings.'
                )
            )

        @classmethod
        def init_operations(cls, operations):
            return cls.Version.init_operations(operations)

        def perform_operations(self, image: Image) -> Image:
            return self.Version.perform_operations(self, image)

    READ_MODE = 'rb'
    WRITE_MODE = 'wb'
    MAX_PROCESSING_TIME = 60

    def _convert(self, input_buffer, **metadata):
        original = Image.open(input_buffer)
        processed_image = previous_version = self.settings.perform_operations(original)

        for version in self.settings.versions:
            if version.source == self.Settings.Version.Sources.processed_original:
                source = processed_image
            elif version.source == self.Settings.Version.Sources.previous_version:
                source = previous_version
            else:
                source = original

            # here a new version translates into the prev to be used by later versions
            previous_version = version.perform_operations(source)
            output_file = self._create_file(ext=version.output_extension)
            version.save(previous_version, output_file, self._write_mode)
            version_metadata = version.meta
            version_metadata['size'] = previous_version.get_size()
            version_metadata['file_size'] = output_file.tell()
            yield output_file, version_metadata


converters.register_class(ImageConverter)
