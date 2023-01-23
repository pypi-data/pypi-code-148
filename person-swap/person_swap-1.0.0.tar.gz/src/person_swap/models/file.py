import argparse
import logging
import os
import random
import shutil
import string
from datetime import datetime

import cv2
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.utils.functional import cached_property
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.video.io.VideoFileClip import VideoFileClip

from .abstract_file import FileType, AbstractFile
from .model import Model
from ..custom_utils.conversion_exception import ConversionError

logger = logging.getLogger(__name__)


class File(AbstractFile):
    file_object = models.FileField(upload_to='files', null=True, blank=True)

    def define_type(self):
        if (self.file_object and not self.type) or self.type is FileType.OTHER:
            if self.file_object.url.endswith(("png", "jpeg", "jpg")):
                self.type = FileType.IMAGE
            elif self.file_object.url.endswith(("mp3", "wav")):
                self.type = FileType.MP3
            elif self.file_object.url.endswith(("mp4", "avi")):
                self.type = FileType.VIDEO
            else:
                raise ValidationError(f"Cannot recognise {self.file_object.url} file type.")

    def save(self, *args, **kwargs):
        self.define_type()
        super(File, self).save(*args, **kwargs)

    @cached_property
    def display_file(self):
        if self.file_object:
            if self.type == FileType.IMAGE:
                return format_html('<img width="100px" height="100px" src="{img}">', img=self.file_object.url)
            if self.type == FileType.MP3:
                return format_html(
                    f'<audio width="100px" height="100px" controls> <source src="{self.file_object.url}" type="audio/mp3"></audio>')
            if self.type == FileType.VIDEO:
                return format_html(
                    f'<video width="100px" height="100px" controls> <source src="{self.file_object.url}" type="video/mp4"></video>')

            else:
                raise Exception

        return format_html('<strong>There is no image for this entry.<strong>')

    display_file.short_description = 'File'


class ConvertedFile(AbstractFile):
    target = models.ForeignKey(File, on_delete=models.SET_NULL, related_name='target', null=True, blank=True)
    source = models.ForeignKey(File, on_delete=models.SET_NULL, related_name='source', null=True, blank=True)
    created = models.ForeignKey(File, on_delete=models.SET_NULL, related_name='created', null=True, blank=True)
    selected_model = models.ForeignKey(Model, on_delete=models.SET_NULL, null=True, blank=True)

    temp = models.BooleanField(default=False)
    conversion_properties = models.JSONField(default=dict(), null=True, blank=True)

    def image_preview(self):

        if self.created:
            if self.type == FileType.IMAGE:
                return mark_safe(
                    '<img src="{0}" width="300" height="300" style="object-fit:contain" />'.format(
                        self.created.file_object.url))
            if self.type == FileType.VIDEO:
                return mark_safe(
                    f'<video width="300" height="300" controls> <source  src="{self.created.file_object.url}" type="video/mp4"></video>')
        else:
            return '(No image)'

    def define_type(self):
        if self.type and self.type is not FileType.OTHER:
            return
        if self.created and self.created.file_object:
            file_object = self.created.file_object
        elif self.target.file_object:
            file_object = self.target.file_object
        else:
            raise ValidationError(f"Cannot determine '{self.id}' file type.")

        if file_object.url.endswith(("png", "jpeg", "jpg")):
            self.type = FileType.IMAGE
        elif file_object.url.endswith(("mp3", "wav")):
            self.type = FileType.MP3
        elif file_object.url.endswith(("mp4", "avi")):
            self.type = FileType.VIDEO
        else:
            raise ValidationError(f"Cannot recognise {self.file_object.url} file type.")
            # self.type = FileType.Other

    def save(self, *args, **kwargs):
        self.define_type()
        super(ConvertedFile, self).save(*args, **kwargs)

    def _str_(self):
        return self.title

    @cached_property
    def display_file(self):
        if self.created and self.created.file_object:
            if self.type == FileType.IMAGE:
                return format_html('<img width="100px" height="100px" src="{img}">', img=self.created.file_object.url)
            elif self.type == FileType.MP3:
                return format_html(
                    f'<audio width="100px" height="100px" controls> <source src="{self.created.file_object.url}" type="audio/mp3"></audio>')
            if self.type == FileType.VIDEO:
                return format_html(
                    f'<video width="100px" height="100px" controls> <source src="{self.created.file_object.url}" type="video/mp4"></video>')

            else:
                # raise Exception
                pass

        return format_html('<strong>There is no image for this entry.<strong>')

    display_file.short_description = 'File'

    def convert(self):
        try:
            if not self.source or not self.target:
                logger.error("Both source and target need to be provided.")
                raise ConversionError("Both source and target need to be provided.")
            if self.type == FileType.OTHER:
                self.define_type()
            if self.type == FileType.IMAGE or self.target.type == FileType.IMAGE:
                swaped_image = self.selected_model.torchmodel.process(
                    self.target.file_object.path,
                    self.source.file_object.path,
                    self.conversion_properties or self.selected_model.conversion_properties
                )

                self.created = File()
                self.created.file_object.save(
                    f'{self.title}.jpeg' if self.title else f'{datetime.now().strftime("%y-%m-%d_%H:%M")}.jpeg',
                    ContentFile(cv2.imencode(".jpeg", swaped_image)[1])
                )

            if self.type == FileType.VIDEO or self.target.type == FileType.VIDEO:
                video_forcheck = VideoFileClip(self.target.file_object.path)
                if video_forcheck.audio is not None:
                    video_audio_clip = AudioFileClip(self.target.file_object.path)
                else:
                    video_audio_clip = None

                del video_forcheck
                source_audio_clip = None
                if self.source.type == FileType.VIDEO:
                    if VideoFileClip(self.source.file_object.path).audio is not None:
                        source_audio_clip = AudioFileClip(self.target.file_object.path)
                    else:
                        source_audio_clip = None

                    source_vidcap = cv2.VideoCapture(self.source.file_object.path)
                    success, video_image = source_vidcap.read()
                    source_im = None
                    while source_im is None and success:
                        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                        faces = face_cascade.detectMultiScale(video_image, 1.1, 4)
                        if len(faces) > 1:
                            raise Exception()  # TODO
                        if faces.any():
                            source_im = video_image
                        success, video_image = source_vidcap.read()
                    source_vidcap.release()
                elif self.source.type == FileType.MP3:
                    source_im = cv2.imread(self.source.file_object.path)
                elif self.source.type == FileType.IMAGE:
                    source_im = cv2.imread(self.source.file_object.path)
                else:
                    raise Exception()  # TODO sutvarkyyt kiekviena case (pvz audio -> video)
                if source_im is None:
                    raise ConversionError(f'Face does not exist in {self.source.file_object.path}')

                vidcap = cv2.VideoCapture(self.target.file_object.path)
                fps = vidcap.get(cv2.CAP_PROP_FPS)

                success, video_image = vidcap.read()
                count = 0
                width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `width`
                height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                temp_results_dir = 'media/tmp/' + f'{datetime.now().strftime("%d%m%Y") + "".join(random.choices(string.ascii_lowercase, k=10))}'
                if os.path.exists(temp_results_dir):
                    shutil.rmtree(temp_results_dir)
                image_filenames = []

                face_model = self.selected_model if self.selected_model.type == FileType.IMAGE else self.selected_model.videoswapmodel.face_model

                while success:
                    if count % 3 != 0:
                        continue
                    swaped_image = face_model.torchmodel.process_for_video(
                        source_im,
                        video_image,
                        self.conversion_properties or face_model.conversion_properties
                    )
                    swaped_image = cv2.resize(swaped_image, (width, height))

                    image_filenames.append(swaped_image)
                    success, video_image = vidcap.read()
                    count += 1

                vidcap.release()

                save_path = f'{self.title}.mp4' if self.title else f'{datetime.now().strftime("%d%m%Y") + "".join(random.choices(string.ascii_lowercase, k=10))}.mp4'

                clips = ImageSequenceClip([cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) for frame in image_filenames],
                                          fps=fps)
                if video_audio_clip:
                    if source_audio_clip:
                        pass
                    clips = clips.set_audio(video_audio_clip)

                clips.write_videofile(f'media/files/{save_path}')

                self.created = File()
                self.created.file_object.name = f'files/{save_path}'
                self.created.save()

            if self.type == FileType.MP3:
                args = argparse.Namespace(
                    am='fastspeech2_vctk',
                    voc='hifigan_vctk',
                    text=None,
                    ngpu=0,
                    input_path=None,
                    outpur_path=None,
                    am_ckpt=None,
                    am_config=None,
                    am_stat=None,
                    phones_dict=None,
                    voc_config=None,
                    voc_ckpt=None,
                    voc_stat=None,
                    ge2e_params_path=None,
                    use_ecapa=True
                )

                save_path = self.selected_model.voiceswapmodel.process(
                    self.source.file_object.path,
                    self.target.file_object.path,
                    args
                )

                # TODO add voice swap
                self.created = File()
                self.created.file_object.name = "files/" + save_path
                self.created.save()

                self.conversion_properties = self.selected_model.conversion_properties

            # self.save()

        except KeyError as ex:
            raise ex
            logger.error(f"reeeeeee {ex}")
            return False, str(ex)
        return True, ""
